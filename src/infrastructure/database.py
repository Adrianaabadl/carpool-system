import psycopg2
from psycopg2 import extras
import yaml

class DbManager:
    def __init__(self, config_file='config.yml') -> None:
        """Initialize the DbManager instance and load the configuration."""
        self.config_file = config_file
        self.connection = None
        self.cursor = None
        self._load_config()

    def _load_config(self):
        """Load database configuration from the config.yml file."""
        with open(self.config_file, 'r') as file:
            config = yaml.safe_load(file)
        
        db_config = config['database']
        self.dbname = db_config['dbname']
        self.user = db_config['user']
        self.password = db_config['password']
        self.host = db_config['host']

    def _create_connection(self):
        """Create a connection to the PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host
            )
            self.cursor = self.connection.cursor(cursor_factory=extras.DictCursor)  # Returns results as a dictionary
            print("Database connection established successfully.")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise

    def _execute_query(self, query, values=None):
        """Execute a SQL query and manage the transaction."""
        try:
            if not self.connection:
                self._create_connection()

            self.cursor.execute(query, values)
            self.connection.commit()
            print("Query executed successfully.")
        except psycopg2.IntegrityError as e:
            print(f"Duplicate key error: {e}")
            self.connection.rollback()
            pass
        except Exception as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            raise
    
    def _close_connection(self):
        """Close the connection and cursor to the database."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed.")
