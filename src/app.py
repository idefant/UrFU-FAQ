import datetime

from flask import Flask, render_template, session
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from website.website import website
from admin.admin import admin
from bot.bot import bot

from models import db, Users

from config import data_base, secret_key

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = data_base
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.permanent_session_lifetime = datetime.timedelta(days=10)

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(bot, url_prefix='/bot')
app.register_blueprint(website, url_prefix='/')
app.debug = True

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


db = SQLAlchemy(app)

app.config['SECRET_KEY'] = secret_key

login_manager = LoginManager(app)
login_manager.login_view = 'admin.login'
login_manager.login_message = 'Для продолжения авторизуйтесь'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('website/page404.html')


if __name__ == "__main__":
    app.run()
