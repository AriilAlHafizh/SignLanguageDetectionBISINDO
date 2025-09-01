import cv2
import mediapipe as mp
import numpy as np
import pickle
import tensorflow as tf
from collections import deque
from flask import Flask, render_template, Response, jsonify

app = Flask(__name__)

# Load model dan label encoder
model = tf.keras.models.load_model("models/sign_language_model_75.h5")
with open("models/label_encoder_75.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Inisialisasi MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

# Buffer untuk menyimpan 30 frame
sequence = deque(maxlen=30)
last_prediction = ""   # hasil prediksi terakhir
last_accuracy = 0.0    # akurasi prediksi terakhir

# Fungsi untuk memproses setiap frame video
def process_frames():
    global sequence, last_prediction, last_accuracy
    cap = cv2.VideoCapture(0)

    # Atur resolusi lebih kecil biar ringan
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Skip frame biar ga terlalu berat (proses 1 dari 2 frame)
        if frame_count % 2 != 0:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        
        frame_features = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks[:2]:
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.extend([lm.x, lm.y])
                frame_features.extend(landmarks)

                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=3),
                    mp_drawing.DrawingSpec(color=(0,0,255), thickness=2)
                )
        
        if len(frame_features) < 84:
            frame_features.extend([0.0] * (84 - len(frame_features)))
        
        frame_features = np.array(frame_features)
        sequence.append(frame_features)
        
        # Prediksi hanya tiap 10 frame sekali
        if len(sequence) == 30 and frame_count % 10 == 0:
            input_data = np.array(sequence).reshape(1, 30, 84)
            prediction = model.predict(input_data, verbose=0)
            pred_class = np.argmax(prediction)
            last_prediction = label_encoder.inverse_transform([pred_class])[0]
            last_accuracy = float(np.max(prediction))

        # cv2.putText(frame, f"Prediksi: {last_prediction}", (10, 40),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Encode dengan kualitas lebih rendah biar enteng
        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
        if not ret:
            continue
        
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(process_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Endpoint baru untuk API prediksi
@app.route('/prediction')
def prediction():
    global last_prediction, last_accuracy
    return jsonify({
        "label": last_prediction,
        "accuracy": last_accuracy
    })

if __name__ == '__main__':
    app.run(debug=True)
