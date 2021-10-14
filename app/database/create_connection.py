from sqlalchemy.orm import sessionmaker
from os import environ as env
from dotenv import load_dotenv
from app.database.connection_functions import connection_to_db

load_dotenv()
connection_dictionary = {'host': env['PostgreSQL_host'],
                         'port': env['PostgreSQL_port'],
                         'user': env['PostgreSQL_user'],
                         'password': env['PostgreSQL_password'],
                         'db_name': env['PostgreSQL_db_name']}

#  make connection with PostgreSQL
postgre_connection = connection_to_db(**connection_dictionary)
postgre_session = sessionmaker(bind=postgre_connection)
sqlalchemy_session = postgre_session()
