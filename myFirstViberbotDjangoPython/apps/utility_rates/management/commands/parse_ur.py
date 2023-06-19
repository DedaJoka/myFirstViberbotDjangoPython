from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Команда для парсингу тарифів на комунальні послуги'

    def handle(self, *args, **options):
        print("Запущена команда для парсингу тарифів на комунальні послуги")