
#  UrFU - FAQ

## О проекте вкратце

**Название проекта:** Автоматизация общения с абитуриентами

__Команда:__ Improve Yourself

__Формат системы:__  Web-сервис, телеграмм-бот

__Цель:__ Создание сервиса для автоматизации общения с абитуриентами УрФУ

__Описание проекта:__ Один или несколько форматов автоматизации ответов на частые вопросы по приему в УрФУ. Это может быть чат-бот, лендинг с удобным поиском по вопросам или любой другой подходящий сервис.

__Целевая аудитория:__ Абитуриенты УрФУ

__Основное преимущество:__  На данный момент не существует достаточно удобных аналогов решения поставленной проблемы конкретно в УРФУ, однако существует несколько сайтов, позволяющие создать своего чат-бота или FAQ-страницы для необходимых задач.
- __Недостатки:__ высокая стоимость пользования и обслуживания бота, отсутствует гибкость решения, полная зависимость от работы чужого сервиса
- __Примеры:__
     - [«Botmother»](https://botmother.com/ru)
     - [«FAQ Bot»](https://www.faqbot.ai/)

__Работа пользователя с системой:__ Пользователь заходит на сайт. Выбрав категории, легко находит необходимую информацию



##  Стек технологий: 

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



## Основные требования к ПО для пользования:

- Python 3.x

- Также пакеты для работы приложения (этот список есть в requirements.txt):

  ```
  alembic==1.6.0
  certifi==2020.12.5
  chardet==4.0.0
  click==7.1.2
  DAWG-Python==0.7.2
  docopt==0.6.2
  Flask==1.1.2
  Flask-CKEditor==0.4.6
  Flask-Classy==0.6.10
  Flask-Login==0.5.0
  Flask-Migrate==2.7.0
  Flask-Script==2.0.6
  Flask-SQLAlchemy==2.5.1
  Flask-WTF==0.14.3
  fuzzywuzzy==0.18.0
  greenlet==1.0.0
  gunicorn==20.1.0
  idna==2.10
  itsdangerous==1.1.0
  Jinja2==2.11.3
  Mako==1.1.4
  MarkupSafe==1.1.1
  pyenchant==3.2.0
  pymorphy2==0.9.1
  pymorphy2-dicts-ru==2.4.417127.4579844
  python-dateutil==2.8.1
  python-editor==1.0.4
  requests==2.25.1
  six==1.15.0
  SQLAlchemy==1.4.4
  urllib3==1.26.4
  vk-api==11.9.3
  Werkzeug==1.0.1
  WTForms==2.3.3
  ```



## Порядок установки: 

### Для разработки/дебага/тестирования (описано на Windows):

1. Установить Python с [официального сайта](https://www.python.org/)

2. Создать папку проекта и в ней виртуальное окружение

   ```sh
   mkdir project
   cd project
   python -m venv env
   ```

3. Активировать виртуальное окружение

   ```sh
   С:\...\project\env\Scripts\activate.bat
   ```

4. Скачать проект и перенести содержимое папки src в только что созданную папку `project`

5. Установка всех пакетов

   ```
   pip install -r requirements.txt
   ```

6. Перенести файлы из папки move_files в папку модуля enchant по пути

   ```
   C:\...\Lib\site-packages\enchant\data\mingw64\share\enchant\hunspell\
   ```

7. Перейти назад в папку проекта

8. Запустить файл app.py

   ```
   python app.py
   ```

9. Открыть сайт локально по адресу

   ```
   127.0.0.1:5000
   ```

   

### Для продакта (описано на Ubuntu):

Для работы будут использованы Gunicorn и Nginx. Полная инструкия находится [здесь](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04)

1. Обновить пакеты

   ```bash
   sudo apt update
   sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
   ```

2. Создание виртуальной среды Python (нужен python3-venv)

   ```bash
   sudo apt install python3-venv
   mkdir ~/app
   cd ~/app
   python3 -m venv venv
   ```

3. Активировать виртуальную среду

   ```bash
   source app/bin/activate
   ```

4. Установить  `wheel`

   ```bash
   pip install wheel
   ```

5. Установить Flask и Gunicorn

   ```bash
   pip install gunicorn flask
   ```

6. Скачать из репозитория проект и переместить файлы из директории src в только что созданную папку app на сервере

7. Установить все зависимости

   ```python
   pip install -r requirements.txt
   ```

8. Перенести файлы из папки move_files в папку модуля enchant по пути

   ```
   C:\...\Lib\site-packages\enchant\data\mingw64\share\enchant\hunspell\
   ```

9. Заменить последние 2 строки app.py на:

   ```python
   if __name__ == "__main__":
       app.run(host='0.0.0.0')
   ```

10. Разрешить доступ к порту 5000

    ```bash
    sudo ufw allow 5000
    ```

11. Проверим работу

    ```bash
    python app.py
    ```

12. Получим примерно такой вывод

    ```
    Output* Serving Flask app "app" (lazy loading)
     * Environment: production
       WARNING: Do not use the development server in a production environment.
       Use a production WSGI server instead.
     * Debug mode: off
     * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
    ```

13. Проверим работу сайта перейде по адресу

    ```
    http://your_server_ip:5000
    ```

14. Настройка Gunicorn

    ```bash
    cd ~/app
    gunicorn --bind 0.0.0.0:5000 wsgi:app
    ```

    Увидим что-то вроде

    ```
    [2018-07-13 19:35:13 +0000] [28217] [INFO] Starting gunicorn 19.9.0
    [2018-07-13 19:35:13 +0000] [28217] [INFO] Listening at: http://0.0.0.0:5000 (28217)
    [2018-07-13 19:35:13 +0000] [28217] [INFO] Using worker: sync
    [2018-07-13 19:35:13 +0000] [28220] [INFO] Booting worker with pid: 28220
    ```

15. Снова проверить работу сайта, перейдя по:

    ```
    http://your_server_ip:5000
    ```

16. Можем деактивировать виртуальную среду

    ```bash
    deactivate
    ```

17. Далее, создадим файл сервисного блока systemd. Создание файла модуля systemd позволит системе init Ubuntu автоматически запускать Gunicorn и обслуживать приложение Flask при загрузке сервера. 

    Создать единичный файл, заканчивающийся на  `.service` в пределах  `/etc/systemd/system` каталог для начала:

    ```bash
    sudo nano /etc/systemd/system/app.service
    ```

18. Заполнить файл. Вместо `<sammy>` подставить логин пользователя компьютера

    ```bash
    [Unit]
    Description=Gunicorn instance to serve app
    After=network.target
    
    [Service]
    User=<sammy>
    Group=www-data
    WorkingDirectory=/home/<sammy>/app
    Environment="PATH=/home/sammy/app/venv/bin"
    ExecStart=/home/<sammy>/app/venv/bin/gunicorn --workers 3 --bind unix:app.sock -m 007 wsgi:app
    
    [Install]
    WantedBy=multi-user.target
    ```

19. Запустить созданный сервис Gunicorn и включить его так, чтобы он запускался при загрузке

    ```bash
    sudo systemctl start app
    sudo systemctl enable app
    ```

20. Проверить состояние

    ```bash
    sudo systemctl status app
    ```

    Должен быть примерно такой вывод

    ```
    yproject.service - Gunicorn instance to serve app
       Loaded: loaded (/etc/systemd/system/app.service; enabled; vendor preset: enabled)
       Active: active (running) since Fri 2018-07-13 14:28:39 UTC; 46s ago
     Main PID: 28232 (gunicorn)
        Tasks: 4 (limit: 1153)
       CGroup: /system.slice/app.service
               ├─28232 /home/sammy/app/venv/bin/python3.6 /home/sammy/app/venv/bin/gunicorn --workers 3 --bind unix:app.sock -m 007
               ├─28250 /home/sammy/app/venv/bin/python3.6 /home/sammy/app/venv/bin/gunicorn --workers 3 --bind unix:app.sock -m 007
               ├─28251 /home/sammy/app/venv/bin/python3.6 /home/sammy/app/venv/bin/gunicorn --workers 3 --bind unix:app.sock -m 007
               └─28252 /home/sammy/app/venv/bin/python3.6 /home/sammy/app/venv/bin/gunicorn --workers 3 --bind unix:app.sock -m 007
    ```

21. Установить Nginx

    ```bash
    sudo apt install nginx
    ```

22. Cоздать новый файл конфигурации блока сервера в Nginx  `sites-available` каталог, назовем app

    ```bash
    sudo nano /etc/nginx/sites-available/app
    ```

23. Открыть серверный блок и установить прослушивание порта по умолчанию  `80`, использовать этот блок для запросов доменного имени нашего сервера: 

    Далее, давайте добавим блок местоположения, который соответствует каждому запросу. В этот блок мы включим  `proxy_params` файл, указывающий некоторые общие параметры проксирования, которые  необходимо установить.  Затем мы передадим запросы в сокет, который мы  определили с помощью  `proxy_pass` директива: 

    ```bash
    server {
        listen 80;
        server_name your_domain www.your_domain;
    
        location / {
            include proxy_params;
            proxy_pass http://unix:/home/sammy/app/app.sock;
        }
    }
    ```

24. Чтобы включить конфигурацию блока сервера Nginx, которую вы только что создали, свяжите этот файл с  `sites-enabled` каталог: 

    ```bash
    sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled
    ```

25. С помощью файла в этом каталоге вы можете проверить наличие синтаксических ошибок: 

    ```bash
    sudo nginx -t
    ```

26. Если это возвращается без указания каких-либо проблем, перезапустите процесс Nginx, чтобы прочитать новую конфигурацию: 

    ```bash
    sudo systemctl restart nginx
    ```

27. Наконец, давайте снова настроим брандмауэр.  Нам больше не нужен доступ через порт  `5000`, так что мы можем удалить это правило.  Затем мы можем разрешить полный доступ к серверу Nginx: 

    ```bash
    sudo ufw delete allow 5000
    sudo ufw allow 'Nginx Full'
    ```

28. Теперь вы должны иметь возможность перейти к доменному имени вашего сервера в веб-браузере: 

    ```
    http://your_domain
    ```



## Структура приложения:

Само приложение находится в директории src/ - она считается корнем

- /app.py - основной файл, необходимый для запуска
- /config.py - конфигурация проекта
- /models.py - файл описывающий базу данных
- /Procfile - описывает, как необходимо запускать приложение с помощью gunicorn
- /requirements.txt - список необходимых для работы модулей и версий к каждой
- /search.py - функции для работы с поиском по базе вопросов
- /dbase.db - база данных SQLite
- /wsgi.py - файл для запуска через Gunicorn и Nginx (для продакта)
- /website/website.py - Блюпринт отвечающий за работу сайта
- /website/templates/website/ - HTML-шаблоны для сайта
- /website/static/ - статичные файлы для сайта
- /static/libraries/ - используемые библиотеки
- /bot/bot.py - Блюпринт отвечающий за работу бота ВКонтакте
- /admin/admin.py - Блюпринт отвечающий за работу админки
- /admin/forms.py - файл содержащий формы из админки
- /admin/templates/admin/ - HTML-шаблоны для админки
- /admin/static/ - статичные файлы для админки
- /admin/views/ - файлы для формирования страниц админки
- /admin/form_handlers/ - обработчики форм для админки
- /admin/functions.py - функции импортируемые для работы админки
- /move_files/ - файлы, которые необходимо перенести внутрь библиотеки pyenchant

