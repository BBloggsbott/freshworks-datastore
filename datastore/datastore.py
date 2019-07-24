from flask import Flask, request
from flask_api import status
import os
import json
from pathlib import Path
import time
import random
from .datastoreutils import add_entry_to_datastore, read_entry_from_datastore, delete_entry_from_datastore

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    savefile = 'data.json',
    filelock = False
))

def perform_action_thread_safe(func, *args):
    app.config.update(dict(
        filelock=True
    ))
    success, resp = func(*args)
    app.config.update(dict(
        filelock=False
    ))
    return success, resp

@app.route('/create', methods=['GET', 'POST'])
def create_entry():
    if request.method == 'GET':
        new_key = request.args.get('key')
        new_value = request.args.get('value')
        resp = ''
        try:
            new_value = json.loads(new_value)
        except:
            return "Error parsing request data", status.HTTP_400_BAD_REQUEST
        
        while True:
            if app.config['filelock']:
                time.sleep(random.random())     #To prevent multiple threads from locking file at the same time
            else:
                success, resp = perform_action_thread_safe(add_entry_to_datastore, new_key, new_value, app.config['savefile'])
                if not success:
                    return resp, status.HTTP_409_CONFLICT
                break
        return resp, status.HTTP_201_CREATED
    else:
        return 'Bad request', status.HTTP_400_BAD_REQUEST
            

@app.route('/read', methods=['GET', 'POST'])
def read_entry():
    if request.method == 'GET':
        resp = ''
        key = request.args.get('key')
        while True:
            if app.config['filelock']:
                time.sleep(random.random())
            else:
                success, resp = perform_action_thread_safe(read_entry_from_datastore, key, app.config['savefile'])
                if not success:
                    return resp, status.HTTP_404_NOT_FOUND
                break
        return resp, status.HTTP_200_OK
    else:
        return 'Bad request', status.HTTP_400_BAD_REQUEST
                
@app.route('/delete', methods=['GET', 'POST'])
def delete_entry():
    if request.method == 'GET':
        resp = ''
        key = request.args.get('key')
        while True:
            if app.config['filelock']:
                time.sleep(random.random())
            else:
                success, resp = delete_entry_from_datastore(key, app.config['savefile'])
                if not success:
                    return resp, status.HTTP_404_NOT_FOUND
                break
        return resp, status.HTTP_200_OK
    else:
        return 'Bad request', status.HTTP_400_BAD_REQUEST