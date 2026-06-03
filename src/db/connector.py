from mysql import connector

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "root",
    "password": "",
    "database": "dem_database",
}

def get_connection():
    return connector.connect(**DB_CONFIG)
