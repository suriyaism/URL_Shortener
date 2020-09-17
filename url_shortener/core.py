from flask import Flask
from flask_sqlalchemy import SQLAlchemy


application = Flask(__name__, instance_relative_config=True)

# Load the development configuration as a default
application.config.from_object('config.development')

# Load the file specified by the APP_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
application.config.from_envvar('APP_CONFIG_FILE')

db = SQLAlchemy(application)