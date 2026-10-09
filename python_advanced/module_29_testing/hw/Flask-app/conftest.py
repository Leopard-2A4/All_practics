import pytest
from application import create_app
from models import db as _db, Client, Parking


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    with app.app_context():
        _db.create_all()

        client = Client(
            name="Ivan",
            surname="Ivanov",
            credit_card="1234567890123456",
            car_number="A123BC77",
        )
        parking = Parking(
            address="Minsk, Lenina 1",
            opened=True,
            count_places=10,
            count_available_places=10,
        )
        _db.session.add_all([client, parking])
        _db.session.commit()

    yield app

    with app.app_context():
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db(app):
    with app.app_context():
        yield _db
        _db.session.rollback()