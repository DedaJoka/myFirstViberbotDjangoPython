from django.contrib import admin
from .models import Provider, City, UtilityTariff
from django.utils.translation import gettext_lazy as _


class ProviderInline(admin.TabularInline):
    model = City.providers.through
    extra = 0
    can_delete = False

class UtilityTariffInline(admin.TabularInline):
    model = UtilityTariff
    extra = 0
    fields = ['city', 'utility_type', 'description_tariff_1', 'tariff_1', 'description_tariff_2', 'tariff_2']
    readonly_fields = ['city', 'utility_type', 'description_tariff_1', 'tariff_1', 'description_tariff_2', 'tariff_2']
    can_delete = False

class CityGasUrlListFilter(admin.SimpleListFilter):
    title = _('Природний газ')
    parameter_name = 'city_gas_url'
    def lookups(self, request, model_admin):
        return (
            ('has_url', 'Містить дані'),
            ('no_url', 'Не містить дані'),
        )
    def queryset(self, request, queryset):
        if self.value() == 'has_url':
            return queryset.exclude(
                gas_url=""
            )
        if self.value() == 'no_url':
            return queryset.filter(
                gas_url=""
            )
class CityWaterUrlListFilter(admin.SimpleListFilter):
    title = _('Водопостачання та водовідведення')
    parameter_name = 'city_water_url'
    def lookups(self, request, model_admin):
        return (
            ('has_url', 'Містить дані'),
            ('no_url', 'Не містить дані'),
        )
    def queryset(self, request, queryset):
        if self.value() == 'has_url':
            return queryset.exclude(
                water_url=""
            )
        if self.value() == 'no_url':
            return queryset.filter(
                water_url=""
            )
class CityHotwaterUrlListFilter(admin.SimpleListFilter):
    title = _('Гаряча вода')
    parameter_name = 'city_hotwater_url'
    def lookups(self, request, model_admin):
        return (
            ('has_url', 'Містить дані'),
            ('no_url', 'Не містить дані'),
        )
    def queryset(self, request, queryset):
        if self.value() == 'has_url':
            return queryset.exclude(
                hotwater_url=""
            )
        if self.value() == 'no_url':
            return queryset.filter(
                hotwater_url=""
            )
class CityElectricUrlListFilter(admin.SimpleListFilter):
    title = _('Електроенергія')
    parameter_name = 'city_electric_url'
    def lookups(self, request, model_admin):
        return (
            ('has_url', 'Містить дані'),
            ('no_url', 'Не містить дані'),
        )
    def queryset(self, request, queryset):
        if self.value() == 'has_url':
            return queryset.exclude(
                electric_url=""
            )
        if self.value() == 'no_url':
            return queryset.filter(
                electric_url=""
            )
class CityHeatingUrlListFilter(admin.SimpleListFilter):
    title = _('Опалення')
    parameter_name = 'city_heating_url'
    def lookups(self, request, model_admin):
        return (
            ('has_url', 'Містить дані'),
            ('no_url', 'Не містить дані'),
        )
    def queryset(self, request, queryset):
        if self.value() == 'has_url':
            return queryset.exclude(
                heating_url=""
            )
        if self.value() == 'no_url':
            return queryset.filter(
                heating_url=""
            )

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', "date_check")
    inlines = [ProviderInline]
    ordering = ['name']
    search_fields = ['name']
    filter_horizontal = ['providers']
    list_filter = [CityGasUrlListFilter, CityWaterUrlListFilter, CityHotwaterUrlListFilter, CityElectricUrlListFilter, CityHeatingUrlListFilter]


@admin.register(UtilityTariff)
class UtilityTariffAdmin(admin.ModelAdmin):
    list_display = ['city', 'date_created', 'utility_type', 'provider', 'description_tariff_1', 'tariff_1', 'description_tariff_2', 'tariff_2']
    list_filter = ['city', 'utility_type', 'date_created']

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', )
    inlines = [UtilityTariffInline]