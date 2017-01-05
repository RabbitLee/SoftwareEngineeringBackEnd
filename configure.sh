# update project
git pull origin master

# restart database
sudo service mongod restart

# update python environment and install new module
source venv/bin/activate
pip install -r requirements.txt

