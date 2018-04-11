"""Utility file to seed the testdb for Viseat Project."""

from datetime import datetime
from sqlalchemy import func

from model import connect_to_db, db, User, City, Trip, Place, SavedPlace
# from server import app

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

    f = '%d-%m-%Y %H:%M'

    trip1 = Trip(user_id=1, city_id=3, arrival_date=datetime.strptime('15-03-2017 16:15', f),
                 departure_date=datetime.strptime('18-03-2017 8:00', f))
    trip2 = Trip(user_id=2, city_id=1, arrival_date=datetime.strptime('20-03-2017 08:00', f),
                 departure_date=datetime.strptime('22-03-2017 20:00', f))
    trip3 = Trip(user_id=3, city_id=2, arrival_date=datetime.strptime('05-04-2017 14:00', f),
                 departure_date=datetime.strptime('06-04-2017 14:00', f))
    trip4 = Trip(user_id=2, city_id=4, arrival_date=datetime.strptime('09-04-2017 10:00', f),
                 departure_date=datetime.strptime('11-04-2017 08:00', f))

    db.session.add_all([trip1, trip2, trip3, trip4])

    db.session.commit()



if __name__ =='__main__':
    from flask import Flask  # make flask app
    app = Flask(__name__)
    connect_to_db(app)

    db.create_all()  # make the tables
    seed_user()  # seed starter data
    seed_city()
    seed_trip()
