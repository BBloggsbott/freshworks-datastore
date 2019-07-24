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
                app.config.update(dict(
                    filelock=True
                ))
                success, resp = add_entry_to_datastore(new_key, new_value, app.config['savefile'])
                if not success:
                    app.config.update(dict(
                        filelock=False
                    ))
                    return resp, status.HTTP_409_CONFLICT
                app.config.update(dict(
                    filelock=False
                ))
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
                app.config.update(dict(
                    filelock=True
                ))
                success, resp = read_entry_from_datastore(key, app.config['savefile'])
                if not success:
                    app.config.update(dict(
                        filelock=False
                    ))
                    return resp, status.HTTP_404_NOT_FOUND
                app.config.update(dict(
                    filelock=False
                ))
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
                app.config.update(dict(
                    filelock=True
                ))
                success, resp = delete_entry_from_datastore(key, app.config['savefile'])
                if not success:
                    app.config.update(dict(
                        filelock=False
                    ))
                    return resp, status.HTTP_404_NOT_FOUND
                app.config.update(dict(
                    filelock=False
                ))
                break
        return resp, status.HTTP_200_OK
    else:
        return 'Bad request', status.HTTP_400_BAD_REQUEST