from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roomId = db.Column(db.Integer, unique=True, nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    guestNum = db.Column(db.Integer, nullable=False)
    beds = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    is_booked = db.Column(db.Boolean, default=False)
    def to_dict(self):
        return {"roomId": self.roomId,"floor": self.floor,"guestNum": self.guestNum,"beds": self.beds,"price": self.price}
