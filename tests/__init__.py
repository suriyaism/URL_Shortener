import json
from url_shortener.core import application


def add_long_url(payload):
    """Helper function to post a new url shortener and return the response."""

    with application.test_client() as c:
        return c.post('/shortener/',
                      data=json.dumps(payload),
                      content_type='application/json'
                      )