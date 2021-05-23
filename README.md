
#  Автоматизация общения с абитуриентами

__Команда:__ Improve Yourself

__Формат системы:__  Web-сервис, телеграмм-бот

__Цель:__ Создание сервиса для автоматизации общения с абитуриентами УрФУ

__Описание проекта:__ Один или несколько форматов автоматизации ответов на частые вопросы по приему в УрФУ. Это может быть чат-бот, лендинг с удобным поиском по вопросам или любой другой подходящий сервис.

__Целевая аудитория:__ Абитуриенты УрФУ

__Основное преимущество:__  На данный момент не существует достаточно удобных аналогов решения поставленной проблемы конкретно в УРФУ, однако существует несколько сайтов, позволяющие создать своего чат-бота или FAQ-страницы для необходимых задач.
- __Недостатки:__ высокая стоимость пользования и обслуживания бота, отсутствует гибкость решения, полная зависимость от работы чужого сервиса
- __Примеры:__
     - [«Botmother»](www.botmother.com)
     - [«FAQ Bot»](www.faqbot.ai)

 __Стек технологий:__ 
-	__Язык программирования и фреймворк__ - В проекте используется фреймворк Python'а - Flask.
-	__Веб-сайт__ - Для создания сайта используются стандартные средства для web-разработки (HTML, CSS, JS)
-   __База данных__ - Для хранения контента и технической информации - Использование одной из популярных БД
-	__Чат-бот__ - Использование API VK для работы с ВКонтакте
-	__Поисковая система__ - Использование такого набора библиотек для обработки пользовательских запросов (возможно работа с дополнительными):
    -	enchant - Проверка орфографии и исправление слов
    -	fuzzywuzzy - Многофункциональная библиотека для нечеткого сравнения строк
    -	 pymorphy2 - Приведение слов к начальной форме
-	__Админ-панель__ - Обладает функционалом для работы c категориями
    -	контентом в виде пары: вопрос-ответ в визуальном редакторе
    -	системой контроля доступа в отдельные части админки
    -	технической информацией для отладки работы поисковой системы
    -	системой сортировки вопросов для настройки популярности


__Работа пользователя с системой:__ Пользователь заходит на сайт. Выбрав категории, легко находит необходимую информацию

__Основные требования к ПО для пользования:__ 

__Порядок установки:__ 

__Структура приложения:__