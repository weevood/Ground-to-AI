#!/usr/bin/env python3
# coding=utf-8

import requests
from utils.constants import *

# Send message to a predefined telegram chat
def send(message, chat_id=BOT_USER_ID, token=BOT_API_TOKEN):
    print(message)
    try:
        query = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + message
        response = requests.get(query)
        return response.json()
    except Exception as e:
        print(e)
    return
