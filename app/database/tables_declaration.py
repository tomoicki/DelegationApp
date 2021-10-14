from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Time
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import shortuuid
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
    user_email = Column(String, ForeignKey('User.email'))
    to_user = relationship("User", back_populates='to_delegation')

    def __str__(self):
        dicted = self.__dict__
        print(dicted)
        if '_sa_instance_state' in dicted:
            del dicted['_sa_instance_state']
        return str(dicted)

