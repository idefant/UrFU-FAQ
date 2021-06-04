from flask import Blueprint
from vk_api import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from flask import request, json
from vk_api.utils import get_random_id

from search import get_answer

from config import vk_bot_token, vk_bot_confirmation_token, bot_messages, bot_messages_emoji, bot_messages_not_found

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
    keyboard.add_button(bot_messages[1][0], color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(bot_messages[2][0], color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(bot_messages[3][0], color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()


def message_handler(data, vk):

    user_message_text = data['object']['message']['text']


    for bot_message in bot_messages:
        if bot_message[0] == user_message_text:
            bot_message_text = (bot_messages_emoji["info"] + " ") if "info" in bot_messages_emoji else ""
            send_message(data, vk, bot_message_text + bot_message[1])
            return

    result = get_answer(user_message_text)
    if type(result) == str:
        send_message(data, vk, result)
    else:
        result_count = len(result)
        if result_count == 0:
            bot_message_text = (bot_messages_emoji["not_found"] + " ") if "not_found" in bot_messages_emoji else ""
            bot_message_text += bot_messages_not_found
            send_message(data, vk, bot_message_text)
        else:
            bot_message_text = (bot_messages_emoji["found"] + " ") if "found" in bot_messages_emoji else ""
            bot_message_text += f"Найдено { str(result_count) } результата"
            send_message(data, vk, bot_message_text)
            for res in result:
                bot_message_text = (bot_messages_emoji["qa"] + " ") if "qa" in bot_messages_emoji else ""
                bot_message_text += f"{ res[1].question } \n\n { res[1].answer }"
                send_message(data, vk, bot_message_text)


def send_message(data, vk, bot_message_text):
    user_id = data['object']['message']['from_id']

    vk.messages.send(access_token=token,
                     user_id=str(user_id),
                     message=bot_message_text,
                     random_id=get_random_id(),
                     keyboard=make_keyboard(),
                     dont_parse_links=1)
