from flask import Flask, request, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os
import json

app = Flask(__name__)

# ✅ Firebase setup (Render + Local both supported)
if os.getenv("FIREBASE_KEY"):
    firebase_key = json.loads(os.environ["FIREBASE_KEY"])
    cred = credentials.Certificate(firebase_key)
else:
    cred = credentials.Certificate("firebase_key.json")

firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def home():
    return render_template('index.html')

# ✅ Mark attendance
@app.route('/mark', methods=['POST'])
def mark_attendance():
    data = request.json

    name = data['name']
    status = data['status']

    db.collection('attendance').add({
        'name': name,
        'status': status,
        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    return jsonify({"message": "Attendance Marked"})

# ✅ Get records
@app.route('/records', methods=['GET'])
def get_records():
    records = db.collection('attendance').stream()
    
    data = []
    for r in records:
        data.append(r.to_dict())

    return jsonify(data)

# ✅ Delete all data
@app.route('/delete', methods=['POST'])
def delete_all():
    docs = db.collection('attendance').stream()
    for doc in docs:
        doc.reference.delete()

    return jsonify({"message": "All data deleted"})

# ✅ Run app (Render compatible)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)