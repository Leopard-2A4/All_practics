from flask import Flask
from config import Config
from app.models.room import db
from app.routes.room_routes import room_bp
import os
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    os.makedirs("instance", exist_ok=True)
    db.init_app(app)
    app.register_blueprint(room_bp)
    with app.app_context():
        db.create_all()
        from app.models.room import Room
        if not Room.query.first():
            db.session.add_all([
                Room(roomId=1, floor=2, guestNum=1, beds=1, price=2000),
                Room(roomId=2, floor=1, guestNum=2, beds=1, price=2500)
            ])
            db.session.commit()
    return app
