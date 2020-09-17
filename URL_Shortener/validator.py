import re
from collections import defaultdict
from URL_Shortener.models import Shortener

# Using re.compile() is more efficient when the expression will be used several times
URL_REGEX_PATTERN = re.compile(r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)


# Validate URL
def validate_url(data):
    if not URL_REGEX_PATTERN.match(data):
        return False, 'Invalid Input Data of URL'
    return True, ''


# Validate the mandatory fields
def validate_mandatory_fields(data):
    if data in [None, '']:
        return False, 'This field is required'
    return True, ''


def url_existence(data):
    if Shortener.query.filter_by(long_url=data).first() is not None:
        return False, 'The URL is already shortened'
    return True, ''


# Generic Error Validations for the set of input
def error_calculator(validate):
    errors = defaultdict(lambda: [])
    for obj in validate:
        is_valid, error_message = obj['func'](obj['field_val'])
        if not is_valid:
            errors[obj['field_name']].append(error_message)
    return errors

