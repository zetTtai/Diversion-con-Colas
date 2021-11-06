import sqlite3

conn = sqlite3.connect('db/database.db')

cursor = conn.cursor()

data = [
    ("atraccion1",  0, "2 3"), 
    ("atraccion2",  0, "1 8"), 
    ("atraccion3",  0, "6 7"), 
    ("atraccion4",  0, "8 2"), 
    ("atraccion5",  0, "1 17"), 
    ("atraccion6",  0, "3 13"), 
    ("atraccion7",  0, "5 16"), 
    ("atraccion8",  0, "9 11"),
    ("atraccion9",  0, "11 5"), 
    ("atraccion10", 0, "14 1"), 
    ("atraccion11", 0, "16 9"), 
    ("atraccion12", 0, "19 4"),
    ("atraccion13", 0, "10 19"), 
    ("atraccion14", 0, "13 12"), 
    ("atraccion15", 0, "15 18"), 
    ("atraccion16", 0, "18 14")
]

cursor.executemany("INSERT INTO atracciones VALUES(?, ?, ?)", data)

conn.commit()
conn.close()

# Zona Verde [(1, 0, 100, "2 3"), (2, 0, 80, "1 8"), (3, 0, 50, "6 7"), (4, 0, 150, "8 2")]
# Zona Azul  [(5, 0, 100, "1 17"), (6, 0, 80, "3 13"), (7, 0, 50, "5 16"), (8, 0, 150, "9 11")]
# Zona Roja  [(9, 0, 100, "11 5"), (10, 0, 80, "14 1"), (11, 0, 50, "16 9"), (12, 0, 150, "19 4")]
# Zona Gris  [(13, 0, 100, "10 19"), (14, 0, 80, "13 12"), (15, 0, 50, "15 18"), (16, 0, 150, "18 14")] 
