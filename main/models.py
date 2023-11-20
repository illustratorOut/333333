from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Autoparts(models.Model):
    manufacturer = models.CharField(max_length=150, verbose_name='Производитель')
    art = models.CharField(max_length=150, verbose_name='Артикул')
    description = models.TextField(verbose_name='Описание')
    qty = models.IntegerField(verbose_name='Количество')
    price = models.DecimalField(**NULLABLE, max_digits=19, decimal_places=2, verbose_name='Цена')
    storage_location = models.CharField(**NULLABLE, max_length=100, verbose_name='Место хранения')
    delivery_date = models.DateField(**NULLABLE, verbose_name='Дата доставки')
    supplier = models.TextField(verbose_name='Поставщик')
    product_is_accepted = models.BooleanField(default=False)
    warehouse = models.CharField(**NULLABLE, max_length=200, verbose_name='Склад хранения')

    def __str__(self):
        return f'{self.pk} Производитель: {self.manufacturer} {self.art}'

    class Meta:
        ordering = ['product_is_accepted', '-art']
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'
