import json
import re

from . import config, keyboards
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import TextMessage, PictureMessage

from utility_rates.models import City, Provider, UtilityTariff

bot_configuration = BotConfiguration(
    name=config.NAME,
    avatar=config.AVATAR,
    auth_token=config.TOKEN
)
viber = Api(bot_configuration)


@csrf_exempt
def incoming(request):
    # Получаем тело запроса
    request_body = request.body
    if not request_body:
        # Если тело запроса пустое, возвращаем ошибку
        return HttpResponseBadRequest('Пусте тіло запиту')

    # Декодуємо тіло запиту з JSON в python dict
    request_dict = json.loads(request.body.decode('utf-8'))
    event = request_dict['event']
    if (event == 'webhook' or
       event == 'unsubscribed' or
       event == 'delivered' or
       event == 'seen'):
        return HttpResponse(status=200)
    elif event == 'subscribed':
        conversation_started(request_dict)
        return HttpResponse(status=200)
    elif event == 'conversation_started':
        conversation_started(request_dict)
        return HttpResponse(status=200)
    elif event == 'message':
        message(request_dict)
        return HttpResponse(status=200)
    else:
        print(f'Undeclared event: {event}')
        return HttpResponseBadRequest(f'Undeclared event: {event}')

# Функція обробки event == 'conversation_started' and 'subscribed'
def conversation_started(request_dict):
    keyboard = keyboards.keyboard_start_menu(request_dict['user']['id'])
    response_message = TextMessage(text="Вітаю друже!",
                                   keyboard=keyboard,
                                   min_api_version=4)
    viber.send_messages(request_dict['user']['id'], [response_message])

# Функція обробки event == 'message'
def message(request_dict):
    # Отримуємо інформацію
    message = request_dict['message']
    message_type = message['type']
    message_text = message['text']
    sender = request_dict['sender']
    viber_id = sender['id']

    print(f"\nПришло:\n{message_text}\n")

    if message_text == 'setting':
        setting(viber_id)
    elif message_text == 'start':
        main_menu(viber_id)
    elif message_text == 'utility_rates':
        utility_rates(viber_id)
    elif re.match(r'^utility_rates::\d{1,2}$', message_text):
        utility_rates_city(viber_id, message_text.split('::')[1])
    elif re.match(r'^utility_rates::\d{1,2}::[a-zA-Z]{4}$', message_text):
        utility_rates_tariff(viber_id, message_text.split('::')[1], message_text.split('::')[2])
    else:
        uncertainty(viber_id)


def main_menu(viber_id):
    keyboard = keyboards.keyboard_start_menu(viber_id)
    response_message = TextMessage(
        text="Для продовження скористайтеся контекстним меню",
        keyboard=keyboard,
        min_api_version=4)
    viber.send_messages(viber_id, [response_message])
def setting(viber_id):
    keyboard = keyboards.keyboard_start_menu(viber_id)
    response_message = TextMessage(
        text="На стадії розробки",
        keyboard=keyboard,
        min_api_version=4)
    viber.send_messages(viber_id, [response_message])
def uncertainty(viber_id):
    keyboard = keyboards.keyboard_start_menu(viber_id)
    response_message = TextMessage(
        text="Не визначений діалог",
        keyboard=keyboard,
        min_api_version=4)
    viber.send_messages(viber_id, [response_message])
def utility_rates(viber_id):
    keyboard = keyboards.keyboard_utility_rates(viber_id)
    response_message = TextMessage(
        text="Оберіть місто скориставшись контекстним меню",
        keyboard=keyboard,
        min_api_version=4)
    viber.send_messages(viber_id, [response_message])
def utility_rates_city(viber_id, city_id):
    keyboard = keyboards.keyboard_utility_rates_city(viber_id, city_id)
    if keyboard[0]:
        response_message = TextMessage(
            text="Оберіть послугу скориставшись контекстним меню",
            keyboard=keyboard[1],
            min_api_version=4)
        viber.send_messages(viber_id, [response_message])
    else:
        response_message = TextMessage(
            text="На жаль для даного міста комунальні тарифи не знайдені. Оберіть інше місто скориставшись контекстним меню",
            keyboard=keyboard[1],
            min_api_version=4)
        viber.send_messages(viber_id, [response_message])
def utility_rates_tariff(viber_id, city_id, utility_type):
    keyboard = keyboards.keyboard_utility_rates_city(viber_id, city_id)
    get_city = City.objects.get(id=city_id)
    get_utility_tariff = UtilityTariff.objects.filter(city__id=city_id, utility_type=utility_type, date_created__gte=get_city.date_check)

    if get_utility_tariff:
        for i in get_utility_tariff:
            text_message = "Постачальник:"
            join_tariff = "Тарифи:\n"
            if i.tariff_1:
                join_tariff = f"{join_tariff}     {i.description_tariff_1}:\n       {i.tariff_1}"
            if i.tariff_1 and i.tariff_2:
                join_tariff = f"{join_tariff}\n"
            if i.tariff_2:
                join_tariff = f"{join_tariff}     {i.description_tariff_2}:\n       {i.tariff_2}"
            text_message = f"{text_message}\n {i.provider}\n  {join_tariff}"

            response_message = TextMessage(
                text=text_message,
                min_api_version=4)
            viber.send_messages(viber_id, [response_message])

        response_message = TextMessage(
            text="Оберіть послугу скориставшись контекстним меню",
            keyboard=keyboard[1],
            min_api_version=4)
        viber.send_messages(viber_id, [response_message])