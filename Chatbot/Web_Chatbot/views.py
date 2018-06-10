# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
import logging

# Create your views here.
@ensure_csrf_cookie
def index(request):
    logger = logging.getLogger('testlogger')
    logger.info('This is a simple log message')
    return render(request, 'index.html')

@ensure_csrf_cookie
def response(request):
    bot=ChatBot('Bot')
    bot.set_trainer(ListTrainer)

    postData = request.POST
    message = postData.get('data[msg]')

    # for _file in os.listdir('/home/pavan/Desktop/Chatbot/Chatbot/Web_Chatbot/templates/Conversation'):
    #     data=open('/home/pavan/Desktop/Chatbot/Chatbot/Web_Chatbot/templates/Conversation/' + _file,'r').readlines()
    #     bot.train(data)
            
    if message.strip() != 'Bye':
             reply = bot.get_response(message)
    if message.strip() == 'Bye':
             reply = 'Bye'
    return HttpResponse(reply)
