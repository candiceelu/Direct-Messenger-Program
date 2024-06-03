# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Candice Lu
# candicl4@uci.edu
# 31761066

import json
import socket
from collections import namedtuple
from Profile4 import time

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['type','message', 'token'])
DMTuple = namedtuple('DMTuple', {'type', 'message'})

def extract_json(json_msg:str) -> DataTuple:
    '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
    try:
        json_obj = json.loads(json_msg)
        type = json_obj['response']['type']
        message = json_obj['response']['message']
        token = json_obj['response']['token']
    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return DataTuple(type, message, token)

def extract_json_dm(json_msg: str) -> list:
    try:
        json_obj = json.loads(json_msg)
        response = json_obj["response"]
        type = response["type"]
        messages =[]
        if "message" in response:
            message = response["message"]
            return DMTuple(type=type, message=message)
        elif "messages" in response:
            msg_lst = response["messages"]
            for msg in msg_lst:
                messages.append(msg)
            return DMTuple(type=type, message=messages)

    except json.JSONDecodeError:
        print("Json cannot be decoded.")

def gen_token(username, password, server):
    join_msg = join_command(username, password)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, 3021))
    send = s.makefile('w')
    recv = s.makefile('r')

    send.write(join_msg + '\r\n')
    send.flush()
    srv_msg = recv.readline()[:-1]
    resp = extract_json(srv_msg)
    token = resp.token
    if resp.type == 'error':
        print(f'ERROR: {resp.message}')
        return False
    elif resp.type == 'ok':
        return (token, s)

def join_command(username:str, password:str) -> str:
    x = {"join": {"username": username, "password": password, "token": ""}}
    msg = json.dumps(x)

    return msg

def post_command(token, entry) -> str:
    x = {"token": token, "post": {"entry": entry, "timestamp": time.time()}}
    msg = json.dumps(x)

    return msg

def bio_command(token, entry) -> str:
    x = {"token": token, "bio": {"entry": entry, "timestamp": time.time()}}
    msg = json.dumps(x)

    return msg

def direct_message(token:str, dm=None, entry=None, recipient=None) -> str:
    if dm is not None:
        x = {"token": token, "directmessage": dm}
    elif entry is not None:
        x = {"token": token, "directmessage": {"entry": entry, "recipient": recipient, "timestamp": time.time()}}
    msg = json.dumps(x)

    return msg
