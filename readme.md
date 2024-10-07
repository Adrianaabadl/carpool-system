# BlablaCar Case Study

Start creating a virtual environment
```bash
python3.10 -m venv ~/carpool-system
source ~/carpool-system/bin/activate 
pip install -r requirements.txt
```

Start your postgres instance
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
```

Connect to the postgres default user
```bash
sudo -i -u postgres
psql
```

Create your database, username and grant access
```bash
CREATE USER blablacar WITH PASSWORD 'adminblablacar';
CREATE DATABASE blablacar_engine;
GRANT USAGE, CREATE ON SCHEMA public TO blablacar;
ALTER ROLE blablacar SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE blablacar_engine TO blablacar;
ALTER USER blablacar WITH SUPERUSER;
```

Hint: Avoid Peer authentication failed for user blablacar
```bash
sudo nano /etc/postgresql/16/main/pg_hba.conf
local   all             all                                     md5 # change this line (change peer to md5)
sudo systemctl restart postgresql # restart your postgres instance
```

Connect to postgres with your user
```bash
psql -U blablacar -d blablacar_engine
```


## Enable bigquery Project

Authenticate
```bash
gcloud init
```

Enable billing
```bash
gcloud auth application-default login
```

```bash
```


## Some considerations

Your working directory or python path shoud be "${workspaceFolder}/src"