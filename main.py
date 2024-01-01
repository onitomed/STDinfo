import sys
from mpyc.runtime import mpc

m = len(mpc.parties)
l = 6

if m%2 == 0:
    print('Odd number of parties required.')
    sys.exit()

t = m//2

voters = list(range(t+1))  # parties P[0],...,P[t]

if mpc.pid in voters:
    vote = int(sys.argv[1]) if sys.argv[1:] else 0  # default "clear"
else:
    vote = None  # no input


secdata = mpc.SecInt(l)  # secure bits over GF(2)

mpc.run(mpc.start())
votes = mpc.input(secdata(vote), senders=voters)
result = mpc.run(mpc.output(mpc.xor(votes[0],votes[1]), receivers=voters))
if result!=None:
    if '1' in str(result):
        result=1
    else: 
        result=0
mpc.run(mpc.shutdown())

if result is None:  # no output
    print('Thanks for serving as oblivious matchmaker')
elif result:
    print('no Match')
else:
    print('match')