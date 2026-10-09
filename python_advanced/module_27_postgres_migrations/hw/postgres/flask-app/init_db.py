import random
import requests
from sqlalchemy.exc import OperationalError
from schemas import engine, Session, Base
import models
import time


def wait_for_db():
    for _ in range(20):
        try:
            with engine.connect():
                return
        except OperationalError:
            time.sleep(2)
    raise RuntimeError("Database is not available")


def init_db():
    wait_for_db()
    Base.metadata.create_all(bind=engine)


def seed_data():
    session = Session()
    try:
        if session.query(models.Coffee).first() is not None:
            print("Data already exists, skipping seed.")
            return

        coffee_response = requests.get(
            "https://dummyjson.com/products/search?q=coffee",
            timeout=15,
        )
        coffee_data = coffee_response.json()
        product = coffee_data.get("products", [None])[0]

        if not product:
            print("No coffee product found.")
            return

        reviews_list = [
            r.get("comment", "")
            for r in product.get("reviews", [])
            if r.get("comment")
        ]

        coffee = models.Coffee(
            title=product.get("title", "Coffee"),
            category=product.get("category", ""),
            description=product.get("description", ""),
            reviews=reviews_list,
        )
        session.add(coffee)
        session.commit()

        coffee_id = coffee.id

        users_response = requests.get("https://dummyjson.com/users?limit=10", timeout=15)
        users_data = users_response.json()

        for user_data in users_data.get("users", [])[:10]:
            address_data = user_data.get("address", {})
            user = models.User(
                name=f"{user_data.get('firstName', '')} {user_data.get('lastName', '')}".strip(),
                has_sale=random.choice([True, False]),
                address={
                    "address": address_data.get("address", ""),
                    "city": address_data.get("city", ""),
                    "state": address_data.get("state", ""),
                    "country": address_data.get("country", ""),
                    "zipcode": address_data.get("postalCode", address_data.get("zipcode", "")),
                },
                coffee_id=coffee_id,
            )
            session.add(user)

        session.commit()
        print("Seed completed.")
    finally:
        session.close()


if __name__ == "__main__":
    init_db()
    seed_data()