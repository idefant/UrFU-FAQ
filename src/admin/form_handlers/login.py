from flask import redirect, url_for, flash, session, render_template
from flask_classy import FlaskView, route
from flask_login import login_user
from werkzeug.security import check_password_hash

from admin import forms
from models import Users


class FormHandlerLogin(FlaskView):
    route_base = '/'

    @route('/login_handler', methods=["POST"])
    def login_handler(self):
        login_form = forms.LoginForm()
        if login_form.validate_on_submit():
            username = login_form.username.data.lower()
            try:
                user = Users.query.filter(Users.username == username).first()
            except (NameError, AttributeError):
                return render_template("admin/error_page.html", message="Ошибка чтения из БД")
            if user and check_password_hash(user.psswd, login_form.password.data):
                login_user(user, remember=login_form.remember.data)
                session['auth_token'] = user.auth_token
                session.modified = True
                return redirect(url_for('.index'))
            flash("Неверный логин/пароль", 'danger')
        return redirect(url_for('.ViewAccount:login'))
