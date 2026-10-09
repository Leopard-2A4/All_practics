from flask import request, jsonify
from sqlalchemy import text
from schemas import Session
from models import Coffee, User
from main import app


@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json() or {}
    session = Session()
    try:
        user = User(
            name=data["name"],
            has_sale=data.get("has_sale", False),
            address=data.get("address", {}),
            coffee_id=data.get("coffee_id"),
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return jsonify(user.to_dict()), 201
    finally:
        session.close()


@app.route("/coffee/search", methods=["GET"])
def search_coffee():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"error": "q is required"}), 400

    session = Session()
    try:
        row = session.execute(
            text("""
                SELECT id, title, category, description, reviews
                FROM coffee
                WHERE to_tsvector('english', title) @@ plainto_tsquery('english', :q)
                LIMIT 1
            """),
            {"q": q},
        ).first()

        if not row:
            return jsonify({"error": "Coffee not found"}), 404

        return jsonify({
            "id": row.id,
            "title": row.title,
            "category": row.category,
            "description": row.description,
            "reviews": row.reviews,
        })
    finally:
        session.close()


@app.route("/coffee/reviews", methods=["GET"])
def unique_reviews():
    session = Session()
    try:
        rows = session.query(Coffee.reviews).all()
        uniq = set()
        for row in rows:
            if row[0]:
                uniq.update(row[0])
        return jsonify({"reviews": sorted(uniq)})
    finally:
        session.close()


@app.route("/users/by-country", methods=["GET"])
def users_by_country():
    country = request.args.get("country", "").strip()
    if not country:
        return jsonify({"error": "country is required"}), 400

    session = Session()
    try:
        rows = session.execute(
            text("""
                SELECT id, name, has_sale, address, coffee_id
                FROM users
                WHERE address->>'country' = :country
            """),
            {"country": country},
        ).fetchall()

        return jsonify({
            "users": [
                {
                    "id": r.id,
                    "name": r.name,
                    "has_sale": r.has_sale,
                    "address": r.address,
                    "coffee_id": r.coffee_id,
                }
                for r in rows
            ]
        })
    finally:
        session.close()