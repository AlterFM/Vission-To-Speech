import cv2
from ultralytics import YOLO
from gtts import gTTS
import os

# === SETUP ===
VIDEO_PATH = "input/video_kamu.mp4"
MODEL_PATH = "yolov8n.pt"  # YOLOv8 model ringan
OUTPUT_AUDIO_PATH = "output/hasil_deteksi.mp3"

# Load model YOLOv8
model = YOLO(MODEL_PATH)

# Buka video
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("❌ Gagal membuka video.")
    exit()

print("🔍 Mendeteksi objek secara real-time... Tekan 'q' untuk keluar.")

detected_labels = set()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Deteksi objek
    results = model.predict(frame, device="cpu", verbose=False)

    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls_id = int(box.cls)
            label = model.names[cls_id]
            confidence = float(box.conf)

            # Simpan label unik
            detected_labels.add(label)

            # Ambil koordinat dan gambar kotak
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{label} {confidence:.2f}', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Tampilkan frame
    cv2.imshow("Deteksi Objek", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# === KESIMPULAN AKHIR ===
if detected_labels:
    sentence = "Dalam video terdeteksi objek seperti " + ", ".join(sorted(detected_labels)) + "."
else:
    sentence = "Tidak ada objek yang berhasil terdeteksi dalam video."

print("✅ Narasi:", sentence)

# Konversi teks ke suara
tts = gTTS(sentence, lang='id')
tts.save(OUTPUT_AUDIO_PATH)
print(f"🔊 Audio disimpan di: {OUTPUT_AUDIO_PATH}")
