import csv
import datetime

from django.shortcuts import render

from main.models import Autoparts


def home(request):
    if request.method == 'POST':
        load_file = request.POST.get('file_load')
        print(load_file)

        # open('/path/to/directory/file_name.pdf', 'wb').write(load_file.content)
        def handle(path):
            category_list = []
            fieldnames = ['manufacturer', 'art', 'description', 'qty', 'price', 'storage_location', 'delivery_date',
                          'supplier']
            with open(path, newline='') as f:
                reader = csv.DictReader(f, delimiter=';', fieldnames=fieldnames)
                for row in reader:
                    date_ref = datetime.datetime.strptime(str(row['delivery_date']), '%d.%m.%Y').date()
                    row['delivery_date'] = date_ref
                    category_list.append(row)

            Autoparts.objects.bulk_create([Autoparts(**category_item) for category_item in category_list])

        try:
            handle(load_file)
            print('try')
            return render(request, 'catalog/home.html', {'load_file': load_file})
        except:
            print('false')
            return render(request, 'catalog/home.html',{'load_file1': load_file})
    print('alll')
    return render(request, 'catalog/home.html')


def search(request):
    if request.method == 'POST':
        search_art = request.POST.get('search_art')
        try:
            search_db = Autoparts.objects.filter(art=search_art)
            return render(request, 'catalog/search.html', {'news': search_db, 'search_art': search_art})
        except:
            return render(request, 'catalog/search.html')

    return render(request, 'catalog/search.html')
