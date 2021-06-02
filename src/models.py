from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from sqlalchemy import DateTime
from werkzeug.security import generate_password_hash, check_password_hash



db = SQLAlchemy()

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    icon_name = db.Column(db.String(30))
    color = db.Column(db.String(7))

    def __repr__(self):
        return '<Categories %r>' % self.id

class Questions(db.Model):      # __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(1000), nullable=False)
    clear_question = db.Column(db.String(1000))
    answer = db.Column(db.Text, nullable = False)
    cat_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    priority = db.Column(db.Integer, nullable=False)
    is_popular = db.Column(db.Boolean, default = False)
    popular_priority = db.Column(db.Integer, default = 0)

    def __repr__(self):
        return '<Questions %r>' % self.id


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    psswd = db.Column(db.Text, nullable=False)
    auth_token = db.Column(db.String)
    post = db.Column(db.String, nullable=False)
    is_deactivated = db.Column(db.Boolean, default = False)
    right_category = db.Column(db.Boolean, default = False)
    right_users = db.Column(db.Boolean, default = False)
    right_qa = db.Column(db.Boolean, default = False)
    right_synonym = db.Column(db.Boolean, default=False)
    right_exception_word = db.Column(db.Boolean, default=False)
    right_request = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Users %r>' % self.id


class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    cleared = db.Column(db.Text, nullable=False)
    date_time = db.Column(DateTime)

    def __repr__(self):
        return '<Requests %r>' % self.id


class BlackWords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<BlackWords %r>' % self.id


class WhiteWords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<BlackWords %r>' % self.id


class SynonymousWords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    synonym_id = db.Column(db.Integer)

    def __repr__(self):
        return '<SynonymousWords %r>' % self.id