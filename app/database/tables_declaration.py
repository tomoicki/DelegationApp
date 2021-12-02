import enum
import os
import datetime
from flask import request
from werkzeug.utils import secure_filename
from functools import wraps
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Date, Float, Time, Enum, Boolean, DateTime, update
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from app.database.create_connection import sqlalchemy_session
from app.tools.useful_functions import recalculate_hours, currency_factor, id_from_str_to_int


# class Base:
class Mixin:
    # when u comment __init__ then every Table that inherits from Mixin
    # get false warnings "unexpected argument" when u try to construct an object Table()
    # and when i dont use Mixin and inherit methods from Base,
    # then PyCharm doesnt see the methods object.[list of all possible methods]
    def __init__(self, *args, **kwargs):
        pass

    id = Column(Integer)

    def delete(self):
        sqlalchemy_session.delete(self)
        sqlalchemy_session.commit()

    def modify(self, modifications_dict: dict):
        stmt = update(self.__class__).where(self.__class__.id == self.id).values(**modifications_dict)
        sqlalchemy_session.execute(stmt)
        sqlalchemy_session.commit()
        return self

    @classmethod
    def create(cls, object_details: dict):
        new_object = cls(**object_details)
        sqlalchemy_session.add(new_object)
        sqlalchemy_session.commit()
        return new_object

    @classmethod
    def get_by_id(cls, provided_id: int):
        if provided_id is not None and provided_id != 'None':
            return sqlalchemy_session.get(cls, provided_id)

    @classmethod
    def not_valid_dict(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            body = request.get_json()
            try:
                if type(body) == dict:
                    try:
                        body2 = body.copy()
                        if 'transit_type_id' in body2.keys():
                            del body2['transit_type_id']
                        id_from_str_to_int(body2)
                        cls(**body2)
                    except ValueError:
                        return {"response": "id needs to be stringed integer or just integer, e.g. '3' or 3. "
                                            "Make sure all id and _id keys have proper values."}, 400
                elif type(body) == list:
                    for item in body:
                        try:
                            item2 = item.copy()
                            if 'transit_type_id' in item2.keys():
                                del item2['transit_type_id']
                            id_from_str_to_int(item2)
                            cls(**item2)
                        except ValueError:
                            return {"response": "id needs to be stringed integer or just integer, e.g. '3' or 3. "
                                                "Make sure all id and _id keys have proper values."}, 400
                return func(*args, **kwargs)
            except (KeyError, TypeError) as e:
                return {"response": str(e)}, 400

        return wrapper


# Base = declarative_base(cls=Base)
Base = declarative_base()


class Country(Base, Mixin):
    __tablename__ = 'Country'
    __table_args__ = {'quote': False}
    # fields
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    diet = Column(Float)
    accommodation_limit = Column(Float)
    # one to many
    currency_id = Column(Integer, ForeignKey('Currency.id'))
    # many to one
    settlement = relationship("Settlement", backref='country')


class Currency(Base, Mixin):
    __tablename__ = 'Currency'
    __table_args__ = {'quote': False}
    # fields
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    # many to one
    country = relationship("Country", backref='currency')
    advance_payment = relationship("AdvancePayment", backref='currency')
    expense = relationship("Expense", backref='currency')

    @classmethod
    def get_by_name(cls, name: str):
        currency = sqlalchemy_session.query(cls).filter(cls.name == name).first()
        return currency.id


class SettlementStatusOptions(enum.Enum):
    submitted = 'submitted'
    approved = 'approved'
    denied = 'denied'
    closed = 'closed'


class SettlementStatus(Base, Mixin):
    __tablename__ = 'SettlementStatus'
    __table_args__ = {'quote': False}
    # fields
    id = Column(Integer, primary_key=True)
    status = Column(Enum(SettlementStatusOptions))
    reason = Column(String)
    date = Column(DateTime)
    # one to many
    settlement_id = Column(Integer, ForeignKey('Settlement.id', ondelete="CASCADE"))


class Settlement(Base, Mixin):
    __tablename__ = 'Settlement'
    __table_args__ = {'quote': False}
    # fields
    id = Column(Integer, primary_key=True)
    title = Column(String)
    departure_city = Column(String)
    arrival_city = Column(String)
    submit_date = Column(DateTime)
    departure_date = Column(Date)
    departure_time = Column(Time, default=datetime.time.fromisoformat("00:00:00"))
    arrival_date = Column(Date)
    arrival_time = Column(Time, default=datetime.time.fromisoformat("00:00:00"))
    reason = Column(String)
    remarks = Column(String)
    breakfast = Column(Integer, default=0)
    lunch = Column(Integer, default=0)
    supper = Column(Integer, default=0)
    # one to many
    delegate_id = Column(Integer, ForeignKey('Users.id'))
    delegate = relationship('Users',
                            backref=backref('settlement_his'),
                            primaryjoin='foreign(Settlement.delegate_id) == remote(Users.id)')
    creator_id = Column(Integer, ForeignKey('Users.id'))
    creator = relationship('Users',
                           backref=backref('creator'),
                           primaryjoin='foreign(Settlement.creator_id) == remote(Users.id)')
    approver_id = Column(Integer, ForeignKey('Users.id'))
    approver = relationship('Users',
                            backref=backref('approver'),
                            primaryjoin='foreign(Settlement.approver_id) == remote(Users.id)')
    country_id = Column(Integer, ForeignKey('Country.id'))
    # many to one
    advance_payment = relationship('AdvancePayment', backref='settlement', cascade="all,delete")
    expense = relationship('Expense', backref='settlement', cascade="all,delete")
    status = relationship('SettlementStatus', backref='settlement', cascade="all,delete")

    def calculate_diet(self):
        """Calculates diet (D35 in excel) for delegation."""
        country = Country.get_by_id(self.country_id)
        meal_reduction = self.breakfast * 0.25 + self.lunch * 0.5 + self.supper * 0.25
        time_delta = datetime.datetime.combine(self.arrival_date, self.arrival_time) - \
                     datetime.datetime.combine(self.departure_date, self.departure_time)
        diet_from_days_hours = (time_delta.days + recalculate_hours(time_delta.seconds / (3600 * 24), days=time_delta.days)) * country.diet
        diet_meal_reduced = diet_from_days_hours - meal_reduction * country.diet
        return {'diet_from_days_hours': str(diet_from_days_hours),
                'diet_meal_reduced': str(diet_meal_reduced),
                'currency': Currency.get_by_id(country.currency_id).name,
                'daily_amount': str(country.diet),
                'daily_limit': str(country.accommodation_limit)}

    def sum_of_expenses(self):
        expenses_list = self.expense
        # all_expense_types = {expense.type.value for expense in expenses_list}
        all_expense_types = [enum_option.value for enum_option in ExpenseType]
        sum_of_expenses_by_type = {expense_type: sum([expense.convert_to_pln() for expense in expenses_list
                                                      if expense.type.value == expense_type])
                                   for expense_type in all_expense_types}
        sum_of_expenses_by_type['total'] = sum(sum_of_expenses_by_type.values())
        sum_of_expenses_by_type = {key: str(value) for key, value in sum_of_expenses_by_type.items()}
        return sum_of_expenses_by_type

    def sum_of_advanced_payments(self):
        advanced_payments_list = self.advance_payment
        currency_set = {advance_payment.currency_id for advance_payment in advanced_payments_list}
        sum_of_advanced_payments_by_currency = \
            {currency: str(sum([advance_payment.amount for advance_payment in advanced_payments_list if
                                advance_payment.currency_id == currency])) for currency in currency_set}
        sum_of_advanced_payments_by_currency = [{"currency_id": str(key),
                                                 "currency_name": Currency.get_by_id(key).name,
                                                 "amount": value}
                                                for key, value in sum_of_advanced_payments_by_currency.items()]
        # sum_of_advanced_payments = [advance_payment.convert_to_pln() for advance_payment in advanced_payments_list]
        return sum_of_advanced_payments_by_currency

    # def generate_pdf(self):
    #     import reportlab.lib.colors as pdf_colors
    #     from reportlab.lib.pagesizes import A4
    #     from reportlab.lib.units import inch
    #     from reportlab.pdfgen.canvas import Canvas
    #     canvas = Canvas(f"{self.title}.pdf", pagesize=A4)
    #     # Set font to Times New Roman with 12-point size
    #     canvas.setFont("Times-Roman", 12)
    #     # Draw blue text one inch from the left and ten
    #     # inches from the bottom
    #     canvas.setFillColor(pdf_colors.blue)
    #     for i, tup in enumerate(self.details().items()):
    #         canvas.drawString(text=f"{tup[0]}: {tup[1]}", x=10+10*i, y=10+10*i)
    #     # Save the PDF file
    #     canvas.save()

    def current_status(self):
        return self.status[-1].status.value

    def change_status(self, changed_status: str, reason: str):
        if changed_status in [enum_option.value for enum_option in SettlementStatusOptions]:
            if self.current_status() != changed_status:
                new_status = SettlementStatus(settlement_id=self.id,
                                              status=changed_status,
                                              reason=reason,
                                              date=datetime.datetime.now())
                sqlalchemy_session.add(new_status)
                sqlalchemy_session.commit()

    def show(self):
        settlement_to_show = {'id': str(self.id),
                              'approver': str(Users.get_by_id(self.approver_id)),
                              'submit_date': self.submit_date,
                              'departure_city': self.departure_city,
                              'arrival_city': self.arrival_city,
                              'departure_date': self.departure_date,
                              'arrival_date': self.arrival_date,
                              'country': Country.get_by_id(self.country_id).name,
                              'delegate': str(Users.get_by_id(self.delegate_id)),
                              'title': self.title,
                              'reason': self.reason,
                              'remarks': self.remarks,
                              'status': self.current_status()}
        return settlement_to_show

    def details(self):
        country = Country.get_by_id(self.country_id)
        time_delta = datetime.datetime.combine(self.arrival_date, self.arrival_time) - \
                     datetime.datetime.combine(self.departure_date, self.departure_time)
        residue_time = time_delta.seconds / 3600
        hours = int(residue_time)
        minutes = round((residue_time - hours) * 60)
        trip_duration = f"{time_delta.days}d {hours}h {minutes}m"
        exchange_rate = currency_factor(Currency.get_by_id(country.currency_id).name)
        approver_names, approver_id = Users.name_and_id(self.approver_id)
        delegate_names, delegate_id = Users.name_and_id(self.delegate_id)
        creator_names, creator_id = Users.name_and_id(self.creator_id)
        settlement_with_details = {'id': str(self.id),
                                   'submit_date': self.submit_date,
                                   'departure_city': self.departure_city,
                                   'arrival_city': self.arrival_city,
                                   'departure_date': self.departure_date,
                                   'departure_time': self.departure_time,
                                   'arrival_date': self.arrival_date,
                                   'arrival_time': self.arrival_time,
                                   'breakfast': str(self.breakfast),
                                   'lunch': str(self.lunch),
                                   'supper': str(self.supper),
                                   'country': country.name,
                                   'delegate': delegate_names,
                                   'approver': approver_names,
                                   'creator': creator_names,
                                   'delegate_id': delegate_id,
                                   'approver_id': approver_id,
                                   'creator_id': creator_id,
                                   'title': self.title,
                                   'reason': self.reason,
                                   'remarks': self.remarks,
                                   'status': self.current_status(),
                                   'trip_duration': trip_duration,
                                   'exchange_rate_for_diet_currency': str(exchange_rate)}
        settlement_with_details = {key: (value.isoformat() if '_time' in key and value is not None else value)
                                   for key, value in settlement_with_details.items()}
        return settlement_with_details

    def give_sorted_expenses(self):
        expenses_list = self.expense
        expenses_list = [expense.show() for expense in expenses_list if expense.refundable]
        currency_set = {expense['currency'] for expense in expenses_list}
        type_amount = {currency: {expense_type: str(sum([float(expense['amount']) for expense in expenses_list if
                                                         expense['currency'] == currency and expense[
                                                             'type'] == expense_type]))
                                  for expense_type in {expense['type'] for expense in expenses_list if
                                                       expense['currency'] == currency}} for currency in currency_set}
        total_amount = {currency: {'total': str(sum([float(expense['amount']) for expense in expenses_list if
                                                     expense['currency'] == currency])) for expense in expenses_list if
                                   expense['currency'] == currency} for currency in currency_set}
        expenses_by_currency = [{'currency': currency,
                                 'currency_id': str(Currency.get_by_name(currency)),
                                 'total_amount': total_amount[currency]['total'],
                                 'type_amount': type_amount[currency],
                                 'expenses': [expense for expense in expenses_list if expense['currency'] == currency]}
                                for currency in currency_set]
        return expenses_by_currency

    @classmethod
    def create(cls, settlement_details: dict):
        transit_type_id = None
        if 'transit_type_id' in settlement_details:
            transit_type_id = settlement_details['transit_type_id']
            del settlement_details['transit_type_id']
        settlement_details['submit_date'] = datetime.datetime.now()
        settlement = Settlement(**settlement_details)
        sqlalchemy_session.add(settlement)
        sqlalchemy_session.flush()
        if transit_type_id:
            first_transit_expense = Expense(amount=0,
                                            type="transit",
                                            settlement_id=settlement.id,
                                            currency_id=1,
                                            description=Transit.get_by_id(transit_type_id).type)
            first_transit_expense.transit_type = [Transit.get_by_id(transit_type_id)]
            sqlalchemy_session.add(first_transit_expense)
            sqlalchemy_session.flush()
        entry_status = SettlementStatus(settlement_id=settlement.id,
                                        status=SettlementStatusOptions.submitted.value,
                                        reason='Settlement creation.',
                                        date=datetime.datetime.now())
        sqlalchemy_session.add(entry_status)
        sqlalchemy_session.commit()
        return settlement

    @classmethod
    def if_exists(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                int(kwargs['settlement_id'])
                if cls.get_by_id(kwargs['settlement_id']) is not None:
                    return func(*args, **kwargs)
                return {'response': "Cannot find settlement with provided ID."}, 404
            except ValueError:
                return {'response': f"Wrong 'id' format. You gave '{kwargs['settlement_id']}', "
                                    f"but needs to be an integer."}, 404

        return wrapper


class AdvancePayment(Base, Mixin):
    __tablename__ = 'AdvancePayment'
    __table_args__ = {'quote': False}
    # fields
    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    submit_date = Column(DateTime)
    nr_kw = Column(String)
    # one to many
    settlement_id = Column(Integer, ForeignKey('Settlement.id', ondelete="CASCADE"))
    currency_id = Column(Integer, ForeignKey('Currency.id'))

    def convert_to_pln(self):
        """Recalculates amount from XXX to PLN if needed."""
        currency_name = Currency.get_by_id(self.currency_id).name
        if currency_name == 'PLN':
            return self.amount
        factor = currency_factor(currency_name)
        return self.amount / factor

    def show(self):
        advance_payment_to_show = {'id': str(self.id),
                                   'amount': str(format(self.amount, '.2f')),
                                   'currency_id': str(self.currency_id),
                                   'submit_date': self.submit_date}
        return advance_payment_to_show

    @classmethod
    def if_exists(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                int(kwargs['advance_payment_id'])
                if cls.get_by_id(kwargs['advance_payment_id']) is not None:
                    return func(*args, **kwargs)
                return {'response': "Cannot find advance payment with provided ID."}, 404
            except ValueError:
                return {'response': f"Wrong 'id' format. You gave '{kwargs['advance_payment_id']}', "
                                    f"but needs to be an integer."}, 404

        return wrapper


class ExpenseType(enum.Enum):
    accommodation = 'accommodation'
    transit = 'transit'
    drive = 'drive'
    other = 'other'


association_Expense_Transit_Type = Table('association_Expense_Transit_Type', Base.metadata,
                                         Column('expense_id', ForeignKey('Expense.id', ondelete="CASCADE"), primary_key=True),
                                         Column('transit_id', ForeignKey('Transit.id'), primary_key=True))


class Transit(Base, Mixin):
    __tablename__ = 'Transit'
    __table_args__ = {'quote': False}
    # fields
    id = Column(Integer, primary_key=True)
    type = Column(String)
    # many to many
    expense = relationship("Expense",
                           secondary=association_Expense_Transit_Type,
                           back_populates='transit_type')


class Expense(Base, Mixin):
    __tablename__ = 'Expense'
    __table_args__ = {'quote': False}
    # fields
    id = Column(Integer, primary_key=True)
    type = Column(Enum(ExpenseType))
    amount = Column(Float)
    description = Column(String)
    refundable = Column(Boolean, default=True)
    # one to many
    settlement_id = Column(Integer, ForeignKey('Settlement.id', ondelete="CASCADE"))
    currency_id = Column(Integer, ForeignKey('Currency.id'))
    # many to one
    attachment = relationship('Attachment', backref='expense', cascade="all,delete")
    # many to many
    transit_type = relationship("Transit",
                                secondary=association_Expense_Transit_Type,
                                back_populates='expense')

    def convert_to_pln(self):
        """Recalculates amount from XXX to PLN if needed."""
        currency_name = Currency.get_by_id(self.currency_id).name
        if currency_name == 'PLN':
            return self.amount
        # else, get the factor
        factor = currency_factor(currency_name)
        return self.amount * factor

    def show(self):
        attachments = self.attachment
        attachments = [attachment.show() for attachment in attachments]
        expense_to_show = {'id': str(self.id),
                           'settlement_id': str(self.settlement_id),
                           'amount': str(format(self.amount, '.2f')),
                           'currency': Currency.get_by_id(self.currency_id).name,
                           'type': self.type.value,
                           'description': self.description,
                           'attachments': attachments}
        if self.transit_type:
            expense_to_show['transit_type'] = self.transit_type[0].type
            expense_to_show['transit_type_id'] = self.transit_type[0].id
        return expense_to_show

    def modify(self, modifications_dict: dict):
        if 'transit_type_id' in modifications_dict.keys():
            association_Expense_Transit_Type.update().where()
            stmt = update(association_Expense_Transit_Type).where(association_Expense_Transit_Type.c.expense_id == self.id)\
                .values({"transit_id": modifications_dict['transit_type_id']})
            sqlalchemy_session.execute(stmt)
            sqlalchemy_session.commit()
            del modifications_dict['transit_type_id']
        stmt = update(self.__class__).where(self.__class__.id == self.id).values(**modifications_dict)
        sqlalchemy_session.execute(stmt)
        sqlalchemy_session.commit()
        return self

    @classmethod
    def create(cls, object_details: dict):
        if 'transit_type_id' in object_details.keys():
            transit_type_id = object_details['transit_type_id']
            del object_details['transit_type_id']
            new_object = cls(**object_details)
            new_object.transit_type = [Transit.get_by_id(transit_type_id)]
            sqlalchemy_session.add(new_object)
            sqlalchemy_session.commit()
        else:
            new_object = cls(**object_details)
            sqlalchemy_session.add(new_object)
            sqlalchemy_session.commit()
        return new_object

    @classmethod
    def if_exists(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                int(kwargs['expense_id'])
                if cls.get_by_id(kwargs['expense_id']) is not None:
                    return func(*args, **kwargs)
                return {'response': "Cannot find expense with provided ID."}, 404
            except ValueError:
                return {'response': f"Wrong 'id' format. You gave '{kwargs['expense_id']}', "
                                    f"but needs to be an integer."}, 404

        return wrapper


class Attachment(Base, Mixin):
    __tablename__ = 'Attachment'
    __table_args__ = {'quote': False}
    # fields
    id = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String)
    # one to many
    expense_id = Column(Integer, ForeignKey('Expense.id', ondelete="CASCADE"))

    @staticmethod
    def allowed_file(filename):
        valid_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in valid_extensions

    @classmethod
    def create(cls, expense_id: int):
        uploads_dir = os.path.join(os.getcwd(), 'uploads')
        expense_path = os.path.join(uploads_dir, 'expense_' + str(expense_id))
        if not os.path.exists(expense_path):
            os.makedirs(expense_path)
        response = []
        files = request.files.getlist('attachment')
        for file in files:
            if file and cls.allowed_file(file.filename) and file.filename.replace(' ', '_') not in os.listdir(
                    expense_path):
                file_name = secure_filename(file.filename)
                file_path = os.path.join(expense_path, file_name)
                file.save(file_path)
                attachment = Attachment(expense_id=expense_id,
                                        path=file_path,
                                        name=file_name)
                sqlalchemy_session.add(attachment)
                sqlalchemy_session.commit()
                response.append(attachment.show())
            else:
                response.append({"error": f"uploaded attachment '{file.filename}' already exists."})
        return response

    def show(self):
        attachment_to_show = {'id': str(self.id),
                              'path': self.path,
                              'name': self.name}
        return attachment_to_show

    @classmethod
    def if_exists(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                int(kwargs['attachment_id'])
                if cls.get_by_id(kwargs['attachment_id']) is not None:
                    return func(*args, **kwargs)
                return {'response': "Cannot find attachment with provided ID."}, 404
            except ValueError:
                return {'response': f"Wrong 'id' format. You gave '{kwargs['attachment_id']}', "
                                    f"but needs to be an integer."}, 404

        return wrapper


class Role(enum.Enum):
    user = 'user'
    manager = 'manager'
    hr = 'hr'
    admin = 'admin'


class Users(Base, Mixin):
    __tablename__ = 'Users'
    __table_args__ = {'quote': False}
    # fields
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    default_city = Column(String)
    role = Column(Enum(Role))
    is_active = Column(Boolean)
    supervisor_id = Column(Integer)
    token = Column(String, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @classmethod
    def name_and_id(cls, provided_id):
        user = cls.get_by_id(provided_id)
        return [str(user), str(user.id)] if user is not None else ["", ""]

    def show(self):
        supervisor_names, supervisor_id = Users.name_and_id(self.supervisor_id)
        user_to_show = {'id': str(self.id),
                        'first_name': self.first_name,
                        'last_name': self.last_name,
                        'email': self.email,
                        'default_city': self.default_city,
                        'role': self.role.value,
                        'is_active': self.is_active,
                        'supervisor_id': supervisor_id,
                        'supervisor': supervisor_names}
        return user_to_show

    def show_id_names(self):
        stuff_to_show = {'id': str(self.id),
                         'first_name': self.first_name,
                         'last_name': self.last_name}
        return stuff_to_show

    def is_authorized(self, settlement: Settlement):
        if self.id == settlement.delegate_id or self.role.value in ['manager', 'hr', 'admin']:
            return True
        return False

    @classmethod
    def create(cls, user_details: dict):
        user = Users(**user_details)
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
