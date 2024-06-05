from django.urls import path
from .views import ListingListCreate

urlpatterns = [
    path('listings/', ListingListCreate.as_view(), name='listing-list-create'),
]
