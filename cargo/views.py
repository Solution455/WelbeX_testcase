from django.db import transaction
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, \
    get_object_or_404

from cargo.models import Cargo, Location, Car
from cargo.serializers import CargoCreateSerializer, CargoListSerializer, \
    CargoDetailSerializer, CarUpdateSerializer, CargoUpdateSerializer, CargoDeleteSerializer


class CargoCreateAPIView(CreateAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoCreateSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        zip_code = self.request.data.get('zip_code')
        pickup_location = get_object_or_404(Location.objects.select_related(), zip_code=zip_code)
        delivery_location = get_object_or_404(Location.objects.select_related(), zip_code=zip_code)

        serializer.save(pick_up=pickup_location, delivery=delivery_location)


class CargoListAPIView(ListAPIView):
    queryset = Cargo.objects.all().select_related('pick_up', 'delivery')
    serializer_class = CargoListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        cargos_with_cars = []
        for cargo in queryset:
            cars = Cargo.get_closest_cars(cargo)
            cargo.cars = cars
            cargos_with_cars.append(cargo)
        return cargos_with_cars


class CargoDetailAPIView(RetrieveAPIView):
    queryset = Cargo.objects.all().select_related('pick_up', 'delivery')
    serializer_class = CargoDetailSerializer


class CarUpdateAPIView(UpdateAPIView):
    queryset = Car.objects.all().select_related('current_location')
    serializer_class = CarUpdateSerializer


class CargoUpdateAPIView(UpdateAPIView):
    queryset = Cargo.objects.all().select_related('pick_up', 'delivery')
    serializer_class = CargoUpdateSerializer


class CargoDeleteAPIView(DestroyAPIView):
    queryset = Cargo.objects.all().select_related('pick_up', 'delivery')
    serializer_class = CargoDeleteSerializer
