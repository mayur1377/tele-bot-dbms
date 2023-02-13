import sqlite3
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute("DELETE FROM studentss WHERE teleid='1377833323'")
conn.commit()