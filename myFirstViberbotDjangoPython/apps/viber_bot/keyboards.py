import pytz

from . import config
from utility_rates.models import City, Provider, UtilityTariff
from django.db.models import F

def button_def (Text, ActionType, ActionBody):
    button = {
        "Columns": 6,
        "Rows": 1,
        "Text": f"<font size=25 color=\"{config.colorTxt_button}\"><b>{Text}</b></font>",
        "BgColor": config.colorBg_button,
        "TextSize": "large",
        "TextHAlign": "center",
        "TextVAlign": "middle",
        "ActionType": ActionType,
        "ActionBody": ActionBody,
    }
    return button
def keyboard_def (Buttons, InputFieldState):
    keyboard = {
        "Type": "keyboard",
        "DefaultHeight": "false",
        "BgColor": config.colorBg_keyboard,
        "Buttons": Buttons,
        "InputFieldState": InputFieldState
    }
    return keyboard


# Клавіатури
def keyboard_start_menu(viber_id):
    buttons = []
    buttons.append(button_def(f"Комунальні тарифи", "reply", "utility_rates"))
    buttons.append(button_def(f"Налаштування", "reply", "setting"))

    keyboard = keyboard_def(buttons, "hidden")
    return keyboard
def keyboard_utility_rates(viber_id):
    buttons = []
    city_object = City.objects.all()

    for items in city_object:
        buttons.append(button_def(f"{items.name}", "reply", f"utility_rates::{items.id}"))
    buttons.append(button_def(f"До головного меню", "reply", "start"))

    keyboard = keyboard_def(buttons, "hidden")
    return keyboard
def keyboard_utility_rates_city(viber_id, city_id):
    buttons = []
    for type in UtilityTariff.UTILITY_TYPE:
        utility_tariff = UtilityTariff.objects.filter(city__id=city_id, utility_type=type[0]).order_by('-date_created')
        if utility_tariff:
            buttons.append(button_def(f"{type[1]}", "reply", f"utility_rates::{city_id}::{type[0]}"))
        else:
            pass

    if buttons:
        buttons.append(button_def(f"До головного меню", "reply", "start"))
        keyboard = keyboard_def(buttons, "hidden")
        return buttons, keyboard
    else:
        keyboard = keyboard_utility_rates(viber_id)
        return buttons, keyboard
