from app.models.room import Room, db
class RoomService:
    @staticmethod
    def get_available_rooms():
        return [r.to_dict() for r in Room.query.filter_by(is_booked=False).all()]
    @staticmethod
    def get_all_rooms():
        return [r.to_dict() for r in Room.query.all()]
    @staticmethod
    def add_room(data):
        room = Room(
            roomId=int(data["roomId"]),
            floor=int(data["floor"]),
            guestNum=int(data["guestNum"]),
            beds=int(data["beds"]),
            price=int(data["price"])
        )
        db.session.add(room)
        db.session.commit()
    @staticmethod
    def book_room(room_id):
        room = Room.query.filter_by(roomId=room_id, is_booked=False).first()
        if room:
            room.is_booked = True
            db.session.commit()
            return True
        return False
