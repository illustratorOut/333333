from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Autoparts(models.Model):
    manufacturer = models.CharField(max_length=150, verbose_name='Производитель')
    art = models.CharField(max_length=150, verbose_name='Артикул')
    description = models.TextField(verbose_name='Описание')
    qty = models.IntegerField(verbose_name='Количество')
    price = models.DecimalField(**NULLABLE, max_digits=19, decimal_places=2, verbose_name='Цена')
    # price = models.CharField(max_length=150, **NULLABLE, verbose_name='Цена')
    storage_location = models.CharField(**NULLABLE, max_length=100, verbose_name='Место хранения', default='нет данных')
    ref_storage = models.CharField(**NULLABLE, max_length=100, verbose_name='Изменённое место хранения')
    delivery_date = models.DateField(**NULLABLE, verbose_name='Дата доставки', default='нет данных')
    supplier = models.TextField(**NULLABLE, verbose_name='Поставщик', default='нет данных')
    product_is_accepted = models.BooleanField(default=False)
    photo = models.ImageField(**NULLABLE, upload_to='blog/', verbose_name='Изображение')

    # warehouse = models.CharField(**NULLABLE, max_length=200, verbose_name='Склад хранения')

    def __str__(self):
        return f'{self.pk} Производитель: {self.manufacturer} {self.art}'

    class Meta:
        ordering = ['product_is_accepted', '-art']
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'
