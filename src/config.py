# Основное

data_base = 'sqlite:///testfaq.db'
secret_key = 'fdgfh78@#5?>gfhf89dx,v06k'
is_debug = True




# Бот

vk_bot_token = '2cc72f653d14df3eb7394cf282d770b1bcbcc256cd8097f9abedfa93baa80a56edac673466b2c7393380e'
vk_bot_confirmation_token = '47e80731'

bot_messages_button = [
    ("Начать", "Привет! Это чат-бот Уральского Федерального Университета, предназначенный для помощи абитуриентам"
               "в поиске информации о вузе.\n\n"
               "Можешь задать мне вопрос или воспользоваться кнопками для получения информации"),
    ("Все вопросы", "Список всех часто задаваемых вопросов с разделением на основные категории ты сможешь найти"
                    "на faq.urfu.ru"),
    ("Соц.сети УрФУ", "Официальный сайт УрФУ: urfu.ru \n\n"
                      "Страница УрФУ для абитуриентов: https://vk.com/abiturient_urfu \n\n"
                      "Также, у нашего университета есть страницы в различных социальных сетях, вот ссылки на них: \n"
                      "💡 instagram.com/urfu.ru \n"
                      "💡 t.me/urfu_ru \n"
                      "💡 facebook.com/ural.federal.university \n"
                      "💡 twitter.com/urfu \n"
                      "💡 ok.ru/uralfederal \n"
                      "💡 tiktok.com/@urfu.ru"),
    ("Приемная комиссия", "Страница УрФУ для абитуриентов: https://vk.com/abiturient_urfu \n"
                          "Здесь ты можешь задать интересующий тебя вопрос непосредственно сотруднику медиа-штата"
                          "нашего университета. \n\n"
                          "Адрес УрФУ: ул. Мира, 19, Кировский район, микрорайон Втузгородок, Екатеринбург \n\n"
                          "Контактные данные приёмной комиссии УрФУ: https://urfu.ru/ru/applicant/contacts/")
]

bot_messages_emoji = {
    "info": "ℹ",
    "qa": "🔥",
    "found": "✅",
    "not_found": "❌"
}

bot_messages_not_found = "Ничего не найдено. Попробуйте переформулировать вопрос или найдите его на сайте faq.urfu.ru"
bot_messages_break_search = "Поиск временно не работает. Мы уже чиним"
bot_messages_too_long_require = "Слишком длинный вопрос. Попробуйте объяснится покороче или найдите его на сайте " \
                                "faq.urfu.ru"




# Веб-сайт

desktop_top_menu = [
    ("Прием УрФУ!", "https://urfu.ru/priemurfu/"),
    ("Официальная информация", "https://urfu.ru/applicant"),
    ("Кабинет абитуриента", "https://priem.urfu.ru/")
]

mobile_side_menu = [
    ("Прием УрФУ!", "https://urfu.ru/priemurfu/"),
    ("Официальная информация", "https://urfu.ru/applicant"),
    ("Кабинет абитуриента", "https://priem.urfu.ru/")
]

contact_tel = ("+7 (343) 375-44-44", "tel:+73433754444")
site_title = "Как поступить в УрФУ?"
site_subtitle = "Все вопросы, которые ты можешь задать при поступлении в УрФУ, мы собрали на одной странице. " \
                "Теперь поступить правильно стало еще проще."

footer_about_university = [
    ("Университет сегодня", "https://urfu.ru/ru/about/today/"),
    ("История", "https://urfu.ru/ru/about/history/"),
    ("Виртуальный тур", "https://urfu.ru/ru/about/online-museum/"),
    ("#УрФУ100", "https://100.urfu.ru/")
]
footer_contacts = [
    ("8-800-100-50-44", "tel:88001005044"),
    ("+7 (343) 375-44-44", "tel:+73433754444"),
    ("contact@urfu.ru", "mailto:contact@urfu.ru")
]
footer_social_net = [
    ("Вконтакте", "https://vk.com/ural.federal.university"),
    ("Facebook", "https://www.facebook.com/ural.federal.university"),
    ("Instagram", "https://www.instagram.com/urfu.ru/"),
    ("Telegram", "https://t.me/urfu_ru"),
    ("Youtube", "https://www.youtube.com/user/stvTVIST"),
    ("Twitter", "https://twitter.com/urfu")
]

qa_text_shadow = True


# Админка

bot_link = "https://vk.com/im?sel=-204389904"