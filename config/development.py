# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Statement for enabling the development environment
DEBUG = True

PORT = "5000"
DATABASE = "Development_Database"

# Define the database - we are working with SQLite
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, DATABASE + '.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = '6a0a827ee70a4e2396a49237a31d4eae'

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = SECRET_KEY
