# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import datetime

# nexmo stuff
import nexmo
import urllib
import urllib2

# Enter Nexmo api keys below
api_key = ""
api_secret = ""
client = nexmo.Client(key=api_key, secret=api_secret)


class MessageCounter(object):

    # tollfree = '18887871694'
    tollfree = '12035638086'
    from_num = ''
    to_num = ''
    counter = {}
    count = 0
    places = {
        '1' : 'Memorial Union',
        '2' : 'Hassayampa',
        '3' : 'Manzanita',
        '4' : 'Sonora',
        '5' : 'Noble',
        '6' : 'Design',
        '7' : 'SDFC',
        '8' : 'Mill Ave'
    }
    rooms = {}
    sessions = {}
    for key in places.values():
        rooms[key] = []
    for key in places.keys():
        sessions[key] = []

    fake_num = {
        '12034869067' : {},
        # '123' : {},
    }

    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)

        self.db = open("big.db", "rw+")

        self.greetings = [
            'Hello there!', 'Buenos dias!', 'Guten tag!',
            'Well met!', 'Hello!'
        ]
        self.what = [
            "What would you like to do?",
            "What are you up to today?"
        ]
        # self.places = [
        #     'Memorial Union', 'Hassayampa', 'Manzanita',
        #     'Sonora Center', 'Noble Library', 'Design School',
        #     'Sun Devil Fitness Complex', 'Mill Ave'
        # ]

        self.errors = [
            "Sorry, please select a valid number.",
            "Sorry, try again with a valid number?"

        ]

    def send_sms(self, to_num, msg, from_num):
        params = {
            'api_key': api_key,
            'api_secret': api_secret,
            'to': to_num,
            'from': from_num,
            'text': msg
        }

        url = 'https://rest.nexmo.com/sms/json?' + urllib.urlencode(params)

        request = urllib2.Request(url)
        request.add_header('Accept', 'application/json')
        response = urllib2.urlopen(request)



    def match_found(self):
        """
        Goes through list of users queuing at each location.

        If list contains two or more users in queue, creates a pairing
        between the first two and add to number in list of numbers.

        Users are then removed from queue.
        """

        for key in self.rooms:
            if len(self.rooms[key]) >= 2:
                num1 = self.rooms[key].pop(0)
                num2 = self.rooms[key].pop(0)
                supnum = min(self.fake_num)
                self.fake_num[supnum][num1] = num2
                self.fake_num[supnum][num2] = num1
                print "to %s: Match Found!" % num1
                print "to %s: Match Found!" % num2
                self.counter[num1]['state'].append(30)
                self.counter[num1]['timestamp'] = datetime.datetime.now()
                self.counter[num1]['phone'] = supnum
                self.counter[num2]['state'].append(30)
                self.counter[num2]['timestamp'] = datetime.datetime.now()
                self.counter[num2]['phone'] = supnum
                import time
                self.send_sms(num1, "We have found a match! Say sup!", supnum)
                time.sleep(1)
                self.send_sms(num2, "We have found a match! Say sup!", supnum)


        return



    def question(self, text, to, msisdn):
        """
        Creates a message to be used to respond to user's texts.

        Toll-free number responds to users in states 0 to 20.

        Long numbers respond to users in state 30.
        """

        msg = ''
        if to == self.tollfree:
            self.from_num = to
            self.to_num = msisdn
            if self.count == 0:
                if 'sup' in text:
                    msg += random.choice(self.greetings) + '\n'\
                    + "Where would you like to go?" + '\n\n'
                    for x in range(1, len(self.places) + 1):
                        msg += str(x) + '. ' + self.places[str(x)] + '\n'
                    self.count += 10
                else:
                    self.count = 0
                self.counter[msisdn]['state'].append(self.count)
            elif self.count == 10:
                if text in self.places:
                    x = text
                    place = self.places[x]
                    msg += "Thanks! You have selected %s. %s."\
                    % (x, place) + '\n'\
                    + "We'll let you know if anyone else is interested."\
                    + '\n' + "Reply 'c' to cancel."
                    self.count += 10
                    self.counter[msisdn]['state'].append(self.count)
                    if msisdn not in self.rooms[place]:
                        self.rooms[place].append(msisdn)
                    self.counter[msisdn]['timestamp'] = datetime.datetime.now()
                    self.counter[msisdn]['phone'] = self.tollfree
                    self.match_found()


                else:
                    self.count = 10
                    self.counter[msisdn]['state'].append(self.count)
                    msg = random.choice(self.errors)


            elif self.count == 20:
                if text == 'c':
                    self.count = 0
                    self.counter[msisdn]['state'].append(self.count)
                    for place in self.rooms:
                        if msisdn in self.rooms[place]:
                            self.rooms[place].remove(msisdn)
                    msg = "Your queue has been cancelled. \
Text 'sup' to start a new one!"
                else:
                    msg = "Searching...\nText 'c' to cancel."
            elif self.count == 30:
                msg = "It would appear you are already in a \
conversation with someone."
            else:
                return

        elif to in self.fake_num:
            self.from_num = to
            if self.count == 30:
                msg = text
                self.to_num = self.fake_num[self.from_num][msisdn]
                if '/endchat' in text:
                    self.counter[msisdn]['state'].append(0)
                    self.counter[self.fake_num\
                    [self.from_num][msisdn]]['state'].append(0)
                    num2 = self.fake_num.pop(msisdn, None)
                    self.fake_num.pop(num2, None)
                print self.fake_num
            elif self.count == 0\
            or self.count == 10\
            or self.count == 20:
                msg = "Oops, there doesn't seem to be anyone here..."
            else:
                return
        else:
            return

        return msg

    def on_chat_message(self, msg):
        """
        Takes message information (dictionary) as argument.

        Strips each value from its key, to be used in subsequent
        functions.
        """

        try:
            _type = msg['type'][0]
        except:
            pass
        try:
            to = msg['to'][0]
        except:
            pass
        try:
            msisdn = msg['msisdn'][0]
        except:
            pass
        try:
            messageId = msg['messageId'][0]
        except:
            pass
        try:
            message_timestamp = msg['message_timestamp'][0]
        except:
            pass
        try:
            datestamp = msg['datestamp'][0]
        except:
            pass
        try:
            timestamp = msg['timestamp'][0]
        except:
            pass
        try:
            nonce = msg['nonce'][0]
        except:
            pass
        try:
            text = msg['text'][0]
        except:
            pass
        try:
            concat = msg['concat'][0]
        except:
            pass
        try:
            concat_ref = msg['concat_ref'][0]
        except:
            pass
        try:
            concat_total = msg['concat_total'][0]
        except:
            pass
        try:
            concat_part = msg['concat_part'][0]
        except:
            pass

        print _type

        text = text.lower()



        if msisdn not in self.counter.keys():
            self.counter[msisdn] = {}
            self.counter[msisdn]['state'] = [0]
            self.counter[msisdn]['timestamp'] = datetime.datetime.now()
            self.counter[msisdn]['phone'] = self.from_num


        else:
            if text == 'unsup':
                self.counter.pop(msisdn, None)
                resp = "You have successfully unsubscribed. See you next time!"
                self.send_sms(msisdn, resp, tollfree)

                self.db.truncate()
                self.db.write(str(self.counter))
                self.db.close()
                return
            if (self.counter[msisdn]['state'][-1] == 20\
            or self.counter[msisdn]['state'][-1] == 30)\
            and self.counter[msisdn]['timestamp'] <= datetime.datetime.now()\
            - datetime.timedelta(minutes=15):
                self.count = 0
                self.counter[msisdn]['state'].append(self.count)
            else:
                self.count = self.counter[msisdn]['state'][-1]

        print self.counter

        print self.count

        if len(self.counter[msisdn]) == 1 and text != 'sup':
            resp = "Welcome to SUP! Text 'sup' to get started now! Text \
'unsup' to unsubscribe (but let's hope it doesn't get to that, yea)."
            self.send_sms(msisdn, resp, self.tollfree)
            self.counter[msisdn]['state'].append(self.count)
        else:
            resp = self.question(text,to,msisdn)

        print resp
        print self.from_num
        print self.to_num

        print self.count

        print self.counter

        print self.rooms
        print self.fake_num


        self.send_sms(self.to_num, resp, self.from_num)

        self.db.truncate()
        self.db.write(str(self.counter))
        self.db.close()
