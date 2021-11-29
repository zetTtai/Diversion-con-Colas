import sqlite3 # con = sqlite3.connect('db/database.db')

conn = sqlite3.connect('db/database.db')

cursor = conn.cursor()

cursor.execute('create table visitantes(id text PRIMARY KEY, name text, password text)')

cursor.execute('create table if not exists atracciones(id text PRIMARY KEY, wait_time integer, position text)')

cursor.execute('create table if not exists registros(id text PRIMARY KEY AUTOINCREMENT, timestamp integer, ip text, action text, params text)')

conn.commit()
conn.close()
