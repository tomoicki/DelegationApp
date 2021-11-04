import enum
import datetime
from flask import request
from functools import wraps
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Time, Enum, Boolean, DateTime, update
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
    settlement = relationship("Settlement", backref='country')


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
    approved = 'approved'
    denied = 'denied'
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
    title = Column(String)
    submit_date = Column(DateTime)
    departure_date = Column(Date, nullable=False)
    departure_time = Column(Time, nullable=False)
    arrival_date = Column(Date, nullable=False)
    arrival_time = Column(Time, nullable=False)
    reason = Column(String)
    remarks = Column(String)
    # one to many
    delegate_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    delegate = relationship('User',
                            backref=backref('settlement_his'),
                            primaryjoin='foreign(Settlement.delegate_id) == remote(User.id)')
    creator_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    creator = relationship('User',
                           backref=backref('creator'),
                           primaryjoin='foreign(Settlement.creator_id) == remote(User.id)')
    approver_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    approver = relationship('User',
                            backref=backref('approver'),
                            primaryjoin='foreign(Settlement.approver_id) == remote(User.id)')
    country_id = Column(Integer, ForeignKey('Country.id'), nullable=False)
    # many to one
    advance_payment = relationship('AdvancePayment', backref='settlement', cascade="all,delete")
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
        settlement_with_details = {'id': self.id,
                                   'approver': str(User.get_by_id(self.approver_id)),
                                   'submit_date': self.submit_date,
                                   'departure_date': self.departure_date,
                                   'departure_time': self.departure_time.isoformat(),
                                   'arrival_date': self.arrival_date,
                                   'arrival_time': self.arrival_time.isoformat(),
                                   'delegation_id': self.delegation_id,
                                   'diet': self.diet}
        return settlement_with_details

    def modify(self, modifications_dict: dict):
        modifications_dict['submit_date'] = datetime.datetime.now()
        stmt = update(Settlement).where(Settlement.id == self.id).values(**modifications_dict)
        sqlalchemy_session.execute(stmt)
        sqlalchemy_session.commit()

    @classmethod
    def create(cls, settlement_details: dict):
        settlement_details['submit_date'] = datetime.datetime.now()
        settlement = Settlement(**settlement_details)
        sqlalchemy_session.add(settlement)
        sqlalchemy_session.commit()
        entry_status = SettlementStatus(settlement_id=settlement.id,
                                        status=SettlementStatusOptions.submitted.value,
                                        reason='Settlement creation.')
        sqlalchemy_session.add(entry_status)
        sqlalchemy_session.commit()
        return settlement

    @classmethod
    def if_exists(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if cls.get_by_id(kwargs['settlement_id']) is not None:
                return func(*args, **kwargs)
            return {'response': "Cannot find settlement with provided ID."}, 404
        return wrapper


class AdvancePayment(Base):
    __tablename__ = 'AdvancePayment'
    # fields
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    submit_date = Column(DateTime)
    nr_kw = Column(String)
    # one to many
    settlement_id = Column(Integer, ForeignKey('Settlement.id', ondelete="CASCADE"), nullable=False)
    currency_id = Column(Integer, ForeignKey('Currency.id'), nullable=False)

    def show(self):
        advance_payment_to_show = {'id': self.id,
                                   'amount': self.amount,
                                   'currency_id': self.currency_id}
        return advance_payment_to_show

    def modify(self, modifications_dict: dict):
        stmt = update(AdvancePayment).where(AdvancePayment.id == self.id).values(**modifications_dict)
        sqlalchemy_session.execute(stmt)
        sqlalchemy_session.commit()

    @classmethod
    def create(cls, advance_payment_details: dict):
        advance_payment = AdvancePayment(**advance_payment_details)
        sqlalchemy_session.add(advance_payment)
        sqlalchemy_session.commit()
        return advance_payment

    @classmethod
    def if_exists(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if cls.get_by_id(kwargs['advance_payment_id']) is not None:
                return func(*args, **kwargs)
            return {'response': "Cannot find advance payment with provided ID."}, 404
        return wrapper


class MealType(enum.Enum):
    breakfast = 'breakfast'
    lunch = 'lunch'
    supper = 'supper'


class Meal(Base):
    __tablename__ = 'Meal'
    # fields
    id = Column(Integer, primary_key=True)
    type = Column(Enum(MealType), nullable=False)
    # one to many
    settlement_id = Column(Integer, ForeignKey('Settlement.id', ondelete="CASCADE"), nullable=False)

    def show(self):
        meal_to_show = {'id': self.id,
                        'type': self.type.value}
        return meal_to_show

    def modify(self, modifications_dict: dict):
        stmt = update(Meal).where(Meal.id == self.id).values(**modifications_dict)
        sqlalchemy_session.execute(stmt)
        sqlalchemy_session.commit()

    @classmethod
    def create(cls, meal_details: dict):
        meal = Meal(**meal_details)
        sqlalchemy_session.add(meal)
        sqlalchemy_session.commit()
        return meal

    @classmethod
    def if_exists(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if cls.get_by_id(kwargs['meal_id']) is not None:
                return func(*args, **kwargs)
            return {'response': "Cannot find meal with provided ID."}, 404
        return wrapper


class ExpenseType(enum.Enum):
    accommodation = 'accommodation'
    transit = 'transit'
    drive = 'drive'
    other = 'other'


class Expense(Base):
    __tablename__ = 'Expense'
    # fields
    id = Column(Integer, primary_key=True)
    type = Column(Enum(ExpenseType), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String)
    # one to many
    settlement_id = Column(Integer, ForeignKey('Settlement.id', ondelete="CASCADE"), nullable=False)
    currency_id = Column(Integer, ForeignKey('Currency.id'), nullable=False)
    # many to one
    attachment = relationship('Attachment', backref='expense', cascade="all,delete")

    def show(self):
        expense_to_show = {'id': self.id,
                           'settlement_id': self.settlement_id,
                           'amount': self.amount,
                           'currency': Currency.get_by_id(self.currency_id).name,
                           'type': self.type.value,
                           'description': self.description}
        return expense_to_show

    def modify(self, modifications_dict: dict):
        stmt = update(Expense).where(Expense.id == self.id).values(**modifications_dict)
        sqlalchemy_session.execute(stmt)
        sqlalchemy_session.commit()

    @classmethod
    def create(cls, expense_details: dict):
        expense = Expense(**expense_details)
        sqlalchemy_session.add(expense)
        sqlalchemy_session.commit()
        return expense

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
    file = Column(String, nullable=False)
    # one to many
    expense_id = Column(Integer, ForeignKey('Expense.id', ondelete="CASCADE"), nullable=False)

    def show(self):
        attachment_to_show = {'id': self.id,
                              'file': self.file}
        return attachment_to_show

    def modify(self, modifications_dict: dict):
        stmt = update(Attachment).where(Attachment.id == self.id).values(**modifications_dict)
        sqlalchemy_session.execute(stmt)
        sqlalchemy_session.commit()

    @classmethod
    def create(cls, attachment_details: dict):
        attachment = Attachment(**attachment_details)
        sqlalchemy_session.add(attachment)
        sqlalchemy_session.commit()
        return attachment

    @classmethod
    def if_exists(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if cls.get_by_id(kwargs['attachment_id']) is not None:
                return func(*args, **kwargs)
            return {'response': "Cannot find attachment with provided ID."}, 404
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
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)
    is_active = Column(Boolean)
    supervisor_id = Column(Integer)
    token = Column(String, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def show(self):
        user_to_show = {'id': self.id,
                        'first_name': self.first_name,
                        'last_name': self.last_name,
                        'email': self.email,
                        'role': self.role.value,
                        'is_active': self.is_active}
        return user_to_show

    def is_authorized(self, settlement: Settlement):
        if self.id == settlement.delegate_id or self.role.value in ['manager', 'hr', 'admin']:
            return True
        return False

    def modify(self, modifications_dict: dict):
        stmt = update(User).where(User.id == self.id).values(**modifications_dict)
        sqlalchemy_session.execute(stmt)
        sqlalchemy_session.commit()

    @classmethod
    def create(cls, user_details: dict):
        user = User(**user_details)
        user.is_active = True
        sqlalchemy_session.add(user)
        sqlalchemy_session.commit()
        return user

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
            return {'response': "You are not logged in."}, 401
        return wrapper

