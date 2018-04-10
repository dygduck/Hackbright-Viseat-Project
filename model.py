
"""Models and database functions for Viseat Project."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.secret_key = "SecretD"

def connect_to_db(app):
    """Connect to database."""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///testdb'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True, primary_key=True)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User fname={} lname={} email={}>".format(self.fname,
                                               self.lname, self.email)



class City(db.Model):
    """City to visit in website."""

    __tablename__ = "cities"

    city_id = db.Column(db.Integer,
                        autoincrement=True, primary_key=True)
    name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<City name={}>".format(self.name)

    # Define relationship to the trips table.
    trips = db.relationship("Trip", backref=db.backref("city"))


class Trip(db.Model):
    """Specific trip of the user in website."""

    __tablename__ = "trips"

    trip_id = db.Column(db.Integer,
                        autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'))
    arrival_date = db.Column(db.DateTime, nullable=False)
    departure_date = db.Column(db.DateTime, nullable=False)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Trip trip_id={} user_id={} city_id={}>".format(self.trip_id,
                                               self.user_id, self.city_id)
    # Define relationship to user
    user = db.relationship("User", backref=db.backref("trips"))


class Place(db.Model):
    """Places to show to the user in website."""

    __tablename__ = "places"

    yelp_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Place name={}>".format(self.name)


class SavedPlace(db.Model):
    """Place recommended to the user."""

    __tablename__ = "saved_places"

    saved_place_id = db.Column(db.Integer,
                        autoincrement=True, primary_key=True)
    yelp_id = db.Column(db.String, db.ForeignKey('places.yelp_id'))
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id'))
    meal_datetime = db.Column(db.DateTime, nullable=False)
    meal_label = db.Column(db.String(40), nullable=False)

    # Define relationship to trip
    trip = db.relationship("Trip",
        backref=db.backref("saved_places"))

    # Define relationship to place
    place = db.relationship("Place",
        backref=db.backref("saved_places"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Recommended_Place trip_id={} name={} meal_label={}>".format(self.trip_id, self.name, self.meal_label)



if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.
    from server import app
    connect_to_db(app)
    print "Connected to DB."
    db.create_all()
