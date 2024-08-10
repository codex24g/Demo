from flask import Flask, Response, render_template
import tensorflow as tf
import numpy as np
import mediapipe as mp
import json
import cv2

# Load the model
try:
    model = tf.keras.models.load_model('staff_mobilenet_v2_model.h5')
except Exception as e:
    print(f"Error loading model: {e}")
    raise

# Load class names and their attributes
try:
    with open('class_names.json') as f:
        class_names = json.load(f)
except Exception as e:
    print(f"Error loading class names: {e}")
    raise

app = Flask(__name__)

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.2)

def process_frame(frame):
    try:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(frame_rgb)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                h, w, _ = frame.shape
                bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
                cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 2)
                
                face_roi = frame[bbox[1]:bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2]]
                if face_roi.size > 0:
                    face_roi_resized = cv2.resize(face_roi, (224, 224))
                    face_roi_normalized = face_roi_resized / 255.0
                    face_roi_expanded = np.expand_dims(face_roi_normalized, axis=0)
                    
                    predictions = model.predict(face_roi_expanded)
                    predicted_class = np.argmax(predictions, axis=1)[0]
                    
                    class_name = list(class_names.keys())[predicted_class]
                    staff_info = class_names[class_name]
                    
                    cv2.putText(frame, f'Name: {class_name}', (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    cv2.putText(frame, f'Drink: {staff_info["drink_preference"]}', (bbox[0], bbox[1] + bbox[3] + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    cv2.putText(frame, f'Diet: {staff_info["dietary_restrictions"]}', (bbox[0], bbox[1] + bbox[3] + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            return b''
        
        return buffer.tobytes()
    except Exception as e:
        print(f"Error processing frame: {e}")
        return b''

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        frame = process_frame(frame)
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error running Flask app: {e}")
