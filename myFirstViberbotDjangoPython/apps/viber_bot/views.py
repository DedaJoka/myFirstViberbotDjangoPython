import json
import re

from . import config, keyboards
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import TextMessage, PictureMessage

# Create your views here.

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

    # Ддекодуємо тіло запиту з JSON в python dict
    request_dict = json.loads(request.body.decode('utf-8'))
    event = request_dict['event']
    if event == 'webhook' or\
       event == 'unsubscribed' or\
       event == 'delivered' or\
       event == 'seen':
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
    keyboard = keyboards_def.keyboard_authorization()
    response_message = TextMessage(text="Вітаю друже!",
                                   keyboard=keyboard,
                                   min_api_version=4)
    viber.send_messages(request_dict['user']['id'], [response_message])

# Функція обробки event == 'message'


def message(request_dict):
    # Отримуємо інформацію
    message = request_dict['message']
    message_type = message['type']
    sender = request_dict['sender']
    viber_id = sender['id']

    keyboard = keyboards.keyboard_start_menu(viber_id)
    response_message = TextMessage(
        text='Це поки все що я вмію!',
        keyboard=keyboard,
        min_api_version=4
    )
    viber.send_messages(viber_id, [response_message])
