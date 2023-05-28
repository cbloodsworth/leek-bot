#!/bin/bash
# Shell script to set the development environment up for the leetcode discord bot.

# For Linux

# Create a virtual environment in this folder
python3 -m venv venv

# Activate said virtual environment (this step will need to be done every time you restart the shell)
. ./venv/bin/activate

# Install the requirements in the virtual environment we created
pip install -r requirements.txt

# Everything ran as planned
echo "Environment successfully set up. Use the following to start up the bot: "
echo "\$ python3 src/bot.py"
