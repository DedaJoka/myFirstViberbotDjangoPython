import requests

from django.core.management.base import BaseCommand
from utility_rates.models import City, Provider, UtilityTariff
from django.utils import timezone
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Команда для парсингу тарифів на комунальні послуги'

    def handle(self, *args, **options):
        print("Запущена команда для парсингу тарифів на комунальні послуги")

        CityAll = City.objects.all()
        for i in CityAll:
            print(f'\n\n{i}')
            i.date_check = timezone.now()
            i.save()

            gas_url = i.gas_url
            gas_parser = i.gas_parser
            if gas_url != "" and gas_parser == 'min':
                funcGas(gas_url, i.name)


def funcGas(url, cityName):
    url = requests.get(url)
    urlBS = BeautifulSoup(url.content, 'lxml')

    # gasP tariff-table1 (постачальники)
    gas_provider = urlBS.find(id="tariff-table1")
    gas_provider = gas_provider.findAll('table')[0].findAll('tr')
    for item in gas_provider[2::2]:
        gas_provider_name = item.find_next().text
        gas_provider_tariff_month_name = "Місячний тариф на природний газ"
        gas_provider_tariff_month_value = item.find_next().find_next().find_next().find_next().find_next().text
        gas_provider_tariff_year_name = "Річний тариф на природний газ"
        gas_provider_tariff_year_value = item.find_next().find_next().find_next().find_next().find_next().find_next().find_next().text

        # Робимо формат який підходить для створення запису
        gas_provider_tariff_month_value = gas_provider_tariff_month_value.replace(",", ".")
        gas_provider_tariff_year_value = gas_provider_tariff_year_value.replace(",", ".")

        # Якщо повернуло порожній рядок перетворюємо його на "None"
        if gas_provider_tariff_month_value == "":
            gas_provider_tariff_month_value = None
            gas_provider_tariff_month_name = None
        if gas_provider_tariff_year_value == "":
            gas_provider_tariff_year_value = None
            gas_provider_tariff_year_name = None

        # Перевірка чи є Постачальник у базі, якщо ні - створюємо
        check_provider = Provider.objects.filter(
            name=gas_provider_name).exists()
        if check_provider:
            pass
        else:
            Provider(name=gas_provider_name).save()

        # Створення комунального тарифу
        UtilityTariff(
            city=City.objects.get(name=cityName),
            provider=Provider.objects.get(name=gas_provider_name),
            date_created=timezone.now(),
            utility_type='gasp',
            tariff_1=gas_provider_tariff_month_value,
            description_tariff_1=gas_provider_tariff_month_name,
            tariff_2=gas_provider_tariff_year_value,
            description_tariff_2=gas_provider_tariff_year_name
        ).save()
        print(f'Создан комунальный тариф для {City.objects.get(name=cityName)} Поставка газу')

        b = Provider.objects.get(name=gas_provider_name)
        e = City.objects.get(name=cityName)
        e.providers.add(b)