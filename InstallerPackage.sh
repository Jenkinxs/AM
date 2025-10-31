#!/bin/bash
apt-get update
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y 
sudo apt install ffmpeg -y 
pip install -r requirements.txt --break-system-packages
pip install -U "discord.py[voice]" --break-system-packages
pip3 install -r requirements.txt --break-system-packages
pip3 install -U "discord.py[voice]" --break-system-packages
chmod +x runBot.sh
