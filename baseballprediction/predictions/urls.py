from django.urls import path
from . import views

app_name = 'predictions'

urlpatterns = [
    path('predict/', views.prediction_view, name='prediction_view'),
]