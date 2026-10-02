import os
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv("SECRET.env")

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f"dbname='{DB_NAME}' user='{DB_USER}' password='{DB_PASS}' host='{DB_HOST}' port='{DB_PORT}'"
#host.docker.internal

# Создаем пул соединений
connection_pool = pool.SimpleConnectionPool(1, 20, DATABASE_URL)

def get_connection():
    return connection_pool.getconn()

def release_connection(connection):
    connection_pool.putconn(connection)
