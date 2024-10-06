import psycopg2
from pathlib import Path
import configparser

config = configparser.ConfigParser()

def initialize_database():
    ddl_file = Path('/home/adriana/Documents/personal/blablacar/src/infrastructure/ddl/create_ddls.sql')
    config.read('config.ini')
    db_config = config['database']
    dbname = db_config['dbname']
    user = db_config['user']
    password = db_config['password']
    host = db_config['host']
    
    with psycopg2.connect(dbname=dbname, user=user, password=password, host=host) as conn:
        with conn.cursor() as cursor, ddl_file.open() as f:
            ddl_script = f.read()
            cursor.execute(ddl_script)
            conn.commit()

if __name__ == "__main__":
    initialize_database()
