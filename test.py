from unittest import TestCase
from model import connect_to_db, db
from seed import seed_user, seed_city, seed_test_data
from server import app, query_api
from flask import session

class LoggedOutUserTest(TestCase):
    """Flask tests html & routes, uses db."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True
        # Connect to test database
        connect_to_db(app, "postgresql:///testdb" )
        # Create tables and add sample data
        db.create_all()
        seed_user()
        seed_city()
        seed_test_data()

    def test_show_homepage_route(self):
        """ Homepage html test."""
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn('It is easy to search and save places', result.data)

    def test_login_user(self):
        """Test login of the user."""
        result = self.client.post("/login",
                                  data={"email": "duygu@gmail.com",
                                        "password": "duckface"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        with self.client as c:
            with c.session_transaction() as sess:
                assert sess['user_id'] == 1
                # import pdb; pdb.set_trace()


    def test_login_wrong_email(self):
        """Test login for wrong email entry."""
        result = self.client.post("/login",
                                  data={"email": "blabla@gmail.com",
                                        "password": "duckface"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Your are not registered.", result.data)

    def test_login_wrong_password(self):
        """Test login for wrong password entry."""
        result = self.client.post("/login",
                                  data={"email": "duygu@gmail.com",
                                        "password": "blablabla"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Check your login entries.", result.data)

    def test_search_user(self):
        """Test searching for an existing user."""
        result = self.client.get("/search_user?username=dygduck",
                                 # data={"username": "dygduck"},
                                 follow_redirects=True)
        self.assertEqual(result.status_code, 200)

        # self.assertIn("s page.", result.data)
        # self.assertNotIn("make some trips?", result.data)

    def test_search_non_user(self):
        """Test searching for a non-existing user."""
        result = self.client.get("/search_user?username=dumbo")
                                 # data={"username": "dumbo"},
                                 #follow_redirects=True)
        #import pdb; pdb.set_trace()
        self.assertEqual(result.status_code, 302)
        self.assertIn('target URL: <a href="/">', result.data)

    def test_show_user_page(self):
        """Test showing the page of an existing user."""
        result = self.client.get("/users/dygduck",
                                 follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Duygu's page.", result.data)
        self.assertNotIn("make some trips?", result.data)


    def test_register_form(self):
        """ Test if register form shows up."""
        result = self.client.get("/register")
        self.assertEqual(result.status_code, 200)
        self.assertIn("It is easy to Viseat! It is easy to register!", result.data)

    def test_register_user(self):
        """Test register of a non existing user."""
        result = self.client.post("/register",
                                  data={"username": "magic",
                                        "fname": "harry",
                                        "lname": "potter",
                                        "email": "harry@gmail.com",
                                        "password": "harryp"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        with self.client as c:
            with c.session_transaction() as sess:
                assert sess['user_id'] == 5
        self.assertIn("User harry@gmail.com added", result.data)

    def test_register_existing_username(self):
        """Test register of a non existing user trying an existing username."""
        result = self.client.post("/register",
                                  data={"username": "dygduck",
                                        "fname": "harry",
                                        "lname": "potter",
                                        "email": "harry@gmail.com",
                                        "password": "harryp"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Username or email already existing, please try another one, or login.", result.data)

    def test_register_existing_email(self):
        """Test register of an exting user trying an existing username and email."""
        result = self.client.post("/register",
                                  data={"username": "kedi",
                                        "fname": "harry",
                                        "lname": "potter",
                                        "email": "duygu@gmail.com",
                                        "password": "harryp"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Username or email already existing, please try another one, or login.", result.data)



    def tearDown(self):
        """Do at the end of every test."""

        db.session.close()
        db.drop_all()

class LoggedInUser(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True
        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")
        # Create tables and add sample data
        db.create_all()
        seed_user()
        seed_city()
        seed_test_data()

        with self.client as c:
                with c.session_transaction() as sess:
                    sess["user_id"] = 1

        def mock_query_api(city_name, meal, num_of_meals, num_of_offsets):
            return [{u'rating': 4.0, u'review_count': 288, u'name': u'Eggs & Co', u'transactions': [], u'url': u'https://www.yelp.com/biz/eggs-et-co-paris?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ', u'price': u'\u20ac\u20ac', u'distance': 1265.5420697108445, u'coordinates': {u'latitude': 48.853123, u'longitude': 2.331244}, u'alias': u'eggs-et-co-paris', u'image_url': u'https://s3-media1.fl.yelpcdn.com/bphoto/cqqRDT553EUVCFuOx0aoug/o.jpg', u'categories': [{u'alias': u'breakfast_brunch', u'title': u'Breakfast & Brunch'}], u'display_phone': u'+33 1 45 44 02 52', u'phone': u'+33145440252', u'id': u'arT8b1fhGKwMzZ4WsaXUww', u'is_closed': False, u'location': {u'city': u'Paris', u'display_address': [u'11 rue Bernard Palissy', u'75006 Paris', u'France'], u'country': u'FR', u'address2': u'', u'address3': u'', u'state': u'75', u'address1': u'11 rue Bernard Palissy', u'zip_code': u'75006'}}, {u'rating': 4.5, u'review_count': 105, u'name': u"Baguett's Caf\xe9", u'transactions': [], u'url': u'https://www.yelp.com/biz/baguetts-caf%C3%A9-paris?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ', u'price': u'\u20ac\u20ac', u'distance': 556.2220788075778, u'coordinates': {u'latitude': 48.86528, u'longitude': 2.33657}, u'alias': u'baguetts-caf\xe9-paris', u'image_url': u'https://s3-media1.fl.yelpcdn.com/bphoto/iRC0dLJ07IdhiT1AbfbvAw/o.jpg', u'categories': [{u'alias': u'coffee', u'title': u'Coffee & Tea'}, {u'alias': u'breakfast_brunch', u'title': u'Breakfast & Brunch'}, {u'alias': u'sandwiches', u'title': u'Sandwiches'}], u'display_phone': u'+33 9 54 83 04 86', u'phone': u'+33954830486', u'id': u'70xArgLO0k56YAytyBIHyg', u'is_closed': False, u'location': {u'city': u'Paris', u'display_address': [u'33 rue de Richelieu', u'75001 Paris', u'France'], u'country': u'FR', u'address2': u'', u'address3': u'', u'state': u'75', u'address1': u'33 rue de Richelieu', u'zip_code': u'75001'}}, {u'rating': 4.5, u'review_count': 210, u'name': u'Kozy', u'transactions': [], u'url': u'https://www.yelp.com/biz/kozy-paris-6?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ', u'price': u'\u20ac', u'distance': 2791.074381151342, u'coordinates': {u'latitude': 48.85521, u'longitude': 2.3054009}, u'alias': u'kozy-paris-6', u'image_url': u'https://s3-media4.fl.yelpcdn.com/bphoto/L-klegsu2Sr7WzeZlq6okw/o.jpg', u'categories': [{u'alias': u'coffee', u'title': u'Coffee & Tea'}, {u'alias': u'breakfast_brunch', u'title': u'Breakfast & Brunch'}, {u'alias': u'sandwiches', u'title': u'Sandwiches'}], u'display_phone': u'+33 9 83 89 12 64', u'phone': u'+33983891264', u'id': u'rukLJuVj9wTF8diraA1BCQ', u'is_closed': False, u'location': {u'city': u'Paris', u'display_address': [u'79 avenue Bosquet', u'75007 Paris', u'France'], u'country': u'FR', u'address2': u'', u'address3': u'', u'state': u'75', u'address1': u'79 avenue Bosquet', u'zip_code': u'75007'}}, {u'rating': 4.5, u'review_count': 77, u'name': u'Holybelly', u'transactions': [], u'url': u'https://www.yelp.com/biz/holybelly-paris-2?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ', u'price': u'\u20ac\u20ac', u'distance': 1628.3994825940053, u'coordinates': {u'latitude': 48.87099, u'longitude': 2.3598}, u'alias': u'holybelly-paris-2', u'image_url': u'https://s3-media2.fl.yelpcdn.com/bphoto/4EvXgjj0spXR_F-Uej9Csw/o.jpg', u'categories': [{u'alias': u'breakfast_brunch', u'title': u'Breakfast & Brunch'}, {u'alias': u'coffee', u'title': u'Coffee & Tea'}], u'display_phone': u'+33 1 82 28 00 80', u'phone': u'+33182280080', u'id': u'rbBs01WKKsVZG61q5IwJ_w', u'is_closed': False, u'location': {u'city': u'Paris', u'display_address': [u'5 rue Lucien Sampaix', u'75010 Paris', u'France'], u'country': u'FR', u'address2': u'', u'address3': None, u'state': u'75', u'address1': u'5 rue Lucien Sampaix', u'zip_code': u'75010'}}, {u'rating': 4.5, u'review_count': 226, u'name': u'Claus - La Table du Petit-D\xe9jeuner', u'transactions': [], u'url': u'https://www.yelp.com/biz/claus-la-table-du-petit-d%C3%A9jeuner-paris?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ', u'price': u'\u20ac\u20ac\u20ac', u'distance': 128.77578245280193, u'coordinates': {u'latitude': 48.86246, u'longitude': 2.34053}, u'alias': u'claus-la-table-du-petit-d\xe9jeuner-paris', u'image_url': u'https://s3-media1.fl.yelpcdn.com/bphoto/wQBjJo4bGwQYYIXB2nGhBw/o.jpg', u'categories': [{u'alias': u'breakfast_brunch', u'title': u'Breakfast & Brunch'}, {u'alias': u'cafes', u'title': u'Cafes'}], u'display_phone': u'+33 1 42 33 55 10', u'phone': u'+33142335510', u'id': u'N3zQ7Y52QXRnfQy_Gri3yw', u'is_closed': False, u'location': {u'city': u'Paris', u'display_address': [u'14 rue Jean-Jacques Rousseau', u'75001 Paris', u'France'], u'country': u'FR', u'address2': u'', u'address3': u'', u'state': u'75', u'address1': u'14 rue Jean-Jacques Rousseau', u'zip_code': u'75001'}}, {u'rating': 4.5, u'review_count': 104, u'name': u'The Hardware Soci\xe9t\xe9', u'transactions': [], u'url': u'https://www.yelp.com/biz/the-hardware-soci%C3%A9t%C3%A9-paris-2?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ', u'price': u'\u20ac\u20ac', u'distance': 2776.4178507056945, u'coordinates': {u'latitude': 48.88688, u'longitude': 2.3445299}, u'alias': u'the-hardware-soci\xe9t\xe9-paris-2', u'image_url': u'https://s3-media4.fl.yelpcdn.com/bphoto/b6F2YclPIxW3rz0OsC3E8Q/o.jpg', u'categories': [{u'alias': u'coffee', u'title': u'Coffee & Tea'}, {u'alias': u'breakfast_brunch', u'title': u'Breakfast & Brunch'}, {u'alias': u'australian', u'title': u'Australian'}], u'display_phone': u'+33 1 42 51 69 03', u'phone': u'+33142516903', u'id': u'GhuBVzRYZ2nWSKgXdEmBpw', u'is_closed': False, u'location': {u'city': u'Paris', u'display_address': [u'10 rue Lamarck', u'75018 Paris', u'France'], u'country': u'FR', u'address2': u'', u'address3': u'', u'state': u'75', u'address1': u'10 rue Lamarck', u'zip_code': u'75018'}}, {u'rating': 4.5, u'review_count': 49, u'name': u'La Petite Marquise', u'transactions': [], u'url': u'https://www.yelp.com/biz/la-petite-marquise-paris?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ', u'price': u'\u20ac\u20ac', u'distance': 4224.362890370749, u'coordinates': {u'latitude': 48.86958, u'longitude': 2.28557}, u'alias': u'la-petite-marquise-paris', u'image_url': u'https://s3-media1.fl.yelpcdn.com/bphoto/iVjo_UGXUhNdt9_KdkCw2Q/o.jpg', u'categories': [{u'alias': u'bakeries', u'title': u'Bakeries'}], u'display_phone': u'+33 1 45 00 77 36', u'phone': u'+33145007736', u'id': u'wCfRv8PEb1cNjy02y3NoFQ', u'is_closed': False, u'location': {u'city': u'Paris', u'display_address': [u'3 place Victor Hugo', u'75116 Paris', u'France'], u'country': u'FR', u'address2': None, u'address3': None, u'state': u'75', u'address1': u'3 place Victor Hugo', u'zip_code': u'75116'}}, {u'rating': 4.5, u'review_count': 110, u'name': u'Soul Kitchen', u'transactions': [], u'url': u'https://www.yelp.com/biz/soul-kitchen-paris?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ', u'price': u'\u20ac\u20ac', u'distance': 3024.77602937331, u'coordinates': {u'latitude': 48.88916, u'longitude': 2.34252}, u'alias': u'soul-kitchen-paris', u'image_url': u'https://s3-media1.fl.yelpcdn.com/bphoto/Yn6QqX4UQMhYeUYeKO8EXQ/o.jpg', u'categories': [{u'alias': u'coffee', u'title': u'Coffee & Tea'}, {u'alias': u'desserts', u'title': u'Desserts'}, {u'alias': u'breakfast_brunch', u'title': u'Breakfast & Brunch'}], u'display_phone': u'+33 1 71 37 99 95', u'phone': u'+33171379995', u'id': u'gIBclMWGw2eAh1c5cYyo7A', u'is_closed': False, u'location': {u'city': u'Paris', u'display_address': [u'33 rue Lamarck', u'75018 Paris', u'France'], u'country': u'FR', u'address2': u'', u'address3': u'', u'state': u'75', u'address1': u'33 rue Lamarck', u'zip_code': u'75018'}}, {u'rating': 4.0, u'review_count': 1013, u'name': u'Angelina', u'transactions': [], u'url': u'https://www.yelp.com/biz/angelina-paris?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ', u'price': u'\u20ac\u20ac\u20ac', u'distance': 1059.8775176567408, u'coordinates': {u'latitude': 48.865092, u'longitude': 2.328464}, u'alias': u'angelina-paris', u'image_url': u'https://s3-media3.fl.yelpcdn.com/bphoto/xD21zTjpa71Ipf9tGQA_fA/o.jpg', u'categories': [{u'alias': u'tea', u'title': u'Tea Rooms'}, {u'alias': u'bakeries', u'title': u'Bakeries'}], u'display_phone': u'+33 1 42 60 82 00', u'phone': u'+33142608200', u'id': u'ijqSzadlZ9SCXvUEpMimcA', u'is_closed': False, u'location': {u'city': u'Paris', u'display_address': [u'226 rue de Rivoli', u'75001 Paris', u'France'], u'country': u'FR', u'address2': None, u'address3': None, u'state': u'75', u'address1': u'226 rue de Rivoli', u'zip_code': u'75001'}}, {u'rating': 4.5, u'review_count': 83, u'name': u'Ob-la-Di', u'transactions': [], u'url': u'https://www.yelp.com/biz/ob-la-di-paris?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ', u'price': u'\u20ac\u20ac', u'distance': 1607.881671102616, u'coordinates': {u'latitude': 48.86301, u'longitude': 2.36403}, u'alias': u'ob-la-di-paris', u'image_url': u'https://s3-media3.fl.yelpcdn.com/bphoto/RNUo2SsWBDnAp2z7o9Dq7g/o.jpg', u'categories': [{u'alias': u'breakfast_brunch', u'title': u'Breakfast & Brunch'}, {u'alias': u'coffee', u'title': u'Coffee & Tea'}], u'display_phone': u'', u'phone': u'', u'id': u'qLD442-5_Xe5wRELOAm03A', u'is_closed': False, u'location': {u'city': u'Paris', u'display_address': [u'54 rue de Saintonge', u'75003 Paris', u'France'], u'country': u'FR', u'address2': u'', u'address3': u'', u'state': u'75', u'address1': u'54 rue de Saintonge', u'zip_code': u'75003'}}, {u'rating': 4.5, u'review_count': 111, u'name': u'Boulangerie Julien', u'transactions': [], u'url': u'https://www.yelp.com/biz/boulangerie-julien-paris-3?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ', u'price': u'\u20ac', u'distance': 172.94784579730944, u'coordinates': {u'latitude': 48.86109, u'longitude': 2.344109}, u'alias': u'boulangerie-julien-paris-3', u'image_url': u'https://s3-media2.fl.yelpcdn.com/bphoto/5sWjJ5u8FPb83Vbkw-tzng/o.jpg', u'categories': [{u'alias': u'bakeries', u'title': u'Bakeries'}], u'display_phone': u'+33 1 42 36 24 83', u'phone': u'+33142362483', u'id': u'fqubHKy6fX5PdyuM_nodng', u'is_closed': False, u'location': {u'city': u'Paris', u'display_address': [u'75 rue Saint-Honor\xe9', u'75001 Paris', u'France'], u'country': u'FR', u'address2': u'', u'address3': u'', u'state': u'75', u'address1': u'75 rue Saint-Honor\xe9', u'zip_code': u'75001'}}, {u'rating': 4.5, u'review_count': 200, u'name': u'Bl\xe9 Sucr\xe9', u'transactions': [], u'url': u'https://www.yelp.com/biz/bl%C3%A9-sucr%C3%A9-paris-2?adjust_creative=xRkF2ozLJzv0Tl0J-wOpZQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xRkF2ozLJzv0Tl0J-wOpZQ', u'price': u'\u20ac', u'distance': 2831.426504410104, u'coordinates': {u'latitude': 48.850565, u'longitude': 2.376759}, u'alias': u'bl\xe9-sucr\xe9-paris-2', u'image_url': u'https://s3-media4.fl.yelpcdn.com/bphoto/CxJXhbTkoYAxWumxH1zViw/o.jpg', u'categories': [{u'alias': u'bakeries', u'title': u'Bakeries'}, {u'alias': u'cakeshop', u'title': u'Patisserie/Cake Shop'}], u'display_phone': u'+33 1 43 40 77 73', u'phone': u'+33143407773', u'id': u'0ywhA79RdU_uwPsmXJcYKw', u'is_closed': False, u'location': {u'city': u'Paris', u'display_address': [u'7 rue Antoine Vollon', u'75012 Paris', u'France'], u'country': u'FR', u'address2': u'', u'address3': u'', u'state': u'75', u'address1': u'7 rue Antoine Vollon', u'zip_code': u'75012'}}]
        query_api = mock_query_api


    def test_logged_in_user_page(self):
        """Test logged in user's personal page."""
        result = self.client.get("/users/1")
        self.assertEqual(result.status_code, 200)
        self.assertIn("Hi Duygu, would you like to make some trips", result.data)
        self.assertIn("The Fat Bear", result.data)
        self.assertIn("lunch", result.data)
        self.assertIn("Departure Date", result.data)
        self.assertIn("City", result.data)
        self.assertIn("Search", result.data)
        self.assertIn("Logout", result.data)
        self.assertNotIn("The English Rose Cafe and Tea Shop", result.data)

    def test_search_data_shows_up(self):
        result = self.client.get("/places?city_id=1&arrival_date=2018-04-27T12:00&departure_date=2018-04-28T20:00")
        self.assertEqual(result.status_code, 200)
        self.assertIn("2018-04-27", result.data)
        self.assertIn("2018-04-28", result.data)
        self.assertIn("breakfast:", result.data)

    def test_user_loggout(self):
        """Test logout process."""
        result = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn("Logged Out.", result.data)
        self.assertIn("If you are not a user, please register.", result.data)
        self.assertIn("Hello!", result.data)
        self.assertNotIn("Hi Duygu, would you like to make some trips", result.data)
        self.assertNotIn("The Fat Bear", result.data)
        with self.client as c:
            with c.session_transaction() as sess:
                assert "user_id" not in sess
    

    def tearDown(self):
        """Do at the end of every test."""

        db.session.close()
        db.drop_all()









if __name__ == '__main__':
    import unittest

    unittest.main()
