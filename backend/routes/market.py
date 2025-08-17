from flask import Blueprint, request, jsonify
from database import db
from models import MarketPrice

market_bp = Blueprint("market", __name__)


@market_bp.get("/api/market")
def list_prices():
    prices = MarketPrice.query.order_by(MarketPrice.created_at.desc()).all()
    return jsonify([p.to_dict() for p in prices])


@market_bp.post("/api/market")
def add_price():
    data = request.get_json()
    p = MarketPrice(
        crop=data["crop"],
        price=data["price"],
        location=data.get("location", "Unknown"),
        trend=data.get("trend", "neutral"),
    )
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201
