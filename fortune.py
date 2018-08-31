#!/usr/bin/env python3
# coding: utf-8

import os
import datetime

from flask import Flask, request, jsonify
import cek
import logging

app = Flask(__name__)

# Create a separate logger for this application
logger = logging.getLogger('cek_fortune_python')

# application_id is used to verify requests.
application_id = os.environ.get("APPLICATION_ID")
# Set debug_mode=True if you are testing your extension. If True, this disables request verification
clova = cek.Clova(application_id=application_id, default_language="ja", debug_mode=False)

@app.route('/clova', methods=['POST'])
def my_service():

    # Forward the request to the Clova Request Handler
    # Just pass in the binary request body and the request header as a dictionary
    body_dict = clova.route(body=request.data, header=request.headers)

    response = jsonify(body_dict)
    # make sure we have correct Content-Type that CEK expects
    response.headers['Content-Type'] = 'application/json;charset-UTF-8'
    return response

# 応答の最後に追加するテンプレート
TEMPLATE_INQUIRY = '星座を言うか、使い方、もしくは終了と呼びかけて下さい。'

def print_request(r):
    print(r.request_type)
    if r.is_intent:
        print(r.intent_name)
    print(r.is_intent)
    print(r.user_id)
    print(r.application_id)
    print(r.access_token)
    print(r.session_id)
    print(r.session_attributes)
    if r.is_intent:
        print(r.slots_dict)

@clova.handle.launch
def launch_request_handler(clova_request):
    print_request(clova_request)
    return clova.response('「サンプル占い」が起動されました。' + TEMPLATE_INQUIRY)

@clova.handle.intent("FortuneIntent")
def fortune_intent_handler(clova_request):
    print_request(clova_request)
    fortunes = ['大吉', 'ちゅうきち', '小吉', '吉', '凶']
    zodiacSigns = ['牡羊座', '牡牛座', '双子座', '蟹座', '獅子座', '乙女座', '天秤座', '蠍座', '射手座', '山羊座', '水瓶座', '魚座']
    print((datetime.date.today().day + zodiacSigns.index(clova_request.slots_dict['zodiac_signs'])) % len(fortunes))
    fortuneToday = fortunes[(datetime.date.today().day + zodiacSigns.index(clova_request.slots_dict['zodiac_signs'])) % len(fortunes)]

    return clova.response('{}の今日の運勢は{}です。'.format(clova_request.slots_dict['zodiac_signs'], fortuneToday))

# Handles Build in Intents
@clova.handle.intent("Clova.GuideIntent")
def guide_intent(clova_request):
    response = clova.response(TEMPLATE_INQUIRY)
    return response


@clova.handle.intent("Clova.CancelIntent")
def cancel_intent(clova_request):
    response = clova.response(TEMPLATE_INQUIRY)
    return response

@clova.handle.intent("Clova.YesIntent")
def yes_intent(clova_request):
    response = clova.response(TEMPLATE_INQUIRY)
    return response

@clova.handle.intent("Clova.NoIntent")
def no_intent(clova_request):
    response = clova.response(TEMPLATE_INQUIRY)
    return response

@clova.handle.end
def end_handler(clova_request):
    pass


# In case not all intents have been implemented the handler falls back to the default handler
@clova.handle.default
def default_handler(request):
    response = clova.response('想定しないインテントです。カスタムインテントの名前が正しいかご確認ください。')
    return response

if __name__ == '__main__':
    app.run(host="localhost", debug=True, port=5000)
