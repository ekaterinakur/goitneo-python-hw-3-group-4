from datetime import datetime, timedelta
import calendar
from collections import defaultdict 
from utils.validators import date_format_default

# ANSI escape codes for text color
CYAN = "\033[96m"
RESET = "\033[0m"

# Get the list of weekday names starting from Monday to keep correct days order
weekdays_starting_from_monday = list(calendar.day_name)
weekend_days = weekdays_starting_from_monday[5:]
sunday_and_monday = [6, 0]

def get_birthdays_per_week(users):
    today = datetime.today().date()
    today_day = today.weekday()
    birthdays_per_week = defaultdict(list)

    # if today is Sunday || Monday - replace today with prev Saturday
    # for Sunday || Monday next weekend BDs should be moved to the next Monday
    # and prev weekend BDs - to the current Monday
    is_today_sunday_or_monday = today_day in sunday_and_monday
    if is_today_sunday_or_monday:
        days_until_previous_saturday = (today_day - 5) % 7
        today = today - timedelta(days=days_until_previous_saturday)

    for user in users:
        user_name = user["name"]
        birthday = datetime.strptime(user["birthday"], date_format_default)
        birthday = birthday.date()
        birthday_this_year = birthday.replace(year=today.year)

        # if day is before today - move to the next year
        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        # include only birthdays within the next 7 days
        delta_days = (birthday_this_year - today).days
        if delta_days >= 7:
            continue

        day_name = birthday_this_year.strftime("%A")

        # if BD on the weekend - move to the next Monday
        if day_name in weekend_days:
            day_name = weekdays_starting_from_monday[0]

        birthdays_per_week[day_name].append(user_name)

    # ? iterate through weekdays_starting_from_monday to keep days order
    for week_day in weekdays_starting_from_monday:
        if not week_day in birthdays_per_week:
            continue
        names = ', '.join(birthdays_per_week[week_day])
        print('{:<18}: {:<}'.format(CYAN + week_day + RESET, names))
