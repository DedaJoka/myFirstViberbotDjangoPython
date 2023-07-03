import pytz

from . import config

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

# Клавиатура "Головне меню"
def keyboard_start_menu(viber_id):
    buttons = []
    buttons.append(button_def(f"Налаштування", "reply", "setting"))
    buttons.append(button_def(f"До головного меню", "reply", "start"))

    keyboard = keyboard_def(buttons, "hidden")
    return keyboard