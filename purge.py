# -*- coding: utf-8 -*-

import time
import datetime




while True:
    f = open('big.db', 'r+')
    finfo = f.read()
    print finfo


    exec('info = ' + finfo)

    print info

    for x in info:
        if info[x]['timestamp'] <= datetime.datetime.now()\
        - datetime.timedelta(seconds=10):
            if info[x]['state'][-1] == 20:
                msg = "Sorry, we couldn't find anyone... \
Text 'sup' to try again."
                num = 'tollfree'
                info[x]['state'].append(0)
            elif info[x]['state'][-1] == 30:
                msg = "Your session has timed out... \
Text 'sup' to the main number to find someone else."
                num = 'chat forwarder'

                info[x]['state'].append(0)
    print '\n'
    print info
    print

    f.seek(0)
    f.truncate()
    f.write(str(info))
    f.close()
            

    time.sleep(5)
