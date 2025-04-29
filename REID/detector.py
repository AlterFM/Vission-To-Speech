from ultralytics import YOLO
import cv2

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# Whitelist barang yang dianggap bawaan orang
allowed_items = {
    "backpack", "handbag", "suitcase", "bottle",
    "cell phone", "laptop", "book", "umbrella"
}

def calculate_overlap(boxA, boxB):
    """Hitung persentase overlap area boxA dalam boxB"""
    ax, ay, aw, ah = boxA
    bx, by, bw, bh = boxB

    # Hitung koordinat sisi-sisi
    ax1, ay1 = ax - aw/2, ay - ah/2
    ax2, ay2 = ax + aw/2, ay + ah/2
    bx1, by1 = bx - bw/2, by - bh/2
    bx2, by2 = bx + bw/2, by + bh/2

    # Hitung overlap
    x_left = max(ax1, bx1)
    y_top = max(ay1, by1)
    x_right = min(ax2, bx2)
    y_bottom = min(ay2, by2)

    if x_right < x_left or y_bottom < y_top:
        return 0.0  # Tidak overlap

    overlap_area = (x_right - x_left) * (y_bottom - y_top)
    areaA = (ax2 - ax1) * (ay2 - ay1)

    return overlap_area / areaA  # Persentase overlap areaA dalam areaB

def detect_objects(video_path):
    cap = cv2.VideoCapture(video_path)
    detected_items = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(frame, verbose=False)
        boxes = results[0].boxes.xywh.cpu().numpy()
        classes = results[0].boxes.cls.cpu().numpy()
        
        persons = []
        objects = []

        # Pisahkan person dan objek
        for i, class_id in enumerate(classes):
            label = model.names[int(class_id)]
            box = boxes[i]

            if label == 'person':
                persons.append(box)
            elif label in allowed_items:
                objects.append((box, label))

        # Untuk setiap orang
        for person_box in persons:
            px, py, pw, ph = person_box
            # Gambar kotak orang
            cv2.rectangle(frame, 
                          (int(px - pw/2), int(py - ph/2)), 
                          (int(px + pw/2), int(py + ph/2)), 
                          (0, 255, 0), 2)

            for obj_box, label in objects:
                overlap = calculate_overlap(obj_box, person_box)

                if overlap > 0.5:  # Hanya jika overlap lebih dari 50%
                    ox, oy, ow, oh = obj_box
                    detected_items.append(label)

                    # Gambar kotak barang
                    cv2.rectangle(frame, 
                                  (int(ox - ow/2), int(oy - oh/2)), 
                                  (int(ox + ow/2), int(oy + oh/2)), 
                                  (255, 0, 0), 2)
                    # Label barang
                    cv2.putText(frame, label, 
                                (int(ox), int(oy - 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                0.6, (255, 0, 0), 2)

        cv2.imshow('Detection', frame)

        # Exit loop kalau tekan 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return list(set(detected_items))
