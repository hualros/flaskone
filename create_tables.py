import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_table = "create table if not exists users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "create table if not exists items (name text, price real)"
cursor.execute(create_table)

cursor.execute("insert into items values ('apple', 10.99)")
cursor.execute("insert into items values ('banana', 2.50)")

connection.commit()
connection.close()
