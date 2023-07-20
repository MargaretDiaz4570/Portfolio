#!/bin/bash

# Kill all existing tmux sessions
tmux kill-session -a

# Change directory to your project folder
cd Portfolio

# Update the git repository with the latest changes from the main branch on GitHub
git fetch && git reset origin/main --hard

# Enter the python virtual environment and install dependencies
source python3-virtualenv/bin/activate
pip install -r requirements.txt

# Start a new detached Tmux session and run the Flask server
# Make sure to run the Flask server on the VPS IP address!