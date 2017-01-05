# use virtual python environment
source venv/bin/activate

# update project
git pull origin master

# update python environment and install new module
pip install -r requirements.txt

# restart and update database
sudo service mongod restart
python TourismWebsite/database/initialize.py

# restart server
kill `cat rocket.pid`
cd TourismWebsite/
gunicorn -c ../deploy_config.py TourismWebsite:app -p rocket.pid -D

