from flask import Flask
from config import Config
from database import db
from routes.weather import weather_bp
from routes.market import market_bp
from routes.forum import forum_bp
from routes.tips import tips_bp
from flask_cors import CORS

# after app = Flask(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config.from_object(Config)

db.init_app(app)

# Register blueprints
app.register_blueprint(weather_bp)
app.register_blueprint(market_bp)
app.register_blueprint(forum_bp)
app.register_blueprint(tips_bp)


@app.route("/")
def index():
    return {"message": "Kisan+ API running"}


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
