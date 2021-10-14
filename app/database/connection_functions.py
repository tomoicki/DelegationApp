import sqlalchemy.engine
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


def connection_to_db(host: str, port: str, user: str, password: str, db_name: str) -> sqlalchemy.engine.base.Engine:
    """Makes a connection to PostgreSQL DB."""
    try:
        postgres_str = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
        cnx = create_engine(postgres_str)
        cnx.connect()
    except OperationalError as e:
        cnx = None
    return cnx

