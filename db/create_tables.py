import sqlite3 # con = sqlite3.connect('db/database.db')

conn = sqlite3.connect('db/database.db')

cursor = conn.cursor()

cursor.execute('create table visitantes(id text PRIMARY KEY, name text, password text)')

cursor.execute('create table if not exists atracciones(id text PRIMARY KEY, wait_time integer, position text)')

conn.commit()
conn.close()
