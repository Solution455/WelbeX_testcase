import random

from django.db import models
from geopy.distance import geodesic


class Cargo(models.Model):
    pick_up = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='pick_up_cargos')
    delivery = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='delivery_cargos')
    weight = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cargo #{self.pk}"

    def get_closest_cars(self):
        cars = Car.objects.all().select_related('current_location')
        closest_cars = []

        for car in cars:
            car_location = car.current_location
            distance = self.calculate_distance(self.pick_up, car_location)
            if distance <= 450:
                closest_cars.append({
                    'number': car.number,
                    'distance_to_cargo': distance
                })

        return closest_cars

    def get_distance_to_cars(self):
        cars = Car.objects.all().select_related('current_location')
        cars_ = []
        for car in cars:
            car_location = car.current_location
            distance = self.calculate_distance(self.pick_up, car_location)
            cars_.append({
                'number': car.number,
                'distance_to_cargo': distance
            })
        return cars_

    @staticmethod
    def calculate_distance(location1, location2):
        point1 = (location1.latitude, location1.longitude)
        point2 = (location2.latitude, location2.longitude)
        distance = geodesic(point1, point2).miles
        return distance


class Car(models.Model):
    number = models.CharField(max_length=5)
    current_location = models.ForeignKey('Location', on_delete=models.CASCADE)
    capacity = models.IntegerField()

    def __str__(self):
        return self.number

    def set_random_location(self):
        locations = Location.objects.all()
        random_location = random.choice(locations)
        self.current_location = random_location


class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10, unique=True)
    latitude = models.FloatField(db_index=True)
    longitude = models.FloatField(db_index=True)

    def __str__(self):
        return f"{self.city}, {self.state} {self.zip_code}"
