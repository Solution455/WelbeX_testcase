from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from cargo.models import Cargo, Car, Location


class CargoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['weight', 'description']


class CargoListSerializer(serializers.ModelSerializer):
    closest_cars = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = ['id', 'pick_up_id', 'delivery_id', 'closest_cars', 'created_at', 'updated_at']

    def get_closest_cars(self, obj):
        return obj.get_closest_cars()


class CargoDetailSerializer(serializers.ModelSerializer):
    cars = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = ['pick_up', 'delivery', 'weight', 'description', 'created_at', 'updated_at', 'cars']

    def get_cars(self, obj):
        return obj.get_distance_to_cars()


class CarUpdateSerializer(serializers.ModelSerializer):
    zip_code = serializers.CharField(write_only=True, required=True)
    current_location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        required=False
    )

    class Meta:
        model = Car
        fields = ['zip_code', 'number', 'capacity', 'current_location']

    def update(self, instance, validated_data):
        zip_code = validated_data.get('zip_code')
        if zip_code:
            location = get_object_or_404(Location, zip_code=zip_code)
            instance.current_location = location

        instance.number = validated_data.get('number', instance.number)
        instance.capacity = validated_data.get('capacity', instance.capacity)
        instance.save()
        return instance


class CargoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['weight', 'description']


class CargoDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = ['id']
