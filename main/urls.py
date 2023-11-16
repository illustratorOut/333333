from django.urls import path

from main.views import home, search

urlpatterns = [
    path('', home),
    path('search', search)
]
