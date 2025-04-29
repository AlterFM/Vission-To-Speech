import mysql.connector  # Import untuk MySQL
import time
from detector import detect_objects  # Import fungsi deteksi dari detector.py

# Connect to MySQL database
def create_database():
    # Koneksi ke MySQL (gunakan konfigurasi XAMPP default)
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Default user untuk XAMPP adalah 'root'
        password="",  # Default password untuk XAMPP adalah kosong
        database="barang_db"  # Nama database yang sudah dibuat
    )
    
    cursor = conn.cursor()

    # Membuat tabel jika belum ada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS barang (
            id INT AUTO_INCREMENT PRIMARY KEY,
            waktu DATETIME,
            stage VARCHAR(50),
            orang_id VARCHAR(50),
            barang_terdeteksi TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Save data to MySQL
def save_to_db(stage, orang_id, items):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="barang_db"
    )
    
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO barang (waktu, stage, orang_id, barang_terdeteksi)
        VALUES (%s, %s, %s, %s)
    ''', (time.strftime('%Y-%m-%d %H:%M:%S'), stage, orang_id, ', '.join(items)))
    
    conn.commit()
    conn.close()

# Main program to start detection
def main():
    create_database()

    # Path to videos
    masuk_video = 'videos/masuk.mp4'
    keluar_video = 'videos/keluar.mp4'

    # Simulate person ID (should be obtained from face recognition)
    orang_id = 'orang_001'

    # Deteksi barang saat masuk
    detected_items_masuk = detect_objects(masuk_video)
    save_to_db('masuk', orang_id, detected_items_masuk)
    print(f"[INFO] Data untuk orang ID '{orang_id}' saat masuk sudah disimpan: {', '.join(detected_items_masuk)}")

    # Deteksi barang saat keluar
    detected_items_keluar = detect_objects(keluar_video)
    save_to_db('keluar', orang_id, detected_items_keluar)
    print(f"[INFO] Data untuk orang ID '{orang_id}' saat keluar sudah disimpan: {', '.join(detected_items_keluar)}")

if __name__ == "__main__":
    main()
