import sqlite3

conn = sqlite3.connect('db/database.db')

cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS visitantes')
cursor.execute('DROP TABLE IF EXISTS atracciones')

conn.commit()
conn.close()