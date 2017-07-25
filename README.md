# Minecraft Bots Environment + Deployer

- Simple deployment mechanism for the "minecraft-bots" project
- Consists of a web server which performs a few tasks such as pulling the repo + running npm install + starting unitialised bots in screen sessions
- To be used in conjunction with Github webhooks and the "minecraft-bots" project

## Workflow

- Set up a Github webhook on a fork of the "minecraft-bots" repository
- Point it towards this server (by default it runs on port 5000) and set it to only act on PUSH events
- Be sure to clone the minecraft-bots project in a sibling directory (minecraft-env and minecraft-bots should be side by side)
- Every time you push/merge into the "master" branch on minecraft-bots, it will trigger this script which pulls the latest code and stats bots.

## Installation

- Requires Python 2.7+
- Install pip (apt-get install python-pip)
- Install flask + requirements (pip install -r requirements.txt)
- Run in a screen, e.g. screen -X -S minecraft-env quit && screen -S minecraft-env -d -m python ./app.py

## Usage

- Post to localhost:5000 (with a Github Webhook payload)
- To test if the server is running, perform a curl request (e.g. curl -X GET http://localhost:5000)
