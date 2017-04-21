import sys,argparse,os
from boto.mturk.connection import MTurkConnection, MTurkRequestError
from boto.mturk.question import ExternalQuestion
from boto.mturk.qualification import NumberHitsApprovedRequirement, Qualifications

# i need to add argparse arguments

TITLE = 'Smart Resume Sample 22'
DESCRIPTION = "sr sample 22"


if len(sys.argv) < 2:
    print 'you need to specify the number of assignments'
    print "usage: 'mturk' num_assignments [-n|--new][-l|--live][--free][-r|--requirement][-d|--dev]"
    sys.exit(1)
else:
    assignments = sys.argv[1]

'''Arguments we accept currently:'''
NEWHIT=     set(["-n","--new"])
LIVE=       set(["-l","--live"])
FREE=       set([     "--free"])
REQUIREMENT=set(["-r","--requirement"])
DEV=        set(["-d","--dev"])

argset=set(sys.argv)

if LIVE.intersection(argset):
#if '-l' in sys.argv or '--live' in sys.argv:
    host = 'mechanicalturk.amazonaws.com'
else:
    host = 'mechanicalturk.sandbox.amazonaws.com'

mtc = MTurkConnection(host=host, aws_access_key_id=os.environ["AWS_KEY"],
                                 aws_secret_access_key=os.environ["AWS_SECRET"])

# if DEV.intersection(argset):
#     ext_url = 'https://wearedynamo-dev.herokuapp.com/registration_codes/new'
# else:
ext_url = 'https://s3-us-west-2.amazonaws.com/cs399-research/testhit.html'

question = ExternalQuestion(ext_url, 400)

requirement = NumberHitsApprovedRequirement('GreaterThan', 5, True)
qualifications = Qualifications()

if REQUIREMENT.intersection(argset):
#if '-r' in sys.argv or '--requirement' in sys.argv:
    qualifications.add(requirement) 

payment=0 if FREE.intersection(argset) else 0.03
#"--free" in sys.argv else 0.10

try:
    #if "-e" in sys.argv or "--extend" in sys.argv
    if NEWHIT.intersection(argset):
        mtc.create_hit(question=question, title=TITLE, description=DESCRIPTION,
                keywords='Photography', duration=3600, reward=payment,
                qualifications=qualifications, max_assignments=assignments,
                approval_delay=0)
    else:
        DynamoHIT=list(mtc.get_all_hits())
        if len(DynamoHIT)!=1:
            print "Can't identify 1 clear HIT to extend, breaking."
            if len(DynamoHIT)==0:
                print "You seem to have no HITs. Please use the -n or --new parameters to make one."
            sys.exit(1)
        else:
            DynamoHIT=DynamoHIT[0]
            print "extending HIT {} by {} assignments"\
                    .format(DynamoHIT.HITId,assignments)
            mtc.extend_hit(DynamoHIT.HITId,assignments=assignments)
except MTurkRequestError as e:
    print 'request failed'
    print e.body
else:
    print 'request successful'
