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
                funcGasProviderMin(gas_url, i.name)
                
            water_url = i.water_url
            water_parser = i.water_parser
            if water_url != "" and water_parser == 'min':
                funcWaterMin(water_url, i.name)
            
            hotwater_url = i.hotwater_url
            hotwater_parser = i.hotwater_parser
            if hotwater_url != "" and hotwater_parser == 'min':
                funcHotwaterMin(hotwater_url, i.name)


def funcGasProviderMin(url, cityName):
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
        
def funcWaterMin(url, cityName):
    url = requests.get(url)
    urlBS = BeautifulSoup(url.content, 'lxml')

    water = urlBS.find("div", class_="compact-table")
    water_provider_name = water.find(class_="gold").text
    water_tariff = water.findAll('table')[0].findAll('tr')

    water_tariff_value_1 = water_tariff[2].find_next().find_next().text
    water_tariff_value_2 = water_tariff[3].find_next().find_next().text
    water_tariff_name_1 = "Водопостачання"
    water_tariff_name_2 = "Водовідведення"

    # Робимо формат який підходить для створення запису
    water_tariff_value_1 = water_tariff_value_1.replace(",", ".")
    water_tariff_value_2 = water_tariff_value_2.replace(",", ".")

    # Якщо повернуло порожній рядок перетворюємо його на "None"
    if water_tariff_value_1 == "":
        water_tariff_value_1 = None
        water_tariff_name_1 = None
    if water_tariff_value_2 == "":
        water_tariff_value_2 = None
        water_tariff_name_2 = None

    # Перевірка чи є Постачальник у базі, якщо ні - створюємо
    check_provider = Provider.objects.filter(name=water_provider_name).exists()
    if check_provider:
        pass
    else:
        Provider(name=water_provider_name).save()
        
    # Створення комунального тарифу
    UtilityTariff(
        city=City.objects.get(name=cityName),
        provider=Provider.objects.get(name=water_provider_name),
        date_created=timezone.now(),
        utility_type='watr',
        tariff_1=water_tariff_value_1,
        description_tariff_1=water_tariff_name_1,
        tariff_2=water_tariff_value_2,
        description_tariff_2=water_tariff_name_2
    ).save()
    print(f'Создан комунальный тариф для {City.objects.get(name=cityName)} Водопостачання та Водовідведення')

    b = Provider.objects.get(name=water_provider_name)
    e = City.objects.get(name=cityName)
    e.providers.add(b)
    
def funcHotwaterMin(url, cityName):
    url = requests.get(url)
    urlBS = BeautifulSoup(url.content, 'html.parser')
    hotwater_tariff = urlBS.find("div", class_="compact-table")
    hotwater_tariff= hotwater_tariff.findAll('table')[0].findAll('tr')
    key = 0
    for item in hotwater_tariff[1:]:
        hotwater_provider_name = item.find_next().text
        hotwater_tariff_value = item.find_next().find_next().text
        hotwater_tariff_name = "Постачання гарячої води"

        # Робимо формат який підходить для створення запису
        hotwater_tariff_value = hotwater_tariff_value.replace(",", ".")

        # Якщо повернуло порожній рядок перетворюємо його на "None"
        if hotwater_tariff_value == "":
            hotwater_tariff_value = None
            hotwater_tariff_name = None

        # Перевірка чи є Постачальник у базі, якщо ні - створюємо
        check_provider = Provider.objects.filter(name=hotwater_provider_name).exists()
        if check_provider:
            pass
        else:
            Provider(name=hotwater_provider_name).save()
            
        # Створення комунального тарифу
        UtilityTariff(
            city=City.objects.get(name=cityName),
            provider=Provider.objects.get(name=hotwater_provider_name),
            date_created=timezone.now(),
            utility_type='hotw',
            tariff_1=hotwater_tariff_value,
            description_tariff_1=hotwater_tariff_name,
        ).save()
        print(f'Создан комунальный тариф для {City.objects.get(name=cityName)} Постачання гарячої води')

        b = Provider.objects.get(name=hotwater_provider_name)
        e = City.objects.get(name=cityName)
        e.providers.add(b)

