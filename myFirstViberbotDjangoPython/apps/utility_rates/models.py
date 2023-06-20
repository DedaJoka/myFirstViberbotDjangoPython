from django.db import models
import datetime
from django.utils import timezone


class Provider(models.Model):
    name = models.CharField("Назва Постачальника", max_length=200)

    class Meta:
        verbose_name = 'Постачальник'
        verbose_name_plural = 'Постачальники'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField("Mісто", max_length=200)
    PARSER_TYPE = (
        ('min', 'minfin'),
        ('oth', 'other'),
    )
    gas_url = models.URLField("природний газ", max_length=200, blank=True,)
    gas_parser = models.CharField(max_length=3, choices=PARSER_TYPE, default='min')
    water_url = models.URLField("водопостачання та водовідведення", max_length=200, blank=True,)
    water_parser = models.CharField(max_length=3, choices=PARSER_TYPE, default='min')
    hotwater_url = models.URLField("гаряча вода", max_length=200, blank=True,)
    hotwater_parser = models.CharField(max_length=3, choices=PARSER_TYPE, default='min')
    electric_url = models.URLField("електроенергія", max_length=200, blank=True,)
    electric_parser = models.CharField(max_length=3, choices=PARSER_TYPE, default='min')
    heating_url = models.URLField("опалення", max_length=200, blank=True,)
    heating_parser = models.CharField(max_length=3, choices=PARSER_TYPE, default='min')
    providers = models.ManyToManyField(Provider, related_name='groups', blank=True, editable=False, verbose_name='Постачальник')
    date_check = models.DateTimeField('Дата останньої перевірки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Місто'
        verbose_name_plural = 'Міста'


class UtilityTariff(models.Model):
    UTILITY_TYPE = (
        ('gasp', 'Поставка газу'),
        ('gasd', 'Доставка газу'),
        ('watr', 'Водопостачання та водовідведення'),
        ('hotw', 'Гаряча вода'),
        ('elec', 'Електроенергія'),
        ('heat', 'Опалення'),
    )
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    date_created = models.DateTimeField('Дата створення', default=timezone.now)
    utility_type = models.CharField("Тип послуги", max_length=4, choices=UTILITY_TYPE)
    tariff_1 = models.DecimalField("Тариф 1", decimal_places=4, max_digits=10, null=True, blank=True,)
    description_tariff_1 = models.CharField("Опис тарифу 1", null=True, max_length=100, blank=True,)
    tariff_2 = models.DecimalField("Тариф 2", decimal_places=4, max_digits=10, null=True, blank=True,)
    description_tariff_2 = models.CharField("Опис тарифу 2", null=True, max_length=100, blank=True,)

    def __str__(self):
        return self.city.name

    class Meta:
        verbose_name = 'Комунальний тариф'
        verbose_name_plural = 'Комунальні тарифи'