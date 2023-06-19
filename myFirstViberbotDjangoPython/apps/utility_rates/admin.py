from django.contrib import admin
from .models import Provider, City, UtilityTariff


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', "date_check")

@admin.register(UtilityTariff)
class UtilityTariffAdmin(admin.ModelAdmin):
    list_display = ['city', 'date_created', 'utility_type', 'provider', 'description_tariff_1', 'tariff_1', 'description_tariff_2', 'tariff_2']


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', )
