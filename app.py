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
from flask.ext.cors import CORS
import logging
from random import randint
import getopt
import subprocess
from os import listdir
from os.path import isfile, join
import hashlib

# Get the path to this script
abspath = os.path.abspath(__file__)
curr_dir = os.path.dirname(abspath)

# Get the minecraft-bots path
bots_path = os.path.join(curr_dir, '..', 'minecraft-bots')

app = Flask(__name__, static_url_path='')
CORS(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        os.chdir(bots_path)
        content = request.json
        if content is not None:
            if content["ref"] == 'refs/heads/master':
                # Get MD5 checksum of current package.json
                package_json_path = bots_path + '/package.json'
                curr_npm_hash = hashlib.md5(open(package_json_path, 'rb').read()).hexdigest()
                # Pull latest version (master)
                print 'Fetching from Git...'
                bash_command = 'git fetch --all'
                process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
                print 'Resetting --hard to master...'
                bash_command = 'git reset --hard origin/master'
                process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
                print 'Pulling from git...'
                bash_command = 'git pull origin master'
                process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
                # NPM install
                new_npm_hash = hashlib.md5(open(package_json_path, 'rb').read()).hexdigest()
                if curr_npm_hash != new_npm_hash:
                    print 'Running NPM install...'
                    bash_command = 'npm install'
                    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
                    output, error = process.communicate()
                # Get JS files in the bots directory
                files = [f for f in listdir(bots_path) if isfile(join(bots_path, f)) and len(f) > 2 and f[-3:] == '.js']
                # Start bots
                print 'Starting bots...'
                print files
                if len(files) > 0:
                    bash_command = 'screen -list'
                    process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
                    screens, error = process.communicate()
                    for f in files:
                        bot_name = f[:-3]
                        if bot_name not in screens:
                            print ' - Initialising ' + bot_name + ' in a screen'
                            bash_command = 'screen -X -S ' + bot_name + ' quit'
                            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
                            output, error = process.communicate()
                            print output, error
                            bash_command = 'screen -S ' + bot_name + ' -d -m nodemon ' + f
                            process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
                            output, error = process.communicate()
                            print output, error
                return "Deployed"
        return "Invalid request"
    else:
        return 'Hello, I am here!'

if __name__ == "__main__":
    app.debug = True
    port = 5000
    app.run(host='0.0.0.0', port=port)

