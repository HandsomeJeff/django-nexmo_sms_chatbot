

alist = ['Memorial Union', 'Hassayampa', 'Manzanita', 'Sonora Center',
         'Noble Library', 'Design School', 'Sun Devil Fitness Complex',
         'Mill Ave']


arizona_state = {}

for x in alist:
    arizona_state[x] = 0

big_dict = {'arizona_state' : arizona_state}

print big_dict

f = open('places.db', 'w')
f.write(str(big_dict))
f.close()

print str(big_dict)
