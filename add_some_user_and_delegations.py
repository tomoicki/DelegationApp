from app.database.create_connection import postgre_connection, postgre_session
from app.database.tables_declaration import *
from shortuuid import uuid
import datetime

Base.metadata.create_all(postgre_connection)
session = postgre_session()

currency1 = Currency(name='PLN')
session.add(currency1)
session.commit()
country1 = Country(name='Poland',
                   currency_id=currency1.id)
session.add(country1)
session.commit()
some_user = {'first_name': 'First',
             'last_name': 'User',
             'email': 'usr@itechart.com',
             'password': 'right',
             'role': Role.user,
             'is_active': True,
             'token': uuid()}
user1 = User(**some_user)
session.add(user1)
session.commit()
user2 = User(**some_user)
user2.first_name = 'Maker'
user2.email = 'maker@gmail.com'
user2.role = Role.manager
session.add(user2)
session.commit()

some_delegation = {'title': 'to wroclaw',
                   'submit_date': datetime.datetime.now(),
                   'departure_date': datetime.date.fromisocalendar(2021, 5, 3),
                   'departure_time': datetime.time(10, 10, 10),
                   'arrival_date': datetime.date.fromisocalendar(2021, 5, 4),
                   'arrival_time': datetime.time(20, 20, 20),
                   'worker_id': user1.id,
                   'maker_id': user2.id,
                   'country_id': country1.id}
delegation1 = Delegation(**some_delegation)
session.add(delegation1)
session.commit()
delegation2 = Delegation(**some_delegation)
delegation2.title = 'to warsaw'
session.add(delegation2)
session.commit()

some_expense = {'type': ExpenseType.accommodation,
                'amount': 123.45,
                'currency_id': currency1.id,
                'delegation_id': delegation1.id}
expense1 = Expense(**some_expense)
session.add(expense1)
session.commit()
expense2 = Expense(**some_expense)
expense2.type = ExpenseType.transit
expense2.amount = 99
expense2.delegation_id = delegation1.id
session.add(expense2)
session.commit()

meal1 = Meal(type=MealType.breakfast,
             delegation_id=delegation1.id)
session.add(meal1)
session.commit()

advance_payment1 = AdvancePayment(amount=121.1,
                                  delegation_id=delegation1.id,
                                  currency_id=currency1.id)
session.add(advance_payment1)
session.commit()

