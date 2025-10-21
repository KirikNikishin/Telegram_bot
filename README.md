# Telegram_bot
## Project on the discipline "Databases"

A project on the discipline "Databases". 
-  This application is designed to manage the work of a Telegram bot and SQL database. The Aiogram library is used to create and manage the bot. 
-  SQL queries are implemented in the Python programming language. The MySQL library is used to interact with the database.

> [!WARNING]
> You must deploy the database on your system. The corresponding sql file with the database structure and test data is located in the "sql_structure_&_data" directory.
> 
> To work correctly, you need to make changes to the files **"config_bot"** and **"config_sql"**.
> - You must to make file **"config_bot.py"** to specify the **Token** of your previously created Telegram bot, in the value of the ***"TOKEN"*** parameter.
> - You must to make filr **"config_sql.py"** to specify the connection parameters to your database: ***host***, ***user***, ***password***, ***port***.
> - Create a database named ***db_py_book_shop***. You can choose **any other database name**, but **do not forget to specify** a new name in the **"config_sql"** file in the value of the ***"db_name"*** parameter.
