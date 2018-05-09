"""Server file for Viseat project."""
from jinja2 import StrictUndefined
from pprint import pformat
import os
import requests
from collections import OrderedDict
from flask import Flask, render_template, redirect, flash, session, request
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, City, Trip, Place, SavedPlace
from datetime import datetime, timedelta

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SecretD"

API_KEY = os.environ.get("YELP_API_KEY")

yelp_search_path = "https://api.yelp.com/v3/businesses/search"


# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def show_homepage():
    """Homepage. Show Login Form and Register button."""

    return render_template("homepage.html")

@app.route('/about')
def show_about():
    """Show about page."""

    return render_template("about.html")


@app.route("/login", methods=["POST"])
def login_process():
    """Process Login."""
    email = request.form["email"].lower()
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Your are not registered.")
        return redirect("/")

    if user.password != password:
        flash("Check your login entries.")
        return redirect("/")

    session["user_id"] = user.user_id

    return redirect("/users/{}".format(user.user_id))

@app.route('/users/<int:user_id>')
def show_personal_page(user_id):
    """Show User's personal page."""

    user = User.query.get(user_id)
    cities = City.query.all()

    if "user_id" in session and session["user_id"] == user.user_id:

        trips = Trip.query.filter(Trip.user_id == session["user_id"]).all()

        trips_dict = {}
        for trip in trips:
            trip_info = {
                "trip_id":trip.trip_id,
                "city_name": trip.city.city_name,
                "departure_date": trip.departure_date.date(),
                "dates": {}
            }
            for place in trip.saved_places:
                date = place.meal_datetime.date()
                meals = trip_info["dates"].get(date, {})
                meals[place.meal_label] = {"name": place.place.name, "url": place.place.place_url, "saved_place_id":place.saved_place_id}
                trip_info["dates"][date] = meals
            trips_dict[trip.arrival_date.date()] = trip_info

        # import pprint
        # pprint.pprint(trips_dict)


        return render_template("user_page.html", user=user, cities=cities,
            trips_dict=trips_dict)

    return redirect("/")

@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


@app.route("/search_user", methods=["GET"])
def search_user():
    """Search for a user page."""
    username = request.args["username"]

    user = User.query.filter_by(username=username).first()
    print user
    if not user:
        flash("oops! username doesn't exist.")
        # return render_template("/")
        return redirect(request.referrer)
    else:
        return redirect("/users/{}".format(user.username))

@app.route('/users/<username>')
def show_user(username):
    """Show a user info page."""

    user = User.query.filter_by(username=username).first()
    trips = Trip.query.filter(Trip.user == user).all()

    trips_dict = {}
    for trip in trips:
        trip_info = {
            "city_name": trip.city.city_name,
            "departure_date": trip.departure_date.date(),
            "dates": {}
        }
        for place in trip.saved_places:
            date = place.meal_datetime.date()
            meals = trip_info["dates"].get(date, {})
            meals[place.meal_label] = {"name": place.place.name, "url": place.place.place_url}
            trip_info["dates"][date] = meals
        trips_dict[trip.arrival_date.date()] = trip_info

    return render_template("user_info.html", user=user, trips_dict=trips_dict)


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register.html")

