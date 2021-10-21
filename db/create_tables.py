import sqlite3 # con = sqlite3.connect('db/database.db')

conn = sqlite3.connect('db/database.db')

cursor = conn.cursor()

cursor.execute('create table visitantes(id integer PRIMARY KEY, name text, password text, position text)')

cursor.execute('create table if not exists atracciones(id integer PRIMARY KEY, wait_time integer, capacity integer, position text)')

conn.commit()
conn.close()