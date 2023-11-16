from django.contrib import admin

from main.models import Autoparts


@admin.register(Autoparts)
class AutopartsAdmin(admin.ModelAdmin):
    list_filter = ('description', 'art', 'price', 'delivery_date')
