from flask import Blueprint, request, jsonify
from app.services.room_service import RoomService
from app.models.room import Room

room_bp = Blueprint("room", __name__)
@room_bp.route("/get-room", methods=["GET"])
def get_rooms():
    return jsonify({"rooms": RoomService.get_available_rooms()}), 200
@room_bp.route("/add-room", methods=["POST"])
def add_room():
    data = request.get_json() or {}
    required = ["roomId","floor","guestNum","beds","price"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400
    if Room.query.filter_by(roomId=data["roomId"]).first():
        return jsonify({"error": "Room exists"}), 409
    RoomService.add_room(data)
    return jsonify({"rooms": RoomService.get_all_rooms()}), 200
@room_bp.route("/booking", methods=["POST"])
def booking():
    data = request.get_json() or {}
    room_id = data.get("roomId")
    if not room_id:
        return jsonify({"error": "roomId required"}), 400
    room = Room.query.filter_by(roomId=room_id).first()
    if not room:
        return jsonify({"error": "Not found"}), 404
    if room.is_booked:
        return jsonify({"error": "Already booked"}), 409
    RoomService.book_room(room_id)
    return jsonify({"message": "Booked"}), 200
