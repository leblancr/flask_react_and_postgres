youtube - Full Stack Flask, React, and Postgres, pt. 1

1. set up system
2. get user to be able to log into database using psql
3. create Event table by: db.create_all()
4. send get request to http://localhost:5000/events using postman.


1. set up system:
gentoo:
sudo emerge --ask dev-db/postgresql
sudo passwd postgres  # set it to 'postgres'
sudo chown -R postgres:postgres /var/lib/postgresql/16  
sudo chown -R postgres:postgres /var/lib/postgresql/data
# sudo mv /var/lib/postgresql/16/data/pg*.conf /etc/postgresql-16/ - didn't work for some reason
sudo mv /var/lib/postgresql/16/data/postgresql.conf /etc/postgresql-16/
sudo mv /var/lib/postgresql/16/data/pg_hba.conf /etc/postgresql-16/
sudo mv /var/lib/postgresql/16/data/pg_ident.conf /etc/postgresql-16/
sudo -u postgres initdb -D /var/lib/postgresql/16/data     

# This command will give full access to the directory to the owner
# (rich in this case) and no access to others.
# Add the user rich to the postgres group:
sudo usermod -aG postgres rich

Initialize the Database:
After installation, you need to initialize the database cluster. 
This is typically done using the initdb command. Run:
sudo su - postgres - enter users creds
initdb --locale=en_US.UTF-8 -D '/var/lib/postgresql/data'
poetry install
poetry shell for virtual environment
may need to update some dependencies if it's been a while.

systems:
freebsd
sudo service postgresql start - to start postgres service
service postgresql status

OpenRC gentoo, if not started automaticlly at startup:
sudo /etc/init.d/postgresql-16 start
* /run/postgresql: creating directory
* /run/postgresql: correcting owner
* Starting PostgreSQL 16 ...
sudo /etc/init.d/postgresql-16 stop

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

Restoring database on a new system from backup.sql:
psql -U postgres -d postgres -h localhost                                2 ↵ ──(Fri,Jun07)─┘
psql (16.3)
Type "help" for help.

postgres=# CREATE DATABASE baby_tracker;
You are now connected to database "baby_tracker" as user "postgres".
baby_tracker-# psql -U postgres -d baby_tracker -h localhost -f backup.sql
baby_tracker-# \q
psql -U postgres -d baby_tracker -h localhost -f backup.sql

3. create Event table by: db.create_all()
# run just once to create event table in Event class
# with app.app_context():
#     db.create_all()

4. 

Starting after setup:
1. Start database - Postgres
Gentoo: 
sudo pg_isready
sudo /etc/init.d/postgresql-16 start
to run dbeaver type ./dbeaver in the extracted directory in a terminal 
/opt/dbeaver/dbeaver
in dbeaver create new connection for rich besides the postgres one

FreeBSD:
to run pgadmin4 type it in a terminal - rkba001 Q223@

2. Start backend:
cd /flask_react_and_postgres/backend/
poetry shell
python -m flask run

3. Start frontend:
cd /flask_react_and_postgres/frontend
npm start

there's a README.md in the frontend directory
/home/rich/.pyenv/versions/3.10.10/envs/flask_react_and_postgres/lib/python3.10/site-packages/
nano my_env/lib/python3.10/site-packages/pgadmin4/config_local.py

Troubleshooting:
Postgres:
/run/postgresql:5432 - no response
rc-service postgresql status

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