@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    username = request.form["username"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    password = request.form["password"]

    existing_user_with_given_email = User.query.filter(User.email == email).first()
    existing_user_with_given_username = User.query.filter(User.username == username).first()


    if not existing_user_with_given_email and not existing_user_with_given_username:
        # if the entered email and username is not in the system.

        user = User(username=username, fname=fname, lname=lname,
        email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.user_id

        flash("User {} added.".format(email))
        return redirect("/users/{}".format(user.user_id))

    elif existing_user_with_given_username or existing_user_with_given_email:
        # if the entered email is not in the system but the username is in the system
        flash("Username or email already existing, please try another one, or login.")
        return redirect("/register")



@app.route("/places")
def handle_entry():
    """Queries the YELP API by the input values from the user."""

    if "user_id" not in session:
        flash("You must be logged in to search.")
        return redirect("/")
    user_id = session["user_id"]


    city_id = request.args["city_id"]
    city_name = City.query.get(city_id).city_name



    # Change the input times into datetime format:
    f = '%Y-%m-%dT%H:%M'
    # arrival_date_processing = arrival_date.replace("T", " ")
    arrival_date = datetime.strptime(request.args["arrival_date"], f)
    # departure_date_processing = departure_date.replace("T", " ")
    departure_date = datetime.strptime(request.args["departure_date"], f)
    delta = departure_date - arrival_date


    days_to_eat = {}

    user = User.query.get(user_id)

    if arrival_date > departure_date:
        flash("Please be sure your that your arrival date is before than your departure date.")
        return redirect("/users/{}".format(user.user_id))
    elif departure_date == arrival_date:
        flash("Sorry, you don't have enough time to eat this time.")
        return redirect("/users/{}".format(user.user_id))


    # find the num of days between these two dates
    full_day_start = arrival_date.date() + timedelta(days=1)
    full_day_end = departure_date.date()
    num_of_full_days = full_day_end - full_day_start

    # num_of_meals = num_of_full_days.days + 2
    num_of_meals = (num_of_full_days.days +2) + 10
    places = {}

    # querying Yelp API for breakfasts
    breakfasts = query_api(city_name, "breakfast", num_of_meals, 0)
    breakfast_recommendations = []
    for business in breakfasts:
        business_name = business["name"]
        # print "breakfast business names"
        # print business_name
        # print "breakfast number of recs"
        # print len(breakfast_recommendations)
        # print breakfast_recommendations
        # print "breakfast num of meals"
        # print num_of_meals
        # print "breakfast places"
        # print places

        if business_name not in places and len(breakfast_recommendations) <= num_of_meals:
            places[business_name] = True
            business["meal"] = "breakfast"
            breakfast_recommendations.append(business)
    # print "length of breakfast recomm"
    # print len(breakfast_recommendations)
    # print "list of places"
    # print places

    # querying Yelp API for lunches
    lunches = query_api(city_name, "lunch", num_of_meals, num_of_meals)
    lunch_recommendations = []
    for business in lunches:
        business_name = business["name"]
        # print "lunch business names"
        # print business_name
        # print "lunch number of recs"
        # print len(lunch_recommendations)
        # print lunch_recommendations
        # print "lunch num of meals"
        # print num_of_meals
        # print "lunch places"
        # print places

        if business_name not in places and len(lunch_recommendations) <= num_of_meals:
            places[business_name] = True
            business["meal"] = "lunch"
            lunch_recommendations.append(business)
    # print "length of lunch recomm"
    # print len(lunch_recommendations)
    # print "list of places"
    # print places


    # querying Yelp API for dinners
    dinners = query_api(city_name, "dinner", num_of_meals, num_of_meals*2)
    dinner_recommendations = []
    for business in dinners:
        business_name = business["name"]
        # print "dinner business names"
        # print business_name
        # print "dinner number of recs"
        # print len(dinner_recommendations)
        # print dinner_recommendations
        # print "dinner num of meals"
        # print num_of_meals
        # print "dinner places"
        # print places

        if business_name not in places and len(dinner_recommendations) <= num_of_meals:
            places[business_name] = True
            business["meal"] = "dinner"
            dinner_recommendations.append(business)
    # print "length of dinner recomm"
    # print len(dinner_recommendations)
    # print "list of places"
    # print places
    if len(dinner_recommendations) == 0 and len(lunch_recommendations) == 0 and len(breakfast_recommendations) == 0:
        flash("Soory bla bla")
        return redirect("/users/{}".format(user.user_id))

    arrival_day = arrival_date.date()
    departure_day = departure_date.date()

    if num_of_full_days != 0:
        # add our days and meals into our days_to_eat list
        for day in range(1, delta.days + 1):
            key = (arrival_date + timedelta(days=day)).date()
            days_to_eat[key] = []
            days_to_eat[key].append(breakfast_recommendations[day])
            days_to_eat[key].append(lunch_recommendations[day])
            days_to_eat[key].append(dinner_recommendations[day])


    arrival_meals = []
    departure_meals = []
    arrival_time = (arrival_date.hour * 100) + arrival_date.minute
    departure_time = (departure_date.hour * 100) + departure_date.minute

    if arrival_time <= 1100:
        # add 1 breakfast to the days_to_eat lists arrival_date dictionary
        arrival_meals.append(breakfast_recommendations[0])

    if arrival_time <= 1500:
        # add 1 lunch to the days_to_eat lists arrival_date dictionary
        arrival_meals.append(lunch_recommendations[0])

    if arrival_time <= 2200:
        # add 1 dinner to the days_to_eat list arrival_date dictionary
        arrival_meals.append(dinner_recommendations[0])

    if departure_time >= 701:
        # add 1 breakfast to the days_to_eat lists departure_date dictionary
        departure_meals.append(breakfast_recommendations[-1])

    if departure_time >= 1101:
        # add 1 lunch to the days_to_eat lists departure_date dictionary
        departure_meals.append(lunch_recommendations[-1])

    if departure_time >= 1801:
        # add 1 dinner to the days_to_eat lists departure_date dictionary
        departure_meals.append(dinner_recommendations[-1])

    if len(arrival_meals) != 0:
        days_to_eat[arrival_day] = arrival_meals
    if len(departure_meals) != 0:
        days_to_eat[departure_day] = departure_meals

    ordered_days_to_eat = OrderedDict(sorted(days_to_eat.items(), key=lambda t:t[0]))


    return render_template("/places.html", ordered_days_to_eat=ordered_days_to_eat,
        arrival_date=arrival_date, departure_date=departure_date, city_id=city_id)


def query_api(city_name, meal, num_of_meals, num_of_offsets):
    """Queries the YELP API by the input values from the user."""
    # print "num_of_meals"
    # print num_of_meals
    # print "meal categories"
    # print meal
    # print "name"
    # print name

    payload = {"location": city_name, "term": meal, "offset": num_of_offsets, "limit": num_of_meals}

    headers = {"Authorization": "Bearer %s" % API_KEY}

    response = requests.get(yelp_search_path, params=payload, headers=headers)
    # print("Response pprint:\n\n\n")
    # import pprint
    # pprint.pprint(response)
    # print("\n\n\nEnd Response pprint")
    # print("Response: {}".format(response))


    # If the response was successful (with a status code of less than 400),
    # use the list of places from the returned JSON
    if response.ok:
        data = response.json()
        businesses = data['businesses']

# If there was an error (status code between 400 and 600), use an empty list
    else:
        businesses = []

    # print meal
    print businesses
    # print "number of businesses"
    # print len(businesses)
    return businesses


@app.route("/save_places", methods=["POST"])
def save_places():
    """Saves the places checked by the user."""
    user_id = session["user_id"]
    user = User.query.get(user_id)

    saved_businesses = request.form.getlist("saved_businesses")
    city_id = request.form["city_id"]
    arrival_date = request.form["arrival_date"]
    departure_date = request.form["departure_date"]


    trip = Trip(user_id=user_id, city_id=city_id, arrival_date=arrival_date,
                departure_date=departure_date)
    db.session.add(trip)

    for business in saved_businesses:
        # get the name from the form
        business_name = request.form[business+'__name']
        # get the label from the form
        business_label = request.form[business+'__label']
        # get the date from the form
        business_date = request.form[business+'__date']
        # get the url from the form
        business_url = request.form[business+'__url']
        # check this place already exists in db
        place = Place.query.get(business)
        if place is None:
            place = Place(yelp_id=business, name=business_name, place_url=business_url)
        saved_place = SavedPlace(trip=trip, place=place,
                                     meal_datetime=business_date,
                                     meal_label=business_label)

        # save the place to the database
        db.session.add(place)
        db.session.add(saved_place)

    db.session.commit()

    session["user_id"] = user.user_id

    return redirect("/users/{}".format(user.user_id))


@app.route("/delete_places", methods=["POST"])
def delete_places():
    """delete the places checked by the user."""
    user_id = session["user_id"]
    user = User.query.get(user_id)

    # delete places first and then delete trips , so there will be no error
    # possibility.

    saved_places = request.form.getlist("saved_place")
    # print saved_places
    for place_id in saved_places:
        saved_place = SavedPlace.query.get(int(place_id))
        db.session.delete(saved_place)


    dates = request.form.getlist("date")
    for date in dates:
        trip_id, meal_datetime = date.split(":")
        trip_id = int(trip_id)
        saved_places_to_delete = SavedPlace.query.filter(SavedPlace.trip_id == trip_id, SavedPlace.meal_datetime == meal_datetime).all()
        for place in saved_places_to_delete:
            db.session.delete(place)


    trips = request.form.getlist("trip")
    # print "PRINTING TRIPS: {}".format(trips)
    for trip_id in trips:
        trip = Trip.query.get(int(trip_id))
        # print("Deleting trip first loop: {}".format(trip))
        db.session.delete(trip)


    trips = Trip.query.filter(Trip.user == user).all()
    # print trips
    for trip in trips:
        if trip.saved_places == []:
            # print("Deleting trip second loop: {}".format(trip))
            db.session.delete(trip)

    
    db.session.commit()

    return "delete completed"























if __name__ == '__main__':
    # Setting debug=True gives us error messages in the browser and also
    # "reloads" our web app if we change the code.
    # app.debug = True
    # DebugToolbarExtension(app)
    # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
