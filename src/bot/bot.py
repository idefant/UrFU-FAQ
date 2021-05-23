from flask import Blueprint
from vk_api import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from flask import Flask, request, json
from vk_api.utils import get_random_id


bot = Blueprint('bot', __name__)

token = '2cc72f653d14df3eb7394cf282d770b1bcbcc256cd8097f9abedfa93baa80a56edac673466b2c7393380e'
confirmation_token = '0767404b'

@bot.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        vk_session = vk_api.VkApi(token=token)
        vk = vk_session.get_api()
        send_message(data, vk)
        return 'ok'


def make_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Первая', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Вторая', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Позитив', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Негатив', color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


def message_handler(user_message_text):
    if user_message_text == "Начать":
        bot_message_text = "Это приветственное сообщение"
    elif user_message_text == "Тест":
        bot_message_text = "Слушаюсь и повинуюсь о повелитель этого проекта"
    else:
        bot_message_text = "Мне что-то найти?"
    return bot_message_text


def send_message(data, vk):
    user_id = data['object']['message']['from_id']
    bot_message_text = message_handler(data['object']['message']['text'])

    vk.messages.send(access_token=token,
                      user_id=str(user_id),
                      message=bot_message_text,
                      random_id=get_random_id(),
                      keyboard=make_keyboard())