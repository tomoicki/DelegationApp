import enum
import datetime
from flask import request
from functools import wraps
from sqlalchemy import Column, LargeBinary, Integer, String, ForeignKey, Date, Float, Time, Enum, Boolean, DateTime, \
    update
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from app.database.create_connection import sqlalchemy_session


class Base:
    def delete(self):
        sqlalchemy_session.delete(self)
        sqlalchemy_session.commit()

    @classmethod
    def get_by_id(cls, provided_id: int):
        if provided_id is not None and provided_id != 'None':
            return sqlalchemy_session.get(cls, provided_id)


Base = declarative_base(cls=Base)


class DelegationStatusOptions(enum.Enum):
    submitted = 'submitted'
    approved_by_manager = 'approved_by_manager'
    settled = 'settled'
    rejected = 'rejected'


class DelegationStatus(Base):
    __tablename__ = 'DelegationStatus'
    # fields
    id = Column(Integer, primary_key=True)
    status = Column(Enum(DelegationStatusOptions))
    reason = Column(String)
    # one to many
    delegation_id = Column(Integer, ForeignKey('Delegation.id', ondelete="CASCADE"))


class Delegation(Base):
    __tablename__ = 'Delegation'
    # fields
    id = Column(Integer, primary_key=True)
    title = Column(String)
    submit_date = Column(DateTime)
    departure_date = Column(Date)
    arrival_date = Column(Date)
    reason = Column(String)
    remarks = Column(String)
    # one to many
    delegate_id = Column(Integer, ForeignKey('User.id'))
    delegate = relationship('User',
                            backref=backref('delegation_his'),
                            primaryjoin='foreign(Delegation.delegate_id) == remote(User.id)')
    creator_id = Column(Integer, ForeignKey('User.id'))
    creator = relationship('User',
                           backref=backref('delegation_creator'),
                           primaryjoin='foreign(Delegation.creator_id) == remote(User.id)')
    approver_id = Column(Integer, ForeignKey('User.id'))
    approver = relationship('User',
                            backref=backref('delegation_approver'),
                            primaryjoin='foreign(Delegation.approver_id) == remote(User.id)')
    country_id = Column(Integer, ForeignKey('Country.id'))
    # many to one
    advance_payment = relationship('AdvancePayment', backref='delegation', cascade="all,delete")
    settlement = relationship('Settlement', backref='delegation')
    status = relationship('DelegationStatus', backref='delegation', cascade="all,delete")

    def current_status(self):
        return self.status[-1].status.value

    def change_status(self, changed_status: str, reason: str):
        if changed_status in [enum_option.value for enum_option in DelegationStatusOptions]:
            if self.current_status() != changed_status:
                new_status = DelegationStatus(delegation_id=self.id,
                                              status=changed_status,
                                              reason=reason)
                sqlalchemy_session.add(new_status)
                sqlalchemy_session.commit()

    def show(self):
        delegation_to_show = {"id": self.id,
                              "title": self.title,
                              "reason": self.reason,
                              "departure date": self.departure_date,
                              "arrival date": self.arrival_date,
                              "departure point": Country.get_by_id(self.country_id).name,
                              "status": self.current_status()}
        return delegation_to_show

    def details(self):
        dicted = self.__dict__
        if '_sa_instance_state' in dicted:
            del dicted['_sa_instance_state']
        dicted = {key.replace('country_id', 'country'): (Country.get_by_id(value).name if 'country' in key else value)
                  for key, value in dicted.items()}
        dicted = {key: (str(User.get_by_id(value)) if '_id' in key else value)
                  for key, value in dicted.items()}
        dicted = {(key.replace('_id', '') if '_id' in key else key): value for key, value in dicted.items()}
        return dicted

    def modify(self, modifications_dict: dict):
        stmt = update(Delegation).where(Delegation.id == self.id).values(**modifications_dict)
        sqlalchemy_session.execute(stmt)
        sqlalchemy_session.commit()

    @classmethod
    def create(cls, delegation_details: dict):
        delegation_details['departure_date'] = datetime.date.fromisoformat(delegation_details['departure_date'])
        delegation_details['arrival_date'] = datetime.date.fromisoformat(delegation_details['arrival_date'])
        delegation_details['submit_date'] = datetime.datetime.now()
        advance_payments = delegation_details['advance_payments']
        del delegation_details['advance_payments']
        delegation = Delegation(**delegation_details)
        sqlalchemy_session.add(delegation)
        sqlalchemy_session.commit()
        entry_status = DelegationStatus(delegation_id=delegation.id,
                                        status=DelegationStatusOptions.submitted.value,
                                        reason='Delegation creation.')
        sqlalchemy_session.add(entry_status)
        sqlalchemy_session.commit()
        for advance_payment in advance_payments:
            advance_payment['delegation_id'] = delegation.id
            AdvancePayment.create(advance_payment)
        return delegation

    @classmethod
    def if_exists(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if cls.get_by_id(kwargs['delegation_id']) is not None:
                return func(*args, **kwargs)
            return {'response': "Cannot find delegation with provided ID."}, 404

        return wrapper


class Role(enum.Enum):
    user = 'user'
    manager = 'manager'
    hr = 'hr'
    admin = 'admin'


class User(Base):
    __tablename__ = 'User'
    # fields
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(Enum(Role))
    is_active = Column(Boolean)
    token = Column(String, unique=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def modify(self, modifications_dict: dict):
        stmt = update(User).where(User.id == self.id).values(**modifications_dict)
        sqlalchemy_session.execute(stmt)
        sqlalchemy_session.commit()

    def show(self):
        user_dicted = self.__dict__
        user_dicted = {key: value for key, value in user_dicted.items()
                       if key not in ['_sa_instance_state', 'token', 'password', 'role']}
        user_dicted['role'] = self.role.value
        return user_dicted

    def is_authorized(self, delegation: Delegation):
        if self.id == delegation.delegate_id or self.role.value in ['manager', 'hr', 'admin']:
            return True
        return False

    @classmethod
    def get_by_token(cls, provided_token: str):
        return sqlalchemy_session.query(cls).filter(cls.token == provided_token).first()

    @classmethod
    def get_by_email(cls, provided_email: str):
        return sqlalchemy_session.query(cls).filter(cls.email == provided_email).first()

    @classmethod
    def is_logged_in(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if cls.get_by_token(request.headers.get('token')) is not None:
                return func(*args, **kwargs)
            return "You are not logged in.", 401

        return wrapper


class AdvancePayment(Base):
    __tablename__ = 'AdvancePayment'
    # fields
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    # one to many
    delegation_id = Column(Integer, ForeignKey('Delegation.id', ondelete="CASCADE"))
    currency_id = Column(Integer, ForeignKey('Currency.id'))

    @classmethod
    def create(cls, advance_payment_details: dict):
        advance_payment = Attachment(**advance_payment_details)
        sqlalchemy_session.add(advance_payment)
        sqlalchemy_session.commit()


class Country(Base):
    __tablename__ = 'Country'
    # fields
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    diet = Column(Float)
    accommodation_limit = Column(Float)
    # one to many
    currency_id = Column(Integer, ForeignKey('Currency.id'))
    # many to one
    delegation = relationship("Delegation", backref='country')


class Currency(Base):
    __tablename__ = 'Currency'
    # fields
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    # many to one
    country = relationship("Country", backref='currency')
    advance_payment = relationship("AdvancePayment", backref='currency')
    expense = relationship("Expense", backref='currency')


class SettlementStatusOptions(enum.Enum):
    submitted = 'submitted'
    approved_by_manager = 'approved_by_manager'
    denied_by_manager = 'denied_by_manager'
    approved_by_hr = 'approved_by_hr'
    denied_by_hr = 'denied_by_hr'
    closed = 'closed'


class SettlementStatus(Base):
    __tablename__ = 'SettlementStatus'
    # fields
    id = Column(Integer, primary_key=True)
    status = Column(Enum(SettlementStatusOptions))
    reason = Column(String)
    # one to many
    settlement_id = Column(Integer, ForeignKey('Settlement.id', ondelete="CASCADE"))


class Settlement(Base):
    __tablename__ = 'Settlement'
    # fields
    id = Column(Integer, primary_key=True)
    submit_date = Column(DateTime)
    departure_date = Column(Date)
    departure_time = Column(Time)
    arrival_date = Column(Date)
    arrival_time = Column(Time)
    diet = Column(Float)
    # one to many
    delegation_id = Column(Integer, ForeignKey('Delegation.id'))
    approver_id = Column(Integer, ForeignKey('User.id'))
    approver = relationship('User',
                            backref=backref('settlement_approver'),
                            primaryjoin='foreign(Settlement.approver_id) == remote(User.id)')
    # many to one
    expense = relationship('Expense', backref='settlement', cascade="all,delete")
    meal = relationship('Meal', backref='settlement', cascade="all,delete")
    status = relationship('SettlementStatus', backref='settlement', cascade="all,delete")

    def current_status(self):
        return self.status[-1].status.value

    def change_status(self, changed_status: str, reason: str):
        if changed_status in [enum_option.value for enum_option in SettlementStatusOptions]:
            if self.current_status() != changed_status:
                new_status = SettlementStatus(settlement_id=self.id,
                                              status=changed_status,
                                              reason=reason)
                sqlalchemy_session.add(new_status)
                sqlalchemy_session.commit()

    def show(self):
        settlement_to_show = {'id': self.id,
                              'submit_date': self.submit_date}
        return settlement_to_show

    def details(self):
        dicted = self.__dict__
        dicted = {key: (value.isoformat() if '_time' in key else value) for key, value in dicted.items()}
        dicted2 = dicted.copy()
        for key in dicted.keys():
            if '_sa_instance_state' in key:
                del dicted2[key]
        return dicted2

    def modify(self, modifications_dict: dict):
        stmt = update(Settlement).where(Settlement.id == self.id).values(**modifications_dict)
        sqlalchemy_session.execute(stmt)
        sqlalchemy_session.commit()

    @classmethod
    def create(cls, settlement_details: dict):
        settlement_details['submit_date'] = datetime.datetime.now()
        expenses = settlement_details['expenses']
        del settlement_details['expenses']
        meals = settlement_details['meals']
        del settlement_details['meals']
        settlement = Settlement(**settlement_details)
        sqlalchemy_session.add(settlement)
        sqlalchemy_session.commit()
        entry_status = SettlementStatus(settlement_id=settlement.id,
                                        status=SettlementStatusOptions.submitted.value,
                                        reason='Settlement creation.')
        sqlalchemy_session.add(entry_status)
        sqlalchemy_session.commit()
        for meal in meals:
            meal['settlement_id'] = settlement.id
            Expense.create(meal)
        for expense in expenses:
            expense['settlement_id'] = settlement.id
            Expense.create(expense)
        return settlement

    @classmethod
    def if_exists(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if cls.get_by_id(kwargs['settlement_id']) is not None:
                return func(*args, **kwargs)
            return {'response': "Cannot find settlement with provided ID."}, 404
        return wrapper

    @classmethod
    def is_correct_child(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            settlement = cls.get_by_id(kwargs['settlement_id'])
            delegation = Delegation.get_by_id(kwargs['delegation_id'])
            if settlement in delegation.settlement:
                return func(*args, **kwargs)
            return {'response': 'Provided settlement is not a child of provided delegation.'}, 404
        return wrapper


class MealType(enum.Enum):
    breakfast = 'breakfast'
    lunch = 'lunch'
    supper = 'supper'


class Meal(Base):
    __tablename__ = 'Meal'
    # fields
    id = Column(Integer, primary_key=True)
    type = Column(Enum(MealType))
    # one to many
    settlement_id = Column(Integer, ForeignKey('Settlement.id', ondelete="CASCADE"))

    @classmethod
    def create(cls, meal_details: dict):
        meal = Meal(**meal_details)
        sqlalchemy_session.add(meal)
        sqlalchemy_session.commit()


class ExpenseType(enum.Enum):
    accommodation = 'accommodation'
    transit = 'transit'
    drive = 'drive'
    other = 'other'


class Expense(Base):
    __tablename__ = 'Expense'
    # fields
    id = Column(Integer, primary_key=True)
    type = Column(Enum(ExpenseType))
    amount = Column(Float)
    description = Column(String)
    # one to many
    settlement_id = Column(Integer, ForeignKey('Settlement.id', ondelete="CASCADE"))
    currency_id = Column(Integer, ForeignKey('Currency.id'))
    # many to one
    attachment = relationship('Attachment', backref='expense', cascade="all,delete")

    def show(self):
        expense_dicted = self.__dict__
        expense_dicted = {key: value for key, value in expense_dicted.items()
                          if key not in ['_sa_instance_state', 'token', 'password', 'type']}
        expense_dicted['type'] = self.type.value
        expense_dicted = {
            key.replace('currency_id', 'currency'): (Currency.get_by_id(value).name if 'currency' in key else value)
            for key, value in expense_dicted.items()}
        return expense_dicted

    @classmethod
    def create(cls, expense_details: dict):
        attachments = expense_details['attachments']
        del expense_details['attachments']
        expense = Expense(**expense_details)
        sqlalchemy_session.add(expense)
        sqlalchemy_session.commit()
        for attachment in attachments:
            attachment['expense_id'] = expense.id
            Attachment.create(attachment)

    @classmethod
    def if_exists(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if cls.get_by_id(kwargs['expense_id']) is not None:
                return func(*args, **kwargs)
            return {'response': "Cannot find expense with provided ID."}, 404
        return wrapper

    @classmethod
    def is_correct_child(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            expense = cls.get_by_id(kwargs['expense_id'])
            settlement = Settlement.get_by_id(kwargs['settlement_id'])
            if expense in settlement.expense:
                return func(*args, **kwargs)
            return {'response': 'Provided settlement is not a child of provided delegation.'}, 404
        return wrapper


class Attachment(Base):
    __tablename__ = 'Attachment'
    # fields
    id = Column(Integer, primary_key=True)
    file = Column(String)
    # one to many
    expense_id = Column(Integer, ForeignKey('Expense.id', ondelete="CASCADE"))

    @classmethod
    def create(cls, attachment_details: dict):
        attachment = Attachment(**attachment_details)
        sqlalchemy_session.add(attachment)
        sqlalchemy_session.commit()

