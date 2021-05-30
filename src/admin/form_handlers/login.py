from flask import redirect, url_for, flash
from flask_classy import FlaskView, route
from flask_login import login_user
from werkzeug.security import check_password_hash

import forms
from models import Users


class FormHandlerLogin(FlaskView):
    route_base = '/'

    @route('/login_handler', methods=["POST"])
    def login_handler(self):
        login_form = forms.LoginForm()
        if login_form.validate_on_submit():
            user = Users.query.filter(Users.username == login_form.username.data).first()
            if user and check_password_hash(user.psswd, login_form.password.data):
                login_user(user, remember=login_form.remember.data)
                return redirect(url_for('.index'))

            flash("Неверный логин/пароль", 'danger')
        return redirect(url_for('.login'))
