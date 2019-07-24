from flask import Flask, request
from flask_api import status
import os
import json
from pathlib import Path
import time
import random
from .datastoreutils import add_entry_to_datastore

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    savefile = Path(app.root_path)/'data.json',
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
                    return resp, status.HTTP_409_CONFLICT
                app.config.update(dict(
                    filelock=False
                ))
                break
        return resp, status.HTTP_201_CREATED
    else:
        return 'Bad request', status.HTTP_400_BAD_REQUEST
            