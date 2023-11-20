import csv
import datetime
import xlwt

from django.http import HttpResponse
from django.shortcuts import render

from main.models import Autoparts


def home(request):
    if request.method == 'POST':
        name_load_file = request.POST.get('file_load')

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
                    row['price'] = row['price'].replace('.', ',')
                    category_list.append(row)

            Autoparts.objects.bulk_create([Autoparts(**category_item) for category_item in category_list])


        try:
            handle(name_load_file)
            return render(request, 'catalog/home.html', {'load_file': name_load_file, 'title': 'Загрузка'})
        except:
            return render(request, 'catalog/home.html', {'load_file1': name_load_file, 'title': 'Загрузка'})
    return render(request, 'catalog/home.html', {'title': 'Загрузка'})


def search(request):
    search_art = request.POST.get('search_art')
    if request.method == 'POST':
        if request.POST.get('search_art'):
            try:
                context = {
                    'news': Autoparts.objects.filter(art=search_art),
                    'search_art': search_art,
                }
                return render(request, 'catalog/search.html', context)
            except:
                return render(request, 'catalog/search.html')

    return render(request, 'catalog/search.html')


def storage_location(request):
    if request.method == 'POST':
        storage = request.POST.get('storage')
        context = {
            'news': Autoparts.objects.filter(storage_location=storage),
            'title': storage,
        }

        return render(request, 'catalog/storage_location.html', context)
    return render(request, 'catalog/storage_location.html', {'title': 'Место хранения'})


def checkbox(request, art, pk, status):
    task = Autoparts.objects.get(pk=pk)
    task.product_is_accepted = status
    task.save()

    context = {
        'news': Autoparts.objects.filter(art=art),
    }
    return render(request, 'catalog/search.html', context)


def storage(request, storage, pk, status):
    task = Autoparts.objects.get(pk=pk)
    task.product_is_accepted = status
    task.save()
    context = {
        'news': Autoparts.objects.filter(storage_location=storage),
        'title': storage
    }

    return render(request, 'catalog/storage_location.html', context)


def download(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="inventory.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("sheet1")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Производитель', 'Артикул', 'Количество', 'Цена', 'Место хранения']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    data = Autoparts.objects.filter(product_is_accepted=True)

    for my_row in data:
        row_num = row_num + 1
        ws.write(row_num, 0, my_row.manufacturer, font_style)
        ws.write(row_num, 1, my_row.art, font_style)
        ws.write(row_num, 2, my_row.qty, font_style)
        ws.write(row_num, 3, my_row.price, font_style)
        ws.write(row_num, 4, my_row.storage_location, font_style)

    wb.save(response)
    return response
