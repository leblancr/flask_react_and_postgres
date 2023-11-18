youtube - Full Stack Flask, React, and Postgres, pt. 1

1. set up system
2. get user to be able to log into database using psql
3. create Event table by: db.create_all()
4. send get reuest to http://localhost:5000/events using postman.


1. set up system:
<!-- pyenv local 3.10.10 -->
<!-- pyenv virtualenv 3.10.10 flask_react_and_postgres - just first time to create venv -->
<!-- pyenv activate flask_react_and_postgres -->
<!-- export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring -->
<!-- python -m keyring --disable -->

poetry install
poetry shell for virtual environment

systems:
sudo service postgresql start - to start postgres service
service postgresql status

OpenRC gentoo, if not started automaticlly at startup:
sudo /etc/init.d/postgresql-15 start
* /run/postgresql: creating directory
* /run/postgresql: correcting owner
* Starting PostgreSQL 15 ...
sudo /etc/init.d/postgresql-15 stop

2. get user to be able to log into database using psql
sudo pg_isready
sudo -u postgres psql - login to postgres using the default postgres role. password = ?
gets to the postgres=# prompt, then...
CREATE DATABASE database;
GRANT ALL PRIVILEGES ON DATABASE database to rich;
ALTER USER rich WITH SUPERUSER;

Password for user postgres: r***pos, rich: r***pos
psql -U rich -d baby-tracker - logs rich into database baby-tracker

baby-tracker=# ALTER USER rich WITH PASSWORD 'admin';
baby-tracker=# GRANT ALL PRIVILEGES ON DATABASE "baby-tracker" to rich;
baby-tracker=# \conninfo
You are connected to database "baby-tracker" as user "rich" via socket in "/var/run/postgresql" at port "5432".

to start: /flask_react_and_postgres/backend/ python -m flask run
to run pgadmin4 type it in a terminal - rkba001 Q223@
/home/rich/.pyenv/versions/3.10.10/envs/flask_react_and_postgres/lib/python3.10/site-packages/
nano my_env/lib/python3.10/site-packages/pgadmin4/config_local.py

3. create Event table by: db.create_all()
# run just once to create event table in Event class
# with app.app_context():
#     db.create_all()

Errors:
ImportError: cannot import name 'MethodViewType' from 'flask.views'
reinstalled with  python -m pip install pgadmin4, make sure in venv

/home/rich/.pyenv/versions/3.10.10/bin/python3: No module named flask
make sure venv activated

ModuleNotFoundError: No module named mod name
put python -m in front
    
Error: Could not locate a Flask application. You did not provide the "FLASK_APP" environment variable, and a "wsgi.py" or "app.py" module was not found in the current directory.
get in the backend directory

in python -m flask shell:
>>> from app import db
>>> db.create_all() 

TypeError: Rule.__init__() got an unexpected keyword argument 'method'
Need 's' after method - methods=['POST'])

Address already in use
Port 5000 is in use by another program.
lsof -i:5000
kill -9 <pid>
   
bash: pgadmin: command not found
type pgadmin4

{eventsList.map(event => {
   return (
   <li key={event.id}>{event.description}</li>
   )
})}

connection to server on socket "/run/postgresql/.s.PGSQL.5432" failed:
FATAL:  password authentication failed for user "rich"

Caused by special character in pass word, '@'. Need to encode, use %40 instead.
