import csv
import random
from string import ascii_uppercase

from .models import Location


def load_locations():
    with open('cargo/csv_files/uszips.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Location.objects.create(
                city=row['city'],
                state=row['state_id'],
                zip_code=row['zip'],
                latitude=row['lat'],
                longitude=row['lng']
            )


def generate_unique_car_number():
    number = random.randint(1000, 9999)
    letter = random.choice(ascii_uppercase)
    return f"{number}{letter}"


def generate_random_location():
    location = Location.objects.order_by('?').first()
    return location
