from django.urls import path

from main.views import home, search, storage_location, checkbox, storage, download

urlpatterns = [
    path('', home),
    path('search', search),
    path('search/<str:art>/<int:pk>/<str:status>', checkbox, name='checkbox'),
    path('storage_location/<str:storage>/<int:pk>/<str:status>', storage, name='storage'),
    path('storage_location', storage_location),
    path('download', download),
]
