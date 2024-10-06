import psycopg2
from psycopg2 import extras
import configparser

class DbManager:
    def __init__(self, config_file='config.ini') -> None:
        """Initialize the DbManager instance and load the configuration."""
        self.config_file = config_file
        self.connection = None
        self.cursor = None
        self._load_config()

    def _load_config(self):
        """Load database configuration from the config.ini file."""
        config = configparser.ConfigParser()
        config.read(self.config_file)
        
        self.dbname = config['database']['dbname']
        self.user = config['database']['user']
        self.password = config['database']['password']
        self.host = config['database']['host']

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