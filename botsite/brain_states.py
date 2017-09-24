import random


class MessageCounter(object):


    counter = {}
    count = 0
    info = {
        'what' : '',
        'where' : '',
        'when' : '',
    }

    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self.db = open("big.db", "rw+")
        self.food = ['food', 'lunch', 'meal', 'eat', '']
        self.greetings = [
            'Hello there!', 'Buenos dias!', 'Guten tag!',
            'Well met!', 'Hello!'
        ]
        self.what = [
            "What would you like to do?",
            "What are you up to today?"
        ]
        self.where = [
            'And where would you like to do this?'
        ]
        self.when = [
            'And when would you like to do this?'
        ]
        self.errors = [
            "Sorry, please try again.",
            "Sorry, try again?"

        ]

    def food(text):
        # returns a restaurant from a list of nearby food places
        pass

    def question(self, text):
        msg = ''
        if self.count == 0:
            msg = random.choice(self.greetings)
        elif self.count == 10:
            msg = random.choice(self.what)
        elif self.count == 20:
            self.info['what'] = text
            msg = random.choice(self.where)
        elif self.count == 30:
            self.info['where'] = text
            msg = random.choice(self.when)
        return msg

    def on_chat_message(self, msg):

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

        command = text.lower()

        print command

        if msisdn not in self.counter.keys():
            self.counter[msisdn] = [0]
        else:

            self.count = self.counter[msisdn][-1] + 10
            self.counter[msisdn].append(self.count)

        print self.counter

        comd_dict = {
            '0' : 0,
            # '1' : 10,
            # '2' : 20,
            # '3' : 30
        }

        if command in comd_dict.keys():
            self.count = 0
            self.count += comd_dict[command]

        print self.count

        if self.count == 40:
            self.info['when'] = text
            resp = "So you want %s at %s within the next %s hours. \
Is this confirmed?" % (
            self.info['what'],
            self.info['where'],
            self.info['when'])
        elif self.count < 40:
            resp = self.question(text)
        else:
            resp = random.choice(self.errors)

        print resp

        print self.counter

        self.db.truncate()
        self.db.write(str(self.counter))
