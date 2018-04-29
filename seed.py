"""Utility file to seed the testdb for Viseat Project."""

from datetime import datetime
from sqlalchemy import func

from model import connect_to_db, db, User, City, Trip, Place, SavedPlace
# from server import app

def seed_user():
    """Seed users table."""
    # This function will demonstrate how to seed user table.

    duygu = User(username="dygduck", fname="Duygu", lname="Ebcim",
        email="duygu@gmail.com", password="duckface")
    heather = User(username="unicorn", fname="Heather", lname="Mahan",
        email="heather@gmail.com", password="heatherm")
    murat = User(username="murti", fname="Murat", lname="Ozgul",
        email="murat@yahoo.com", password="murato")
    romain = User(username="lyon", fname="Romain", lname="Komorn",
        email="romain@gmail.com", password="romaink")

    db.session.add_all([duygu, heather, murat, romain])

    db.session.commit()


def seed_city():
    """Seed  cities table."""
    # This function will demonstrate how to seed city table.

    paris = City(city_name="Paris, France")
    london = City(city_name="London, United Kingdom")
    barcelona = City(city_name="Barcelona, Spain")
    istanbul = City(city_name="Istanbul, Turkey")
    madrid = City(city_name="Madrid, Spain")
    nice = City(city_name="Nice, France")
    berlin = City(city_name="Berlin, Germany")
    hongkong = City(city_name="Hong Kong, Hong Kong")
    singapore = City(city_name="Singapore, Singapore")
    sanfrancisco = City(city_name="San Francisco, United States")
    newyork = City(city_name="New York, United States")
    losangeles = City(city_name="Los Angeles, United States")
    chicago = City(city_name="Chicago, United States")


    db.session.add_all([paris, london, barcelona, istanbul, madrid, nice, berlin,
        hongkong, singapore, sanfrancisco, newyork, losangeles, chicago])

    db.session.commit()


# def seed_trip():
#     """Seed trips table."""
#     # This function will demonstrate how to seed trip table.

#     f = '%d-%m-%Y %H:%M'

#     trip1 = Trip(user_id=1, city_id=3, arrival_date=datetime.strptime('15-03-2017 16:15', f),
#                  departure_date=datetime.strptime('18-03-2017 08:00', f))
#     trip2 = Trip(user_id=2, city_id=1, arrival_date=datetime.strptime('20-03-2017 08:00', f),
#                  departure_date=datetime.strptime('22-03-2017 20:00', f))
#     trip3 = Trip(user_id=3, city_id=2, arrival_date=datetime.strptime('05-04-2017 14:00', f),
#                  departure_date=datetime.strptime('06-04-2017 14:00', f))
#     trip4 = Trip(user_id=2, city_id=4, arrival_date=datetime.strptime('09-04-2017 10:00', f),
#                  departure_date=datetime.strptime('11-04-2017 08:00', f))

#     db.session.add_all([trip1, trip2, trip3, trip4])

#     db.session.commit()

def seed_test_data():
    "Seed the tests."
    f = "%Y-%m-%d %H:%M:%S"
    place1 = Place(yelp_id="Z0r83lDOA1mI8RpNccXtHw", name="The Fat Bear", place_url="https://www.yelp.com/biz/the-fat-bear-london?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ")
    place2 = Place(yelp_id="7Pc6VXiWEqc4JbgrH4U3tA", name="Rocca", place_url="https://www.yelp.com/biz/rocca-london?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ")
    place3 = Place(yelp_id="K_dDxWgagylIvuB2oQy1KQ", name="The Black Penny", place_url="https://www.yelp.com/biz/the-black-penny-london?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ")
    place4 = Place(yelp_id="0B-ag3J18TatG9H9EQohGg", name="Hawksmoor Seven Dials", place_url="https://www.yelp.com/biz/hawksmoor-seven-dials-london-4?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ")
    place5 = Place(yelp_id="BjPq77aiaKZAVUHIu2S3gA", name="The English Rose Cafe and Tea Shop", place_url="https://www.yelp.com/biz/the-english-rose-cafe-and-tea-shop-london?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ")
    place6 = Place(yelp_id="5sEiM_Xw5jXbMhloNqSgYQ", name="Grumbles", place_url="https://www.yelp.com/biz/grumbles-london?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ")
    place7 = Place(yelp_id="cgkDnzaQvP9q-JHXd-ECcA", name="Cambridge Street Kitchen", place_url="https://www.yelp.com/biz/cambridge-street-kitchen-london?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ")
    place8 = Place(yelp_id="-ylzTrYtRJUJa2BuAInoyQ", name="Friends of Ours", place_url="https://www.yelp.com/biz/friends-of-ours-london?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ")
    trip1= Trip(user_id=1, city_id=2, arrival_date=datetime.strptime('2018-03-07 12:00:00', f), departure_date=datetime.strptime('2018-03-13 23:00:00', f))
    trip2= Trip(user_id=2, city_id=1, arrival_date=datetime.strptime('2018-04-10 10:00:00', f), departure_date=datetime.strptime('2018-04-15 15:00:00', f))
    trip3= Trip(user_id=1, city_id=3, arrival_date=datetime.strptime('2018-04-19 14:00:00', f), departure_date=datetime.strptime('2018-04-22 12:00:00', f))
    saved_place1 = SavedPlace(place=place1, trip=trip1, meal_datetime=datetime.strptime('2018-03-07 00:00:00', f), meal_label="lunch")
    saved_place2 = SavedPlace(place=place2, trip=trip1, meal_datetime=datetime.strptime('2018-03-07 00:00:00', f), meal_label="dinner")
    saved_place3 = SavedPlace(place=place3, trip=trip1, meal_datetime=datetime.strptime('2018-03-08 00:00:00', f), meal_label="lunch")
    saved_place4 = SavedPlace(place=place4, trip=trip1, meal_datetime=datetime.strptime('2018-03-09 00:00:00', f), meal_label="breakfast")
    saved_place5 = SavedPlace(place=place5, trip=trip2, meal_datetime=datetime.strptime('2018-04-12 00:00:00', f), meal_label="breakfast")
    saved_place6 = SavedPlace(place=place6, trip=trip2, meal_datetime=datetime.strptime('2018-04-13 00:00:00', f), meal_label="lunch")
    saved_place7 = SavedPlace(place=place7, trip=trip3, meal_datetime=datetime.strptime('2018-04-20 00:00:00', f), meal_label="dinner")
    saved_place8 = SavedPlace(place=place8, trip=trip3, meal_datetime=datetime.strptime('2018-04-21 00:00:00', f), meal_label="lunch")


    db.session.add_all([place1, place2, place3, place4, place5, place6, place7,
        place8, trip1, trip2, trip3, saved_place1, saved_place2, saved_place3, saved_place4,
        saved_place5, saved_place6, saved_place7, saved_place8])
    db.session.commit()


if __name__ =='__main__':
    from flask import Flask  # make flask app
    app = Flask(__name__)
    connect_to_db(app)

    db.create_all()  # make the tables
    seed_user()  # seed starter data
    seed_city()
    # seed_trip()
