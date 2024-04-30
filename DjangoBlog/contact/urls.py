from django.urls import path, include
from .views import about, contact

app_name = 'about'

urlpatterns = [
    path('', about, name='about'),
    path('contact/', contact, name='contact'),
]
