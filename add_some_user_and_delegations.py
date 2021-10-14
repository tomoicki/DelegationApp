from app.database.create_connection import postgre_connection, postgre_session
from app.database.tables_declaration import *


Base.metadata.create_all(postgre_connection)
session = postgre_session()
some_user = {'first_name': 'First',
             'last_name': 'User',
             'email': 'usr@itechart.com',
             'password': 'right',
             'access_level': 999,
             'token': 'xxx'}
user1 = User(**some_user)
delegation1 = Delegation()
delegation1.title = 'aaa'
delegation1.user_email = user1.email

delegation2 = Delegation()
delegation2.title = 'bbb'
delegation2.user_email = user1.email

user2 = User(**some_user)
user2.email = 'other@mail.com'
delegation3 = Delegation()
delegation3.title = 'ccc'
delegation3.user_email = user2.email

# session.add(user1)
# session.add(user2)
# session.add(delegation1)
# session.add(delegation2)
# session.add(delegation3)
# session.commit()

