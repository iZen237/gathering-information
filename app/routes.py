import os
from flask import Blueprint, render_template, request, jsonify
from werkzeug.utils import secure_filename
import cv2

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")


@main.route("/api/search", methods=["POST"])
def search():
    name = request.form.get("name", "")
    email = request.form.get("email", "")
    phone = request.form.get("phone", "")
    username = request.form.get("username", "")

    image_file = request.files.get("image")
    bbox = None

    if image_file:
        filename = secure_filename(image_file.filename)
        save_path = os.path.join(main.root_path, '..', 'uploads', filename)
        image_file.save(save_path)

        # Detect face (optional)
        img = cv2.imread(save_path)
        if img is not None:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = cascade.detectMultiScale(gray, 1.1, 5)
            if len(faces) > 0:
                x, y, w, h = faces[0]
                h_img, w_img = img.shape[:2]
                bbox = {
                    "left": round((x / w_img) * 100, 2),
                    "top": round((y / h_img) * 100, 2),
                    "width": round((w / w_img) * 100, 2),
                    "height": round((h / h_img) * 100, 2)
                }

    return jsonify({
        "targetName": name or username or email or "Unknown Target",
        "emails": [email] if email else ["demo@example.com"],
        "phones": [phone] if phone else ["+237 699 99 99 99"],
        "links": ["https://twitter.com/demo_user", "https://linkedin.com/in/demo-user"],
        "matches": [
            {"name": "John Doe", "source": "Twitter", "handle": "@johndoe", "confidence": 87},
            {"name": "Jonathan D.", "source": "LinkedIn", "handle": "jonathan-doe", "confidence": 74}
        ],
        "bbox": bbox
    })
