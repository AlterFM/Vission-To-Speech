import sqlite3
import os

# Koneksi ke database SQLite
def create_database():
    if not os.path.exists('database/barang.db'):
        conn = sqlite3.connect('database/barang.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS barang (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                waktu TEXT,
                stage TEXT,
                orang_id TEXT,
                barang_terdeteksi TEXT
            )
        ''')
        conn.commit()
        conn.close()

def save_to_db(stage, orang_id, items):
    conn = sqlite3.connect('database/barang.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO barang (waktu, stage, orang_id, barang_terdeteksi)
        VALUES (?, ?, ?, ?)
    ''', (time.strftime('%Y-%m-%d %H:%M:%S'), stage, orang_id, ', '.join(items)))
    conn.commit()
    conn.close()
