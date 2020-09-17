import unittest
import json
import os
from url_shortener.core import application, db
from tests import add_long_url


class TestShortener(unittest.TestCase):

    def setUp(self):
        # Use a test config as the database file
        self.app = application.test_client()
        application.config.from_object('config.test')
        db.create_all()

    def tearDown(self):
        os.unlink(os.path.join(application.config['BASE_DIR'] + '/' + application.config['DATABASE'] + '.db'))

    def test_invalid_key_url_shortener(self):
        """Test that adding invalid key and then getting an error."""
        payload = {
            'long_url1': 'http://www.google.com'
        }
        response = add_long_url(payload)
        self.assertEqual(500, response.status_code)

    def test_invalid_data_url_shortener(self):
        """Test that adding an invalid url data and then getting an error."""
        payload = {
            'long_url': 'httppp://www.google.com'
        }
        response = add_long_url(payload)
        self.assertEqual(400, response.status_code)

    def test_url_shortener(self):
        """Test that adding an input long url and then getting a short url."""
        payload = {
            'long_url': 'http://google.com'
            }
        response = add_long_url(payload)
        self.assertEqual(200, response.status_code)
