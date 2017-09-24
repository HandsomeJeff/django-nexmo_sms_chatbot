import time
import datetime
import ast

print type(datetime.datetime.now())


alist = ['Memorial Union', 'Hassayampa', 'Manzanita', 'Sonora Center',
         'Noble Library', 'Design School', 'Sun Devil Fitness Complex',
         'Mill Ave']


arizona_state = {}

for x in alist:
    arizona_state[x] = datetime.datetime.now()

big_dict = arizona_state

print big_dict

f = open('newpurge.db', 'w')
f.write(str(big_dict))
f.close()

print str(big_dict)

f = open('newpurge.db', 'r')
dog = str(f.read())
print 'dog = ' + dog
exec('dog = ' + dog)


print dog

while True:
    time.sleep(1)
    print 123
    for x in dog:
        if dog[x] > datetime.datetime.now()\
        - datetime.timedelta(seconds=5):
            print x
