from flask import Blueprint
from vk_api import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from flask import request, json
from vk_api.utils import get_random_id

from search import get_answer

from config import vk_bot_token, vk_bot_confirmation_token

bot = Blueprint('bot', __name__)

token = vk_bot_token
confirmation_token = vk_bot_confirmation_token


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

        message_handler(data, vk)

        return 'ok'


def make_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Все вопросы', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Соц.сети УрФУ', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Приемная комиссия', color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()


def message_handler(data, vk):

    user_message_text =data['object']['message']['text']

    if user_message_text == "Начать":
        bot_message_text = "Привет! Это чат-бот Уральского Федерального Университета,предназначенный для помощи " \
                           "абитуриентам в поиске информации о вузе.\n\n" \
                           "Можешь задать мне вопрос или воспользоваться кнопками для получения информации"
        send_message(data, vk, bot_message_text)

    elif user_message_text == "Все вопросы":
        bot_message_text = "Список всех часто задаваемых вопросов с разделением на основные категории ты сможешь " \
                           "найти на (ЭТОМ САЙТЕ)"
        send_message(data, vk, bot_message_text)

    elif user_message_text == "Соц.сети УрФУ":
        bot_message_text = "Официальный сайт УрФУ: urfu.ru \n\n" \
                           "Страница УрФУ для абитуриентов: https://vk.com/abiturient_urfu \n\n" \
                           "Также, у нашего университета есть страницы в различных социальных сетях," \
                           "вот ссылки на них: \n" \
                           "💡 instagram.com/urfu.ru \n" \
                           "💡 t.me/urfu_ru \n" \
                           "💡 facebook.com/ural.federal.university \n" \
                           "💡 twitter.com/urfu \n" \
                           "💡 ok.ru/uralfederal \n" \
                           "💡 tiktok.com/@urfu.ru"
        send_message(data, vk, bot_message_text)

    elif user_message_text == "Приемная комиссия":
        bot_message_text = "Страница УрФУ для абитуриентов: https://vk.com/abiturient_urfu \n" \
                           "Здесь ты можешь задать интересующий тебя вопрос непосредственно сотруднику" \
                           "медиа-штата нашего университета. \n\n" \
                           "Адрес УрФУ: ул. Мира, 19, Кировский район, микрорайон Втузгородок, Екатеринбург \n\n" \
                           "Контактные данные приёмной комиссии УрФУ: https://urfu.ru/ru/applicant/contacts/ "
        send_message(data, vk, bot_message_text)

    else:
        result = get_answer(user_message_text)
        result_count = len(result)
        if result_count == 0:
            bot_message_text = "Ничего не найдено"
            send_message(data, vk, bot_message_text)
        else:
            send_message(data, vk, "Найдено " + str(result_count) + " результата")
            for res in result:
                bot_message_text = str(res[0]) + " "
                bot_message_text += res[1].question
                send_message(data, vk, bot_message_text)


def send_message(data, vk, bot_message_text):
    user_id = data['object']['message']['from_id']

    vk.messages.send(access_token=token,
                     user_id=str(user_id),
                     message=bot_message_text,
                     random_id=get_random_id(),
                     keyboard=make_keyboard())
