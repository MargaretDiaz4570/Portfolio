#!/bin/bash

# Kill all existing tmux sessions
tmux kill-session -a

# Change directory to your project folder
cd /mnt/c/Users/marga/Desktop/MLH_FELLOW/Portfolio

# Update the git repository with the latest changes from the main branch on GitHub
git fetch && git reset origin/main --hard

# Enter the python virtual environment and install dependencies
source /mnt/c/Users/marga/Desktop/MLH_FELLOW/python3-virtualenv/
pip install -r requirements.txt

# Start a new detached Tmux session and run the Flask server
tmux new-session -d -s flask-session 'cd /mnt/c/Users/marga/Desktop/MLH_FELLOW/Portfolio
 && source /mnt/c/Users/marga/Desktop/MLH_FELLOW/python3-virtualenv/ && flask run'