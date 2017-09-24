# -*- coding: utf-8 -*-
from __future__ import unicode_literals



titles = ["text","msisdn","message-timestamp","to","type","messageId","keyword","timestamp","concat","concat-ref","concat-total","concat-part",]

messages = []


from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import ast
import brain

# from .models import Post
# from .froms import PostForm
@csrf_exempt
def request_msg(request):

    if request.method == 'GET':
        data = request.GET
        print '_'*20+'\n'
        print data
        print '_'*20+'\n'
        print 'get request'

    elif request.method == 'POST':
        data = request.POST
        print '_'*20+'\n'
        print data
        print '_'*20+'\n'
        print 'post request'
    else:
        print 'no request'


    myDict = dict(data.iterlists())

    f = open('msg_data.csv',  'r+')
    # for x in myDict.keys():
    #     f.write(x+',')

    compare = f.readlines()[0].split(",")
    # compare = ['"text"','"msisdn"','"message-timestamp"','"to"','"type"','"messageId"','"keyword"','"timestamp"','"concat"','"concat-ref"','"concat-total"','"concat-part"',]
    # print compare
    # for x in compare:
    #     f.write(x+',')
    try:
        start = "{u'keyword': "

        start += myDict.values()[0][0]
        if start[-1] != '}':
            start = '}'

        newd = ast.literal_eval(start)

        print newd

        for x in newd.keys():
            print x + ' key'


    except:
        print myDict.values()
        newd = myDict

        for x in newd.keys():
            print x + ' key'

    for a in compare:
        x = a.replace('"', '')
        if x in newd.keys():
            f.write(newd[x][0].replace(',', '')+',')
        else:
            f.write(",")
    f.write('\n')
    f.close()

    for a in newd.values():
        a[0] = a[0].replace('"', '')
        a[0] = a[0].replace(',', '')
    print newd


    mc = brain.MessageCounter()
    mc.on_chat_message(newd)



    return HttpResponse("200")
