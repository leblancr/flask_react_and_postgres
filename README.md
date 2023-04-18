youtube - Full Stack Flask, React, and Postgres, pt. 1

setup:
pyenv local 3.10.10
pyenv virtualenv 3.10.10 flask_react_and_postgres - just first time to create venv
pyenv activate flask_react_and_postgres
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
python -m keyring --disable
poetry install

to start: /flask_react_and_postgres/backend/ python -m flask run
to run pgadmin4 type it in a terminal - rkba001 Q223@
/home/rich/.pyenv/versions/3.10.10/envs/flask_react_and_postgres/lib/python3.10/site-packages/
nano my_env/lib/python3.10/site-packages/pgadmin4/config_local.py
sudo service postgresql start - to start postgres service
service postgresql status
sudo pg_isready
sudo -u postgres psql - login to postgres using the default postgres role.
gets to the postgres=# prompt, then...
CREATE USER rich WITH PASSWORD 'reddposQ223@';
CREATE DATABASE database;
GRANT ALL PRIVILEGES ON DATABASE database to rich;
ALTER USER rich WITH SUPERUSER;
baby-tracker=# ALTER USER rich WITH PASSWORD 'admin';
baby-tracker=# GRANT ALL PRIVILEGES ON DATABASE "baby-tracker" to rich;
baby-tracker=# \conninfo
You are connected to database "baby-tracker" as user "rich" via socket in "/var/run/postgresql" at port "5432".

github token
black - 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
new1  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


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

