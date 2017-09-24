import json
import urllib2
#Read file and print a line
webFD = urllib2.urlopen("http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/assignment4.txt")
tweets = webFD.readlines()

for tweet in tweets:
    print tweet


    #create dictionary
    try:
        dictt = json.loads(tweet)
    except ValueError:
        continue

    #print dictionary
    print dictt.keys()

    #print values
    print dictt.values()



    #loop through tweets
    for (key, value) in dictt.items():
        print key, '->', value


    #Created the DB
    import sqlite3

    conn = sqlite3.connect('twitter.db')
    c = conn.cursor()
