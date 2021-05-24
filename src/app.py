from flask import Flask, render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from website.website import website
from admin.admin import admin
from bot.bot import bot


from dbase import db, Users


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testfaq.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(bot, url_prefix='/bot')
app.register_blueprint(website, url_prefix='/')


manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


db = SQLAlchemy(app)

app.config['SECRET_KEY'] = 'fdgfh78@#5?>gfhf89dx,v06k'

login_manager = LoginManager(app)
login_manager.login_view = 'admin.login'
login_manager.login_message = 'Для продолжения авторизуйтесь'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html')


if __name__ == "__main__":
    app.run(debug=True)
