from django.urls import path
from .views import new_location, success, News, index, Contact, location, locations, LocationView, factions
urlpatterns = [
    path('News', News, name = 'News'),
    path('', index, name = 'index'),
    path('Contact', Contact, name = 'Contact'),
    path('locations', locations, name='locations'),
    path('new_location/', new_location, name='new_location'),
    path('locations/<int:location_id>', location, name='location'),
    path('new_location/success/', success, name='success'),
    path('Factions', factions, name = 'factions' ),
    
]