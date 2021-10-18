from app.database.create_connection import postgre_connection, postgre_session
from app.database.tables_declaration import *
from shortuuid import uuid
import datetime

Base.metadata.create_all(postgre_connection)
session = postgre_session()

currency1 = Currency(id=uuid(),
                     name='PLN')

country1 = Country(id=uuid(),
                   name='Poland',
                   currency_id=currency1.id)

some_user = {'id': uuid(),
             'first_name': 'First',
             'last_name': 'User',
             'email': 'usr@itechart.com',
             'password': 'right',
             'role': Role.user,
             'is_active': True,
             'token': uuid()}
user1 = User(**some_user)
user2 = User(**some_user)
user2.id = uuid()
user2.first_name = 'Maker'
user2.email = 'maker@gmail.com'
user2.role = Role.manager

some_delegation = {'id': uuid(),
                   'title': 'to wroclaw',
                   'submit_date': datetime.datetime.now(),
                   'departure_date': datetime.date.fromisocalendar(2021, 5, 3),
                   'departure_time': datetime.time(10, 10, 10),
                   'arrival_date': datetime.date.fromisocalendar(2021, 5, 4),
                   'arrival_time': datetime.time(20, 20, 20),
                   'worker_id': user1.id,
                   'maker_id': user2.id,
                   'country_id': country1.id}
delegation1 = Delegation(**some_delegation)
delegation2 = Delegation(**some_delegation)
delegation2.id = uuid()
delegation2.title = 'to warsaw'

some_expense = {'id': uuid(),
                'type': ExpenseType.accommodation,
                'amount': 123.45,
                'currency_id': currency1.id,
                'delegation_id': delegation1.id}
expense1 = Expense(**some_expense)
expense2 = Expense(**some_expense)
expense2.id = uuid()
expense2.type = ExpenseType.transit
expense2.amount = 99
expense2.delegation_id = delegation2.id

meal1 = Meal(id=uuid(),
             type=MealType.breakfast,
             delegation_id=delegation1.id)

advance_payment1 = AdvancePayment(id=uuid(),
                                  amount=121.1,
                                  delegation_id=delegation1.id,
                                  currency_id=currency1.id)

session.bulk_save_objects([currency1, country1, user1, user2, delegation1, delegation2,
                           expense1, expense2,meal1, advance_payment1])
session.commit()
