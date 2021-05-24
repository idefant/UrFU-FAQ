from flask import Blueprint
from vk_api import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from flask import request, json
from vk_api.utils import get_random_id

bot = Blueprint('bot', __name__)

token = '2cc72f653d14df3eb7394cf282d770b1bcbcc256cd8097f9abedfa93baa80a56edac673466b2c7393380e'
confirmation_token = 'de39cb88'


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
    keyboard.add_button('Все вопросы', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Соц.сети УрФУ', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Приемная комиссия', color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()


def message_handler(user_message_text):
    if user_message_text == "Начать":
        bot_message_text = "Привет! Это чат-бот Уральского Федерального Университета,предназначенный для помощи " \
                           "абитуриентам в поиске информации о вузе.\n\n" \
                           "Можешь задать мне вопрос или воспользоваться кнопками для получения информации"

    elif user_message_text == "Все вопросы":
        bot_message_text = "Список всех часто задаваемых вопросов с разделением на основные категории ты сможешь " \
                           "найти на (ЭТОМ САЙТЕ)"

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

    elif user_message_text == "Приемная комиссия":
        bot_message_text = "Страница УрФУ для абитуриентов: https://vk.com/abiturient_urfu \n" \
                           "Здесь ты можешь задать интересующий тебя вопрос непосредственно сотруднику" \
                           "медиа-штата нашего университета. \n\n" \
                           "Адрес УрФУ: ул. Мира, 19, Кировский район, микрорайон Втузгородок, Екатеринбург \n\n" \
                           "Контактные данные приёмной комиссии УрФУ: https://urfu.ru/ru/applicant/contacts/ "

    else:
        bot_message_text = "Функция поиска будет введена в эксплуатацию через несколько дней"
    return bot_message_text


def send_message(data, vk):
    user_id = data['object']['message']['from_id']
    bot_message_text = message_handler(data['object']['message']['text'])

    vk.messages.send(access_token=token,
                     user_id=str(user_id),
                     message=bot_message_text,
                     random_id=get_random_id(),
                     keyboard=make_keyboard())
