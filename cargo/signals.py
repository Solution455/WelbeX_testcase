from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from cargo.load_data import *
from cargo.models import Car, Location


@receiver(post_migrate, sender=AppConfig)
def load_data(**kwargs):
    if not Location.objects.exists():
        load_locations()
    if not Car.objects.exists():
        for _ in range(20):
            number = generate_unique_car_number()
            current_location = generate_random_location()
            capacity = random.randint(1, 1000)
            Car.objects.create(number=number, current_location=current_location, capacity=capacity)
