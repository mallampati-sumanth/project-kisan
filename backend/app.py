import os
from datetime import datetime
from uuid import uuid4
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Config
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# In-memory stores (swap to DB later)
POSTS = []  # {id, title, content, user_id, timestamp, likes, image_path}
TIPS = {
    "irrigation": [
        {
            "icon": "💧",
            "title": "Water Schedule",
            "content": "Irrigate early morning for minimal evaporation.",
        },
        {
            "icon": "🧪",
            "title": "Soil Moisture",
            "content": "Use finger test 5–7cm depth before watering.",
        },
    ],
    "sowing": [
        {
            "icon": "🌱",
            "title": "Seed Treatment",
            "content": "Treat seeds with Trichoderma for damping-off.",
        },
    ],
    "harvesting": [
        {
            "icon": "🌾",
            "title": "Harvest Timing",
            "content": "Target grain moisture ~20–25% before harvest.",
        },
    ],
}


def ok(data=None, **kw):
    res = {"success": True}
    if data is not None:
        res["data"] = data
    res.update(kw)
    return jsonify(res)


def fail(msg="Error", code=400):
    return jsonify({"success": False, "error": msg}), code


@app.get("/api/health")
def health():
    return ok({"status": "ok", "time": datetime.utcnow().isoformat()})


# --- Weather (mock; wire real API later) ---
@app.get("/api/weather")
def weather():
    # Optional: location from query ?q=City
    q = request.args.get("q", "Vijayawada")  # use ?q=CityName
    data = {
        "location": q,
        "temperature": 30,
        "rainfall": "0.0 mm",
        "humidity": 55,
        "wind": "8 km/h",
        "forecast": [
            {"day": "Today", "icon": "⛅", "temp": 30, "condition": "Partly Cloudy"},
            {"day": "Tomorrow", "icon": "🌧️", "temp": 27, "condition": "Light Rain"},
            {"day": "Day After", "icon": "☀️", "temp": 31, "condition": "Sunny"},
        ],
    }
    return jsonify(data), 200


# --- Tips ---
@app.get("/api/tips")
def tips():
    return ok(TIPS)


# --- Forum ---
@app.get("/api/posts")
def get_posts():
    return ok(list(reversed(POSTS)))


@app.post("/api/posts")
def create_post():
    body = request.get_json(force=True)
    title = (body.get("title") or "").strip()
    content = (body.get("content") or "").strip()
    user_id = body.get("user_id", "guest")
    if not title or not content:
        return fail("Title and content are required")
    post = {
        "id": str(uuid4()),
        "title": title,
        "content": content,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "likes": 0,
        "image_path": None,
    }
    POSTS.append(post)
    return ok(post)


@app.post("/api/posts/<post_id>/like")
def like_post(post_id):
    for p in POSTS:
        if p["id"] == post_id:
            p["likes"] += 1
            return ok({"likes": p["likes"]})
    return fail("Post not found", 404)


# --- Diagnosis upload (mock AI) ---
ALLOWED = {"png", "jpg", "jpeg", "webp"}


def allowed_file(fn: str) -> bool:
    return "." in fn and fn.rsplit(".", 1)[1].lower() in ALLOWED


@app.post("/api/diagnosis")
def diagnosis():
    if "image" not in request.files:
        return fail("No image")
    f = request.files["image"]
    if f.filename == "":
        return fail("No filename")
    if not allowed_file(f.filename):
        return fail("Unsupported type")
    filename = secure_filename(f"{uuid4()}_{f.filename}")
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    f.save(path)

    # Mock AI result
    result = {
        "image_url": f"/api/uploads/{filename}",
        "diagnosis": {
            "disease": "Early blight (possible)",
            "confidence": 87.3,
            "severity": "Moderate",
            "remedy": "Remove infected leaves, improve airflow, and apply copper-based fungicide as labeled.",
        },
    }
    return ok(result)


@app.get("/api/uploads/<path:fname>")
def serve_upload(fname):
    return send_from_directory(app.config["UPLOAD_FOLDER"], fname)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)
