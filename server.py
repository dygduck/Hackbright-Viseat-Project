"""Server file for Viseat project."""
from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, flash, session, request
# from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, City, Trip, Place, SavedPlace

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "SecretD"

yelp_serch_path = "https://api.yelp.com/v3/businesses/search"


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

    flash("Logged in")
    return redirect("/users/{}".format(user.user_id))

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """Show User's personal page."""

    user = User.query.get(user_id)
    return render_template("user_page.html", user=user)













if __name__ == '__main__':
    # Setting debug=True gives us error messages in the browser and also
    # "reloads" our web app if we change the code.
    connect_to_db(app)
    app.run(debug=True)
