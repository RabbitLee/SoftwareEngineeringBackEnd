# use virtual python environment
source venv/bin/activate

# update project
git pull origin master

# restart and update database
sudo service mongod restart
python TourismWebsite/database/initialize.py

# update python environment and install new module
pip install -r requirements.txt

