import sqlite3
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE studentss ( teleid STRING PRIMARY KEY , usn STRING , name STRING, year STRING , branch STRING , number STRING , email STRING)")
# cursor.execute("CREATE TABLE skills (usn string PRIMARY KEY, skills string)")
conn.commit()