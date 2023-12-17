from datetime import datetime
import re

phone_pattern = re.compile(r'\d{10}')
# date_pattern = re.compile(r'^(?:0[1-9]|[12][0-9]|3[01]).(?:0[1-9]|1[0-2]).(?:(?:19|20)\d\d)$')
date_format_default = '%d.%m.%Y'

def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, date_format_default)
        return True
    except ValueError:
        return False

def is_valid_phone(phone):
	return bool(phone_pattern.match(phone))
