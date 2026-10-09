import pytest
from models import Client, Parking, Client_Parking
from factories import ClientFactory, ParkingFactory


@pytest.mark.parametrize(
    "method,url",
    [
        ("get", "/clients"),
        ("get", "/clients/1"),
    ],
)
def test_get_methods_return_200(client, method, url):
    response = getattr(client, method)(url)
    assert response.status_code == 200


def test_create_client(client, db):
    before = db.session.query(Client).count()

    response = client.post(
        "/clients",
        json={
            "name": "Petr",
            "surname": "Petrov",
            "credit_card": "1111222233334444",
            "car_number": "B777BB77",
        },
    )

    assert response.status_code == 201
    assert db.session.query(Client).count() == before + 1

    created = db.session.query(Client).order_by(Client.id.desc()).first()
    assert created.id is not None
    assert created.name == "Petr"
    assert created.surname == "Petrov"


def test_create_parking(client, db):
    before = db.session.query(Parking).count()

    response = client.post(
        "/parkings",
        json={
            "address": "Minsk, Pushkina 10",
            "count_places": 5,
        },
    )

    assert response.status_code == 201
    assert db.session.query(Parking).count() == before + 1

    created = db.session.query(Parking).order_by(Parking.id.desc()).first()
    assert created.id is not None
    assert created.address == "Minsk, Pushkina 10"
    assert created.count_places == 5
    assert created.count_available_places == 5


@pytest.mark.parking
def test_start_parking(client, db):
    client_obj = db.session.query(Client).filter_by(name="Ivan").first()
    parking_obj = db.session.query(Parking).filter_by(address="Minsk, Lenina 1").first()

    before_places = parking_obj.count_available_places

    response = client.post(
        "/client_parkings",
        json={
            "client_id": client_obj.id,
            "parking_id": parking_obj.id,
        },
    )

    assert response.status_code == 201

    db.session.refresh(parking_obj)
    assert parking_obj.count_available_places == before_places - 1

    log = db.session.query(Client_Parking).filter_by(
        client_id=client_obj.id,
        parking_id=parking_obj.id,
        time_out=None,
    ).first()
    assert log is not None
    assert log.time_in is not None


@pytest.mark.parking
def test_stop_parking(client, db):
    client_obj = db.session.query(Client).filter_by(name="Ivan").first()
    parking_obj = db.session.query(Parking).filter_by(address="Minsk, Lenina 1").first()

    existing_log = db.session.query(Client_Parking).filter_by(
        client_id=client_obj.id,
        parking_id=parking_obj.id,
        time_out=None,
    ).first()

    if existing_log is None:
        start_response = client.post(
            "/client_parkings",
            json={
                "client_id": client_obj.id,
                "parking_id": parking_obj.id,
            },
        )
        assert start_response.status_code == 201

    db.session.refresh(parking_obj)
    places_before_delete = parking_obj.count_available_places

    response = client.delete(
        "/client_parkings",
        json={
            "client_id": client_obj.id,
            "parking_id": parking_obj.id,
        },
    )

    assert response.status_code == 200

    db.session.refresh(parking_obj)
    assert parking_obj.count_available_places == places_before_delete + 1

    log = db.session.query(Client_Parking).filter_by(
        client_id=client_obj.id,
        parking_id=parking_obj.id,
    ).order_by(Client_Parking.time_in.desc()).first()

    assert log.time_out is not None
    assert log.time_out >= log.time_in


def test_create_client_with_factory(client, db):
    before = db.session.query(Client).count()

    obj = ClientFactory()
    db.session.commit()

    assert obj.id is not None
    assert db.session.query(Client).count() == before + 1

    response = client.post(
        "/clients",
        json={
            "name": obj.name,
            "surname": obj.surname,
            "credit_card": obj.credit_card,
            "car_number": obj.car_number,
        },
    )
    assert response.status_code == 201


def test_create_parking_with_factory(client, db):
    before = db.session.query(Parking).count()

    obj = ParkingFactory(count_places=7, count_available_places=7)
    db.session.commit()

    assert obj.id is not None
    assert db.session.query(Parking).count() == before + 1

    response = client.post(
        "/parkings",
        json={
            "address": obj.address,
            "count_places": obj.count_places,
        },
    )
    assert response.status_code == 201