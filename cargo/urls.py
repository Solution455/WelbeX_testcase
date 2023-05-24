from django.urls import path

from cargo.views import CargoCreateAPIView, CargoListAPIView, CargoDetailAPIView, \
    CarUpdateAPIView, CargoUpdateAPIView, CargoDeleteAPIView

urlpatterns = [
    path('cargos/', CargoCreateAPIView.as_view(), name='cargo-create'),
    path('cargos/list/', CargoListAPIView.as_view(), name='cargo-list'),
    path('cargos/<int:pk>/', CargoDetailAPIView.as_view(), name='cargo-detail'),
    path('cars/update/<int:pk>/', CarUpdateAPIView.as_view(), name='car-update'),
    path('cargos/update/<int:pk>/', CargoUpdateAPIView.as_view(), name='cargo-update'),
    path('cargos/delete/<int:pk>/', CargoDeleteAPIView.as_view(), name='cargo-delete'),
]
