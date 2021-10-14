from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Time
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database.connection_functions import connection_to_db
from os import environ as env
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


#  main Tables
class User(Base):
    __tablename__ = 'User'
    #  fields
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, primary_key=True)
    password = Column(String)
    access_level = Column(Integer)
    token = Column(String)
    #  many to one
    delegation_id = Column(String, ForeignKey('Delegation.id'))
    to_delegation = relationship("Delegation", back_populates='to_user')


class Delegation(Base):
    __tablename__ = 'Delegation'
    #  fields
    id = Column(String, primary_key=True)
    title = Column(String)
    submit_date = Column(Date)
    departure_date = Column(Date)
    departure_time = Column(Time)
    arrival_date = Column(Date)
    arrival_time = Column(Time)
    destination = Column(String)
    reason = Column(String)
    approved_by = Column(String)
    advance_payment = Column(Float)
    # one to many
    to_user = relationship("User", back_populates='to_delegation')


#  create connection with DB
# cnx = connection2db(env['PostgreSQL_host'],
#                     env['PostgreSQL_port'],
#                     env['PostgreSQL_user'],
#                     env['PostgreSQL_password'],
#                     env['PostgreSQL_db_name'])
#
# #  create all declared tables inside DB
# Base.metadata.create_all(cnx)
# #  create session
# session = sessionmaker(bind=cnx)
# session = session()
# user1 = User()
# user1.email = 'usr@itechart.com'
# session.add(user1)
# session.commit()
