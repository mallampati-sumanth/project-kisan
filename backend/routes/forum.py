from flask import Blueprint, request, jsonify
from database import db
from models import ForumPost, ForumComment

forum_bp = Blueprint("forum", __name__)


@forum_bp.get("/api/forum")
def list_posts():
    posts = ForumPost.query.order_by(ForumPost.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts])


@forum_bp.post("/api/forum")
def add_post():
    data = request.get_json()
    post = ForumPost(
        author=data["author"], title=data["title"], content=data["content"]
    )
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201


@forum_bp.post("/api/forum/<int:post_id>/comment")
def add_comment(post_id):
    data = request.get_json()
    comment = ForumComment(
        post_id=post_id, author=data["author"], content=data["content"]
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201
