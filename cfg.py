import os

DB_HOST = os.environ.get('POSTGRES_HOST')

# Stream types
LOCAL_STREAM = 0
REMOTE_STREAM = 1

# postgresql database connection string
connection_string = f"postgresql://postgres:postgres@{DB_HOST}:5432/postgres"
