import sqlite3

conn = sqlite3.connect('database/barang.db')
cursor = conn.cursor()

for row in cursor.execute('SELECT * FROM barang'):
    print(row)

conn.close()
