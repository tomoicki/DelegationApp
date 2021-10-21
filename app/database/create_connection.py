from sqlalchemy.orm import sessionmaker
from os import environ as env
from dotenv import load_dotenv
from app.database.connection_functions import connection_to_db

load_dotenv()
connection_dictionary = {'host': env['POSTGRE_SQL_HOST'],
                         'port': env['POSTGRE_SQL_PORT'],
                         'user': env['POSTGRE_SQL_USER'],
                         'password': env['POSTGRE_SQL_PASSWORD'],
                         'db_name': env['POSTGRE_SQL_DB_NAME']}

#  make connection with PostgreSQL
postgre_connection = connection_to_db(**connection_dictionary)
postgre_session = sessionmaker(bind=postgre_connection)
sqlalchemy_session = postgre_session()
