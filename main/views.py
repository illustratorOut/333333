import csv
import datetime
import xlwt
from django.forms import model_to_dict

from django.http import HttpResponse
from django.shortcuts import render

from main.models import Autoparts


def home(request):
    if request.method == 'POST':
        name_load_file = request.POST.get('file_load')

        def handle(path):
            category_list = []
            fieldnames = ['manufacturer', 'art', 'description', 'qty', 'price', 'storage_location', 'delivery_date',
                          'supplier']
            count = 0

            with open(path, newline='') as f:
                reader = csv.DictReader(f, delimiter=';', fieldnames=fieldnames)
                for row in reader:
                    count += 1

                    if not row['qty'].isdigit():
                        row['qty'] = 0

                    if row['delivery_date'] != "" and row['storage_location'] != "" and row['supplier'] != "":
                        try:
                            row['price'] = row['price'].replace(',', '.')
                        except Exception as e:
                            print(f'Ошибка смены знака , на . - {e}')
                        date_ref = datetime.datetime.strptime(str(row['delivery_date']), '%d.%m.%Y').date()
                        row['delivery_date'] = date_ref
                        row['storage_location'] = row['storage_location'].upper()
                        category_list.append(row)

                    else:
                        row['storage_location'] = row['storage_location'].upper()

                        if not row['delivery_date']:
                            row['delivery_date'] = datetime.date(2023, 1, 1)
                        else:
                            date_ref = datetime.datetime.strptime(str(row['delivery_date']), '%d.%m.%Y').date()
                            row['delivery_date'] = date_ref
                        if not row['storage_location']:
                            row['storage_location'] = 'нет данных'
                        if not row['supplier']:
                            row['supplier'] = 'нет данных'
                        category_list.append(row)

            Autoparts.objects.bulk_create([Autoparts(**category_item) for category_item in category_list])
            print(f'Загружено строк {len(category_list)} из / {count}')
            return count

        try:
            context = {
                'title': 'Загрузка',
                'load_file': name_load_file,
                'count': handle(name_load_file),
            }
            return render(request, 'catalog/home.html', context)
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
    font_style.alignment.horz = font_style.alignment.HORZ_CENTER
    columns = ['Производитель', 'Артикул', 'Кол-во', 'Цена', 'Место хранения']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    data = Autoparts.objects.filter(product_is_accepted=True)

    font_style = xlwt.XFStyle()
    font_style.alignment.horz = font_style.alignment.HORZ_CENTER  # Отцентровать ячейку горизонтально
    ws.col(0).width = 7000  # Ширина ячейки
    ws.col(1).width = 5000  # Ширина ячейки

    transpose = [i.price for i in data]
    for my_row in data:
        row_num = row_num + 1
        ws.write(row_num, 0, my_row.manufacturer, font_style)
        ws.write(row_num, 1, my_row.art, font_style)
        ws.write(row_num, 2, my_row.qty, font_style)
        ws.write(row_num, 3, my_row.price, font_style)
        ws.write(row_num, 4, my_row.storage_location, font_style)

    font_style = xlwt.XFStyle()
    borders = xlwt.Borders()
    # borders.left = borders.MEDIUM
    borders.bottom = borders.MEDIUM
    borders.top = borders.MEDIUM
    borders.right = borders.MEDIUM

    font = xlwt.Font()
    font.name = "Times New Roman"
    font.height = 20 * 14

    font_style.font = font
    font_style.borders = borders

    ws.write(row_num + 1, 3, sum(transpose), font_style)

    font_style = xlwt.XFStyle()
    borders = xlwt.Borders()
    borders.left = borders.MEDIUM
    borders.bottom = borders.MEDIUM
    borders.top = borders.MEDIUM
    # borders.right = borders.MEDIUM

    font = xlwt.Font()
    font.name = "Times New Roman"
    font.height = 20 * 14

    font_style.font = font
    font_style.borders = borders
    ws.write(row_num + 1, 2, 'Итого:', font_style)

    wb.save(response)
    return response
