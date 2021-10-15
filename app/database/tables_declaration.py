import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Time, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class Role(enum.Enum):
    user = 'user'
    accountant = 'accountant'
    admin = 'admin'


# main Tables
class User(Base):
    __tablename__ = 'User'
    # fields
    id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(Enum(Role))
    is_active = Column(Boolean)
    token = Column(String)
    # many to one
    # worker_to_delegation = relationship("Delegation", back_populates='to_worker')
    # maker_to_delegation = relationship("Delegation", back_populates='to_maker')
    # approver_to_delegation = relationship("Delegation", back_populates='to_approver')


class Delegation(Base):
    __tablename__ = 'Delegation'
    # fields
    id = Column(String, primary_key=True)
    title = Column(String)
    submit_date = Column(DateTime)
    departure_date = Column(Date)
    departure_time = Column(Time)
    arrival_date = Column(Date)
    arrival_time = Column(Time)
    reason = Column(String)
    remarks = Column(String)
    diet = Column(Float)
    # one to many
    worker_id = Column(String, ForeignKey('User.id'))
    # to_worker = relationship("User", foreign_keys=[worker_id])
    maker_id = Column(String, ForeignKey('User.id'))
    # to_maker = relationship("User", foreign_keys=[maker_id])
    approved_by_id = Column(String, ForeignKey('User.id'))
    # to_approver = relationship("User", foreign_keys=[approved_by_id])
    country_id = Column(String, ForeignKey('Country.id'))
    # to_country = relationship('Country', back_populates='to_delegation')
    # many to one
    # to_expense = relationship('Expense', back_populates='to_delegation')
    # to_advance_payment = relationship('AdvancePayment', back_populates='to_delegation')

    def __str__(self):
        dicted = self.__dict__
        if '_sa_instance_state' in dicted:
            del dicted['_sa_instance_state']
        return str(dicted)


class AdvancePayment(Base):
    __tablename__ = 'AdvancePayment'
    # fields
    id = Column(String, primary_key=True)
    amount = Column(Float)
    # one to many
    delegation_id = Column(String, ForeignKey('Delegation.id'))
    # to_delegation = relationship("Delegation", back_populates='to_advance_payment')
    currency_id = Column(String, ForeignKey('Currency.id'))
    # to_currency = relationship("Currency", back_populates='to_advance_payment')


class Currency(Base):
    __tablename__ = 'Currency'
    # fields
    id = Column(String, primary_key=True)
    name = Column(String)
    # many to one
    # to_advance_payment = relationship("AdvancePayment", back_populates='to_currency')
    # to_expense = relationship("Expense", back_populates='to_currency')
    # to_country = relationship("Country", back_populates='to_currency')


class ExpenseType(enum.Enum):
    accommodation = 'accommodation'
    transit = 'transit'
    drive = 'drive'
    other = 'other'


class Expense(Base):
    __tablename__ = 'Expense'
    # fields
    id = Column(String, primary_key=True)
    type = Column(Enum(ExpenseType))
    amount = Column(Float)
    description = Column(String)
    # one to many
    delegation_id = Column(String, ForeignKey('Delegation.id'))
    # to_delegation = relationship("Delegation", back_populates='to_expense')
    currency_id = Column(String, ForeignKey('Currency.id'))
    # to_currency = relationship("Currency", back_populates='to_expense')


class Country(Base):
    __tablename__ = 'Country'
    # fields
    id = Column(String, primary_key=True)
    name = Column(String)
    # one to many
    currency_id = Column(String, ForeignKey('Currency.id'))
    # to_currency = relationship("Currency", back_populates='to_country')
    # many to one
    # to_delegation = relationship("Delegation", back_populates='to_country')


class Settlement(Base):
    __tablename__ = 'Settlement'
    # fields
    id = Column(String, primary_key=True)
    delegation_id = Column(String, ForeignKey('Delegation.id'))
    approver_id = Column(String, ForeignKey('User.id'))
    date = Column(DateTime)


class MealType(enum.Enum):
    breakfast = 'breakfast'
    lunch = 'lunch'
    supper = 'supper'


class Meal(Base):
    __tablename__ = 'Meal'
    # fields
    id = Column(String, primary_key=True)
    type = Column(Enum(MealType))
    delegation_id = Column(String, ForeignKey('Delegation.id'))




