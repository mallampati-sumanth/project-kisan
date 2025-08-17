from datetime import datetime
from database import db


# --- Weather ---
class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(120), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    rainfall = db.Column(db.String(50))
    humidity = db.Column(db.Integer)
    wind = db.Column(db.String(50))
    condition = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# --- Market Prices ---
class MarketPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(120))
    trend = db.Column(db.String(20))  # "up" / "down" / "neutral"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# --- Forum Posts ---
class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship(
        "ForumComment", backref="post", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "comments": [c.to_dict() for c in self.comments],
        }


class ForumComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("forum_post.id"), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# --- Tips (Farming / Diagnosis) ---
class Tip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(
        db.String(120), nullable=False
    )  # "fertilizer", "pest", "general"
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
