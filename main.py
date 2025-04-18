import torch
import cv2
from gtts import gTTS

# === SETUP ===
VIDEO_PATH = "input/contoh_video.mp4"
MODEL_PATH = "yolov5s.pt"
FINAL_AUDIO_PATH = "output/kesimpulan_deteksi.mp3"

# Load model YOLOv5
model = torch.hub.load('yolov5', 'custom', path=MODEL_PATH, source='local')

# Load video
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("❌ Gagal membuka video.")
    exit()

print("🔍 Mendeteksi objek secara real-time... Tekan 'q' untuk keluar.")

# Set untuk menyimpan semua jenis objek yang terdeteksi selama video
all_detected_objects = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Deteksi objek pada frame
    results = model(frame)

    # Ambil hasil deteksi
    for *box, conf, cls in results.xyxy[0]:  # setiap deteksi: box (x1,y1,x2,y2), confidence, class
        x1, y1, x2, y2 = map(int, box)
        label = model.names[int(cls)]
        confidence = float(conf)

        # Simpan jenis objek ke dalam set
        all_detected_objects.add(label)

        # Gambar kotak dan label
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Tampilkan frame
    cv2.imshow("Deteksi Objek", frame)

    # Tekan 'q' untuk keluar manual sebelum video habis
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Setelah video selesai
cap.release()
cv2.destroyAllWindows()

# === Narasi Kesimpulan ===
if all_detected_objects:
    objek_terdeteksi = ", ".join(all_detected_objects)
    jumlah_jenis = len(all_detected_objects)
    summary_text = f"Dalam video ini terdeteksi {jumlah_jenis} jenis objek yaitu {objek_terdeteksi}."
else:
    summary_text = "Tidak ada objek yang berhasil terdeteksi dalam video."

print(f"\n📋 Kesimpulan:\n{summary_text}")

# === Buat suara dari teks kesimpulan ===
tts = gTTS(summary_text, lang='id')
tts.save(FINAL_AUDIO_PATH)
print(f"🔊 Narasi akhir disimpan di: {FINAL_AUDIO_PATH}")
