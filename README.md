# GoVisEat

GoVisEat is a web app that helps user to make a customized search to choose where to eat in a specific city for a time period, save these recommended places in advance and even search for other users to see their saved trips. The application uses Yelp API and Google Maps for place search.

![GoVisEat Homepage](https://github.com/dygduck/Hackbright-Viseat-Project/blob/master/static/images/homepage.png)

### Features

Users can register and login.

![GoVisEat Register Page](https://github.com/dygduck/Hackbright-Viseat-Project/blob/master/static/images/register_screen.png)

Once the user logged in, they are directed to their personal page, where they can see their saved places if they have saved any, and a search form.

![GoVisEat Register Page](https://github.com/dygduck/Hackbright-Viseat-Project/blob/master/static/images/userpage_search_screen.png)

User can save these recommendations and search for other users to see their saved places.

![GoVisEat Register Page](https://github.com/dygduck/Hackbright-Viseat-Project/blob/master/static/images/saving_screen.png)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Languages: Python, JS, HTML, CSS, SQL
Frameworks and Templates: Flask, Jinja, Bootstrap
Other Technologies: Ajax, jQuery, SQLAlchemy, PostgreSQL
APIs: YELP, Google Maps



### Installing

GoVisEat requires [Python 2.7](https://www.python.org/downloads/release/python-2714/) and [PostgreSQL](https://www.postgresql.org/) to run.

Clone this repository.

```sh
$ git clone https://github.com/dygduck/Hackbright-Viseat-Project.git
```

Create and activate a virtual environment inside your own GoVisEat directory.

```sh
$ virtualenv env
$ source env/bin/activate
```

Install the requirements.

```sh
$ pip install -r requirements.txt
```

Get keys to the [Yelp](https://www.yelp.com/developers/documentation/v3) and [Google Maps](https://developers.google.com/maps/documentation/javascript/get-api-key) APIs.

Store them in a secrets.sh file:

```sh
export YELP_API_KEY="ABC
```

Create your database.

```sh
$ createdb viseatdb
$ python model.py
```

Run the server.

```sh
$ python server.py
```

## Authors

* **Duygu Ebcim Ozgul** - [dygduck](https://github.com/dygduck)



## Acknowledgments

* [Hackbright Academy](https://hackbrightacademy.com/) - This web app is created as a project by Duygu Ebcim Ozgul while she was a Full-Stack Software Engineering student at Hackbright Academy.
