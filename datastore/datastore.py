from flask import Flask
import os

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    savefile = os.path.join(app.root_path, 'data.json')
))

