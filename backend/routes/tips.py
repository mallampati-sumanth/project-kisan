from flask import Blueprint, request, jsonify
from database import db
from models import Tip

tips_bp = Blueprint("tips", __name__)


@tips_bp.get("/api/tips")
def list_tips():
    category = request.args.get("category")
    query = Tip.query
    if category:
        query = query.filter_by(category=category)
    tips = query.order_by(Tip.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tips])


@tips_bp.post("/api/tips")
def add_tip():
    data = request.get_json()
    tip = Tip(category=data["category"], content=data["content"])
    db.session.add(tip)
    db.session.commit()
    return jsonify(tip.to_dict()), 201
