import sys, traceback, re, os, shutil, string
from collections import defaultdict
from decimal import *
from datetime import datetime, date, time, timedelta
import time as tyme
from collections import OrderedDict
import base64
import ssl
import json
from flask import Flask, jsonify, request, abort, url_for, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask.ext.cors import CORS
import logging
from random import randint
import getopt
import subprocess

# Change directory to the location of this script
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

app = Flask(__name__, static_url_path='')
CORS(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    global_limits=["10000 per minute", "50 per second"],
)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        content = request.json
        if content is not None:
            if content["ref"] == "refs/heads/master":
                os.chdir(os.path.join(dname, '..', 'minecraft-bots'))
                bash_command = "git pull origin master"
                process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
                return "Deploying"
        return "Invalid request"
    else:
        return 'Hello, woof!'

if __name__ == "__main__":
    app.debug = True
    port = 5000
    app.run(host='0.0.0.0', port=port)

