import sqlite3

conn = sqlite3.connect('skills.db')
cursor = conn.cursor()

# cursor.execute('''CREATE TABLE skills (usn text, skills text)''')
# cursor.execute("INSERT INTO clubs VALUES ('DESTINY MUSIC CLIQUE', 'user1', 'pass1' , 'music')")
# cursor.execute("INSERT INTO clubs VALUES ('VULCANS', 'user2', 'pass2', 'dance')")
# cursor.execute("INSERT INTO clubs VALUES ('AURORA', 'user3', 'pass3' , 'acting')")
cursor.execute("INSERT INTO skills VALUES ('same usn as prev', 'music')")


# cursor.execute("INSET INTO studentss VALUES('1SI20IS027' , 'mayur' , '4' , 'ISE' , 'phone numbe'  , 'email' )



conn.commit()
conn.close()