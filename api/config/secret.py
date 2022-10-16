import os

db_password = os.getenv('DB_PASSWORD')
db_database = os.getenv('DB_DATABASE')

host_args = {
    "host": "db",
    "user": "root",
    "password": db_password,
    "database": db_database
}