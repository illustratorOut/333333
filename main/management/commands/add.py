from django.core.management import BaseCommand
from main.models import Autoparts
import csv
import datetime


class Command(BaseCommand):

    def handle(self, *args, **options):
        category_list = []
        # Autoparts.objects.bulk_create([Autoparts(**category_item) for category_item in category_list])

        fieldnames = ['manufacturer', 'art', 'description', 'qty', 'price', 'storage_location', 'delivery_date',
                      'supplier']
        with open('Остатки_партий_15.11.2023 21-04-22.csv', newline='') as f:
            reader = csv.DictReader(f, delimiter=';', fieldnames=fieldnames)
            for row in reader:
                date_ref = datetime.datetime.strptime(str(row['delivery_date']), '%d.%m.%Y').date()
                row['delivery_date'] = date_ref
                category_list.append(row)

        Autoparts.objects.bulk_create([Autoparts(**category_item) for category_item in category_list])
