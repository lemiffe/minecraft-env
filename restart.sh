#!/bin/bash
screen -X -S minecraft-env quit
screen -S minecraft-env -L -d -m python ./app.py
exit 0
