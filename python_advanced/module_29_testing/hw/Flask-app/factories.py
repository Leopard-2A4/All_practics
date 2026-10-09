import factory
from factory.alchemy import SQLAlchemyModelFactory
from models import db, Client, Parking


class ClientFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = factory.Faker("credit_card_number")
    car_number = factory.Faker("bothify", text="?#??##")


class ParkingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    address = factory.Faker("address")
    opened = factory.Faker("pybool")
    count_places = factory.Faker("random_int", min=1, max=100)
    count_available_places = factory.LazyAttribute(lambda obj: obj.count_places)