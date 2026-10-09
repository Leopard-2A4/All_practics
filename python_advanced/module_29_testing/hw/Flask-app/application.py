from flask import Flask, jsonify, request
from datetime import datetime
from models import db, Client, Parking, Client_Parking


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    def get_json_data():
        data = request.get_json(silent=True)
        if data is None:
            return None, (jsonify({"error": "Request body must be valid JSON"}), 400)
        return data, None

    @app.route("/clients", methods=["GET"])
    def get_clients():
        clients = db.session.query(Client).all()
        return jsonify([client.to_json() for client in clients]), 200

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def get_client(client_id: int):
        client = db.session.get(Client, client_id)
        if not client:
            return jsonify({"error": "Client not found"}), 404
        return jsonify(client.to_json()), 200

    @app.route("/clients", methods=["POST"])
    def create_client():
        data, error_response = get_json_data()
        if error_response:
            return error_response

        name = data.get("name")
        surname = data.get("surname")
        credit_card = data.get("credit_card")
        car_number = data.get("car_number")

        if not name or not surname:
            return jsonify({"error": "name and surname are required"}), 400

        new_client = Client(
            name=name,
            surname=surname,
            credit_card=credit_card,
            car_number=car_number,
        )
        db.session.add(new_client)
        db.session.commit()

        return jsonify(new_client.to_json()), 201

    @app.route("/parkings", methods=["POST"])
    def create_parking():
        data, error_response = get_json_data()
        if error_response:
            return error_response

        address = data.get("address")
        count_places = data.get("count_places")

        if not address:
            return jsonify({"error": "address is required"}), 400

        try:
            count_places = int(count_places)
        except (TypeError, ValueError):
            return jsonify({"error": "count_places must be an integer"}), 400

        if count_places < 1:
            return jsonify({"error": "count_places must be greater than 0"}), 400

        new_parking = Parking(
            address=address,
            opened=True,
            count_places=count_places,
            count_available_places=count_places,
        )
        db.session.add(new_parking)
        db.session.commit()

        return jsonify(new_parking.to_json()), 201

    @app.route("/client_parkings", methods=["POST"])
    def start_parking():
        data, error_response = get_json_data()
        if error_response:
            return error_response

        client_id = data.get("client_id")
        parking_id = data.get("parking_id")

        client = db.session.get(Client, client_id)
        parking = db.session.get(Parking, parking_id)

        if not client:
            return jsonify({"error": "Client not found"}), 404
        if not parking:
            return jsonify({"error": "Parking not found"}), 404
        if not parking.opened:
            return jsonify({"error": "Parking is closed"}), 400
        if parking.count_available_places <= 0:
            return jsonify({"error": "No available places"}), 400

        active_parking = (
            db.session.query(Client_Parking)
            .filter(
                Client_Parking.client_id == client_id,
                Client_Parking.parking_id == parking_id,
                Client_Parking.time_out.is_(None),
            )
            .first()
        )
        if active_parking:
            return jsonify({"error": "Client is already parked here"}), 400

        parking.count_available_places -= 1
        if parking.count_available_places == 0:
            parking.opened = False

        record = Client_Parking(
            client_id=client_id,
            parking_id=parking_id,
            time_in=datetime.utcnow(),
        )
        db.session.add(record)
        db.session.commit()

        return jsonify(
            {
                "message": "Client parked successfully",
                "client_id": client_id,
                "parking_id": parking_id,
                "time_in": record.time_in.isoformat(),
            }
        ), 201

    @app.route("/client_parkings", methods=["DELETE"])
    def stop_parking():
        data, error_response = get_json_data()
        if error_response:
            return error_response

        client_id = data.get("client_id")
        parking_id = data.get("parking_id")

        client = db.session.get(Client, client_id)
        parking = db.session.get(Parking, parking_id)

        if not client:
            return jsonify({"error": "Client not found"}), 404
        if not parking:
            return jsonify({"error": "Parking not found"}), 404

        record = (
            db.session.query(Client_Parking)
            .filter(
                Client_Parking.client_id == client_id,
                Client_Parking.parking_id == parking_id,
                Client_Parking.time_out.is_(None),
            )
            .order_by(Client_Parking.time_in.desc())
            .first()
        )

        if not record:
            return jsonify({"error": "Active parking record not found"}), 404

        if not client.credit_card:
            return jsonify({"error": "Client has no linked credit card"}), 400

        record.time_out = datetime.utcnow()
        if record.time_out < record.time_in:
            return jsonify({"error": "time_out cannot be earlier than time_in"}), 400

        parking.count_available_places += 1
        if parking.count_available_places > 0:
            parking.opened = True

        db.session.commit()

        return jsonify(
            {
                "message": "Client left parking successfully",
                "client_id": client_id,
                "parking_id": parking_id,
                "time_in": record.time_in.isoformat() if record.time_in else None,
                "time_out": record.time_out.isoformat() if record.time_out else None,
            }
        ), 200

    return app