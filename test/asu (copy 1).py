from datetime import datetime, timedelta


a = datetime.now()

for x in range(10):
    c = 0
    c += 1



import json

print int(' 1  ')

f = open('places.db', 'r+')

fr = f.read().replace("'",'"')


sch_dict = json.loads(fr)

f.close()

places = sch_dict.keys()

places.sort()

choices = {}

i = 1
for x in places:
    choices[str(places.index(x)+1)] = x


print choices


inp = '1'

sch_dict[choices[inp]] += 1

print sch_dict

numlist = [str(x) for x in sch_dict.values()]

print numlist

numlist.sort()

numlist = [int(x) for x in numlist]

print numlist


choicelist = []
for x in numlist[::-1]:
    for y in sch_dict.keys():
        if y not in choicelist and sch_dict[y] == x:
            choicelist.append(y)


print choicelist[:5]

def fe():
    if False:
        supnum = '123'
        return (True, supnum)
    return (False, None)

if fe():
    print fe()[1]
print '\\endchat'

b = datetime.now()

print a > b - timedelta(minutes=1)

print timedelta(minutes=1)
print b-a
