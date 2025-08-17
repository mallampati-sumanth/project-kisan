from flask import Blueprint, request, jsonify
from database import db
from models import Weather

weather_bp = Blueprint("weather", __name__)

@weather_bp.get("/api/weather")
def get_weather():
    q = request.args.get("q", "Vijayawada")
    record = Weather.query.filter_by(location=q).order_by(Weather.created_at.desc()).first()
    if record:
        return jsonify(record.to_dict())
    return jsonify({"message": "No data found", "location": q}), 404

@weather_bp.post("/api/weather")
def add_weather():
    data = request.get_json()
    w = Weather(
        location=data.get("location", "Unknown"),
        temperature=data.get("temperature", 0),
        rainfall=data.get("rainfall", "0.0 mm"),
        humidity=data.get("humidity", 0),
        wind=data.get("wind", "0 km/h"),
        condition=data.get("condition", "Clear"),
    )
    db.session.add(w)
    db.session.commit()
    return jsonify(w.to_dict()), 201
