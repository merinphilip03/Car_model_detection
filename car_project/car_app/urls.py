from car_app import views
from django.urls import path

urlpatterns = [
    path('cars/', views.classify_cars, name='cars')
]
