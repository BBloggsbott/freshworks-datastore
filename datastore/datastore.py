from flask import Flask, request
from flask_api import status
import os
import json
from pathlib import Path
import time
import random
from .datastoreutils import add_entry_to_datastore, read_entry_from_datastore, delete_entry_from_datastore, write_timetolive, read_timetolive, isalive, intimetolive

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    savefile = 'data.json',
    filelock = False,
    timetolivelock = False,
    timetolivefile='timetolive.json'
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
        time_to_live = request.args.get('timetolive')
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
                while True:
                    if time_to_live==None:
                        break
                    elif not app.config['timetolivelock']:
                        app.config.update(dict(
                            timetolivelock=True
                        ))
                        timetolivedict = read_timetolive(app.config['timetolivefile'])
                        timetolivedict[new_key] = (int(time.time()), int(time_to_live))
                        write_timetolive(timetolivedict, app.config['timetolivefile'])
                        app.config.update(dict(
                            timetolivelock=False
                        ))
                        break
                    else:
                        time.sleep(random.random())
                break
        return resp, status.HTTP_201_CREATED
    else:
        return 'Bad request', status.HTTP_400_BAD_REQUEST
            

@app.route('/read', methods=['GET', 'POST'])
def read_entry():
    if request.method == 'GET':
        resp = ''
        key = request.args.get('key')
        cur_time = time.time()
        while True:
            if app.config['filelock']:
                time.sleep(random.random())
            else:
                while True:
                    if not app.config['timetolivelock']:
                        app.config.update(dict(
                            timetolivelock=True
                        ))
                        if intimetolive(key, app.config['timetolivefile']):
                            if not isalive(key, cur_time, app.config['timetolivefile']):
                                app.config.update(dict(
                                    timetolivelock=False
                                ))
                                return 'Cannot read. Key has expired', status.HTTP_403_FORBIDDEN
                        app.config.update(dict(
                            timetolivelock=False
                        ))
                        break
                    else:
                        time.sleep(random.random())
                success, resp = perform_action_thread_safe(read_entry_from_datastore, key, app.config['savefile'])
                if not success:
                    return resp, status.HTTP_404_NOT_FOUND
                break
        return resp, status.HTTP_200_OK
    else:
        return 'Bad request', status.HTTP_400_BAD_REQUEST
                
@app.route('/delete', methods=['GET', 'POST'])
def delete_entry():
    cur_time= time.time()
    if request.method == 'GET':
        resp = ''
        key = request.args.get('key')
        while True:
            if app.config['filelock']:
                time.sleep(random.random())
            else:
                while True:
                    if not app.config['timetolivelock']:
                        app.config.update(dict(
                            timetolivelock=True
                        ))
                        if intimetolive(key, app.config['timetolivefile']):
                            if not isalive(key, cur_time, app.config['timetolivefile']):
                                app.config.update(dict(
                                    timetolivelock=False
                                ))
                                return 'Cannot delete. Key has expired', status.HTTP_403_FORBIDDEN
                        app.config.update(dict(
                            timetolivelock=False
                        ))
                        break
                    else:
                        time.sleep(random.random())
                success, resp = delete_entry_from_datastore(key, app.config['savefile'], app.config['timetolivefile'])
                if not success:
                    return resp, status.HTTP_404_NOT_FOUND
                break
        return resp, status.HTTP_200_OK
    else:
        return 'Bad request', status.HTTP_400_BAD_REQUEST