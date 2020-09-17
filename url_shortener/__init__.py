import os
import markdown
from flask import Flask, Markup, render_template, request, redirect
from url_shortener.validator import validate_url, url_existence, error_calculator, validate_mandatory_fields
from url_shortener.utils import json_response
from url_shortener.models import Shortener
from url_shortener.core import application, db


@application.route("/", methods=["GET"])
def index():
    # Open the README file
    with open(os.path.dirname(application.root_path) + '/README.md', 'r') as markdown_file:
        # Read the markdown contents
        content = markdown_file.read()
        # Convert the markdown to HTML and then treat it as actual HTML so it's not escaped
        html = Markup(markdown.markdown(content, extensions=['markdown.extensions.fenced_code']))
    return render_template('index.html', content=html)


@application.route("/shortener/", methods=["POST"])
def shortener():
    list_key = []
    payload = request.get_json()

    # Storing Key of the payload
    for key, value in payload.items():
        list_key.append(key)

    # Checking key in the payload
    if 'long_url' not in list_key or list_key is None:
        response_output = json_response(message="Error",
                                        data="Check or pass the correct input with a proper key",
                                        status=500)
        return response_output

    # Storing long URL
    long_url = payload.get('long_url')

    # Validate the input
    validate = [
        {'field_name': 'long_url', 'func': validate_mandatory_fields, 'field_val': long_url},
        {'field_name': 'long_url', 'func': validate_url, 'field_val': long_url},
        {'field_name': 'long_url', 'func': url_existence, 'field_val': long_url},
    ]
    result = error_calculator(validate)

    # Shortening the URL based on the validations
    if result:
        response_output = json_response(message="Error",
                                        data=result,
                                        status=400)
    else:
        # Adding the payload into the database
        url_shortener = Shortener.create_short_url(long_url=long_url)
        output_url = "https://tier.app/" + str(url_shortener)
        response_output = json_response(message=long_url,
                                        data=output_url,
                                        status=200)
    return response_output


@application.route("/<short_url>", methods=["GET"])
def redirect_url(short_url):
    # Filter the data with the short url
    short = Shortener.query.filter_by(short_url=short_url).first()
    # 404 found if short url is None
    if short is None:
        response_output = json_response(message="Error",
                                        data="Page Not Found or Invalid URL provided, "
                                             "please enter the valid short url from the list "
                                             "(http://127.0.0.1:" + str(application.config['PORT']) + "/shortener/list) "
                                             "or check the documentation "
                                             "(http://127.0.0.1:" + str(application.config['PORT']) + "/)",
                                        status=404)
        return response_output
    # Incrementing the hits count and updating the database
    short.hits += 1
    db.session.commit()
    # Redirecting the site to the long urls
    return redirect(short.long_url)


@application.route("/shortener/list", methods=["GET"])
def urls_list():
    url_shortener = []
    # Fetching all the data from the database
    for url in Shortener.query.all():
        url_shortener.append(url.to_json())
    response_output = json_response(message="List of URL Shortener",
                                    data=url_shortener,
                                    status=200)
    return response_output

# if __name__ == "__main__":
#    db.create_all()
#    application.run(host=HOST, port=PORT, threaded=True)
