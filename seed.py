"""Utility file to seed the testdb for Viseat Project."""

from datetime import datetime
from sqlalchemy import func

from model import connect_to_db, db, User, City, Trip, Place, SavedPlace


def seed_user():
    """Seed users table."""
    # This function will demonstrate how to seed user table.

    duygu = User(fname="Duygu", lname="Ebcim", email="duygu@gmail.com",
                 password="duckface")
    heather = User(fname="Heather", lname="Mahan", email="heather@gmail.com",
                   password="heatherm")
    murat = User(fname="Murat", lname="Ozgul", email="murat@yahoo.com",
                 password="murato")
    romain = User(fname="Romain", lname="Komorn", email="romain@gmail.com",
                  password="romaink")

    db.session.add_all([duygu, heather, murat, romain])

    db.session.commit()


def seed_city():
    """Seed  cities table."""
    # This function will demonstrate how to seed user table.

    paris = City(name="Paris")
    london = City(name="London")
    barcelona = City(name="Barcelona")
    istanbul = City(name="Istanbul")

    db.session.add_all([paris, london, barcelona, istanbul])

    db.session.commit()


def seed_trip():
    """Seed trips table."""
    # This function will demonstrate how to seed trip table.

    trip1 = Trip(user_id=1, city_id=3, arrival_date=(2017, 03, 15, 16, 15),
                 departure_date=(2017, 03, 18, 8, 00))
    trip2 = Trip(user_id=2, city_id=1, arrival_date=(2017, 03, 20, 8, 00),
                 departure_date=(2017, 03, 22, 20, 00))
    trip3 = Trip(user_id=3, city_id=2, arrival_date=(2017, 04, 5, 14, 00),
                 departure_date=(2017, 04, 6, 14, 00))
    trip4 = Trip(user_id=2, city_id=4, arrival_date=(2017, 04, 9, 10, 00),
                 departure_date=(2017, 04, 11, 8, 00))

    db.session.add_all([trip1, trip2, trip3, trip4])

    db.session.commit()



if __name__ =='__main__':
    from flask import Flask #make flask app
    app = Flask(__name__)
    connect_to_db(app)

    db.create_all() #make the tables
    seed_user() # seed starter data
    seed_city()
    seed_trip()
