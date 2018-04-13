"""Server file for Viseat project."""
from jinja2 import StrictUndefined
from pprint import pformat
import os
import requests
from flask import Flask, render_template, redirect, flash, session, request
# from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, City, Trip, Place, SavedPlace

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



@app.route("/login", methods=["POST"])
def login_process():
    """Process Login."""
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Your are not registered.")
        return redirect("/")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/")

    session["user_id"] = user.user_id

    return redirect("/users/{}".format(user.user_id))

@app.route('/users/<int:user_id>')

def show_personal_page(user_id):
    """Show User's personal page."""

    user = User.query.get(user_id)
    if "user_id" in session and session["user_id"] == user.user_id:
        return render_template("user_page.html", user=user)
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
        flash("oops! username doesn't exists.")
        return redirect("/")
    else:
        return redirect("/users/{}".format(user.username))

@app.route('/users/<username>')
def show_user(username):
    """Show user info page."""

    user = User.query.filter_by(username=username).first()

    return render_template("user_info.html", user=user)


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

    elif existing_user_with_given_username:
        # if the entered email is not in the system but the username is in the system
        flash("Please pick a different user name.")
        return redirect("/register")

    else:
        flash("email and username already existing, login.")
        return redirect("/")


@app.route("/places")
def query_api():
    """Queries the YELP API by the input values from the user."""

    # We are getting the name of the City from user.
    name = request.args["name"]
    # name = "Paris,75000,France"

    # If the required information is in the request, look for afterparties
    if name:

        payload = {"location": name}

        headers = {"Authorization": "Bearer %s" % API_KEY}

        response = requests.get(yelp_search_path,
            params=payload, headers=headers)
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
            flash(":( No parties: " + data['error_description'])
            businesses = []

    return render_template("places.html", data=pformat(data),
        results=businesses)



















if __name__ == '__main__':
    # Setting debug=True gives us error messages in the browser and also
    # "reloads" our web app if we change the code.
    connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
