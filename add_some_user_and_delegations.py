from app.database.create_connection import postgre_connection, sqlalchemy_session
from app.database.tables_declaration import *
from shortuuid import uuid
import datetime
import csv

Base.metadata.create_all(postgre_connection)

with open('foreign_diet_rate.csv', mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    currency_names = {line['Currency'] for line in reader}
    currencies = [Currency(name=name) for name in currency_names]
    sqlalchemy_session.bulk_save_objects(currencies)
    sqlalchemy_session.commit()

with open('foreign_diet_rate.csv', mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    countries = [Country(name=line['Country'],
                         diet=line['Diet Rate'],
                         accommodation_limit=line['Accommodation Limit'],
                         currency_id=sqlalchemy_session.query(Currency).where(
                             Currency.name == line['Currency']).first().id)
                 for line in reader]
    sqlalchemy_session.bulk_save_objects(countries)
    sqlalchemy_session.commit()

country1 = sqlalchemy_session.query(Country).where(Country.name == 'Poland').first()
currency1 = sqlalchemy_session.query(Currency).where(Currency.id == country1.currency_id).first()
country2 = sqlalchemy_session.query(Country).where(Country.name == 'Germany').first()
currency2 = sqlalchemy_session.query(Currency).where(Currency.id == country2.currency_id).first()

some_user = {'first_name': 'First',
             'last_name': 'User',
             'email': 'usr@itechart.com',
             'password': 'right',
             'role': Role.user,
             'is_active': True,
             'token': uuid()}
user1 = User(**some_user)
sqlalchemy_session.add(user1)
user11 = User(**some_user)
user11.first_name = 'User2'
user11.email = 'user2@gmail.com'
user11.token = uuid()
sqlalchemy_session.add(user11)
user2 = User(**some_user)
user2.first_name = 'Maker'
user2.email = 'maker@gmail.com'
user2.role = Role.manager
user2.token = uuid()
sqlalchemy_session.add(user2)
user3 = User(**some_user)
user3.first_name = 'Hr'
user3.email = 'hr@gmail.com'
user3.role = Role.hr
user3.token = uuid()
sqlalchemy_session.add(user3)
user4 = User(**some_user)
user4.first_name = 'admin'
user4.email = 'admin@gmail.com'
user4.role = Role.admin
user4.token = uuid()
sqlalchemy_session.add(user4)
sqlalchemy_session.commit()

some_delegation = {'title': 'to wroclaw',
                   'submit_date': datetime.datetime.now(),
                   "departure_date": "2020-01-15",
                   "arrival_date": "2020-01-20",
                   'delegate_id': user1.id,
                   'creator_id': user1.id,
                   'approver_id': user3.id,
                   'country_id': country1.id}
delegation1 = Delegation.create(some_delegation)
sqlalchemy_session.add(delegation1)
delegation2 = Delegation.create(some_delegation)
delegation2.title = 'to warsaw'
delegation2.creator_id = user2.id
delegation2.country_id = country2.id
sqlalchemy_session.add(delegation2)
sqlalchemy_session.commit()

advance_payment1 = AdvancePayment(amount=121.1,
                                  delegation_id=delegation1.id,
                                  currency_id=currency1.id)
sqlalchemy_session.add(advance_payment1)
advance_payment2 = AdvancePayment(amount=10,
                                  delegation_id=delegation2.id,
                                  currency_id=currency2.id)
sqlalchemy_session.add(advance_payment2)
sqlalchemy_session.commit()

some_settlement = {"departure_date": "2020-01-15",
                   "departure_time": "10:10:10",
                   "arrival_date": "2020-01-20",
                   "arrival_time": "20:10:10",
                   'delegation_id': delegation1.id}
settlement1 = Settlement.create(some_settlement)
sqlalchemy_session.add(settlement1)
sqlalchemy_session.commit()

some_expense = {'type': ExpenseType.accommodation,
                'amount': 123.45,
                'currency_id': currency1.id,
                'settlement_id': settlement1.id}
expense1 = Expense(**some_expense)
sqlalchemy_session.add(expense1)
expense2 = Expense(**some_expense)
expense2.type = ExpenseType.transit
expense2.amount = 99
expense2.settlement_id = settlement1.id
sqlalchemy_session.add(expense2)
expense3 = Expense(**some_expense)
expense3.type = ExpenseType.other
expense3.amount = 11
expense3.settlement_id = settlement1.id
sqlalchemy_session.add(expense3)
sqlalchemy_session.commit()

meal1 = Meal(type=MealType.breakfast,
             settlement_id=settlement1.id)
sqlalchemy_session.add(meal1)
meal2 = Meal(type=MealType.supper,
             settlement_id=settlement1.id)
sqlalchemy_session.add(meal2)
meal3 = Meal(type=MealType.lunch,
             settlement_id=settlement1.id)
sqlalchemy_session.add(meal3)
sqlalchemy_session.commit()
