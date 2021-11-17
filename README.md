# DelegationApp
In order to make application work you need to have postgresql database instance.<br>
You could use our remote database dedicated for this app, but you need to contact me directly to get the connection string.

You can also create your own local database instance.<br>
Visit [PostgreSQL documentation](https://www.postgresql.org/docs/current/) to find out how.<br>
When you have your database instance ready you need to define environment variables.<br>
For example, you could create file '.env' that contains following data.
>POSTGRE_SQL_HOST = localhost<br>
>POSTGRE_SQL_PORT = 5432<br>
>POSTGRE_SQL_USER = your_username<br>
>POSTGRE_SQL_PASSWORD = your_password<br>
>POSTGRE_SQL_DB_NAME = your_database_name

Alternatively, you could directly change the connection string (app/database/connection_functions) from<br> 
<code>postgres_str = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'</code><br>
to<br>
<code>postgres_str = f'postgresql://your_username:your_password@localhost:5432/your_database_name'</code>

Once you have your database and connection details set up, you will need to run <code>run_me_just_once.py</code>.<br>
It will create all the tables and populate them.<br>
Then, to start the application execute <code>run.py</code>.<br>
You should see this or similar output.
> Serving Flask app 'app.app' (lazy loading)<br>
Environment: production<br>
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.<br>
Debug mode: off<br>
Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

When the application is running, go to http://127.0.0.1:5000/swagger/ to test out API.