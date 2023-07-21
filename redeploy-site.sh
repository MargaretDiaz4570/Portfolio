#!/bin/bash
# cd ~/.ssh/
# ssh -i ~/.ssh/MLHprivate.pem root@165.22.178.151
# Change directory to your project folder
cd Portfolio

# Update the git repository with the latest changes from the main branch on GitHub
git fetch && git reset origin/main --hard

# Enter the python virtual environment and install dependencies
source python3-virtualenv/bin/activate
pip install -r requirements.txt

# Restart myportfolio service
sudo systemctl daemon-reload
sudo systemctl restart myportfolio
systemctl status myportfolio