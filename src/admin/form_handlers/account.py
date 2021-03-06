import re
from secrets import token_urlsafe
from flask import flash, url_for, redirect, render_template, session
from flask_classy import FlaskView, route
from flask_login import login_required, current_user, login_user
from sqlalchemy import exc
from werkzeug.security import check_password_hash, generate_password_hash
from models import Users, db
from admin.forms import EditAccountForm, ChangePasswordAccountForm, LoginForm


class FormHandlerAccount(FlaskView):
    route_base = '/'

    @route('/edit_account', methods=["POST"])
    @login_required
    def edit_account(self):
        edit_account_form = EditAccountForm()
        if not edit_account_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            name = " ".join(edit_account_form.name.data.split())
            username = edit_account_form.username.data
            password = edit_account_form.password.data

            if not (name and username and password):
                flash('Поля должны быть заполнены', category='danger')
            else:
                try:
                    users = Users.query
                except NameError:
                    return render_template("admin/error_page.html", message="Ошибка чтения из БД")

                if not check_password_hash(current_user.psswd, password):
                    flash('Неправильный пароль', category='danger')
                else:
                    try:
                        user = users.filter(Users.username == username).first()
                    except (NameError, AttributeError):
                        return render_template("admin/error_page.html", message="Ошибка чтения из БД")
                    if user is not None and user != current_user:
                        flash('Не должно быть 2 пользователей с одинаковыми логинами', category='danger')
                    else:
                        if not bool(re.match("^[a-z0-9._-]*$", username)):
                            flash('Логин может состоять только из латинских букв, цифр, знаков нижнего подчеркивания '
                                  '( _ ), тире ( - ), точки ( . )', category='danger')
                        else:
                            current_user.name = name
                            current_user.username = username
                            try:
                                db.session.commit()
                                flash("Изменение пользовательских данных прошло успешно", category='success')
                            except exc.SQLAlchemyError:
                                flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.ViewAccount:account'))

    @route('/change_password_account', methods=["POST"])
    @login_required
    def change_password_account(self):
        change_password_account_form = ChangePasswordAccountForm()
        if not change_password_account_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            old_password = change_password_account_form.old_password.data
            password = change_password_account_form.password.data
            password_confirm = change_password_account_form.password_confirm.data
            if not check_password_hash(current_user.psswd, old_password):
                flash('Неправильный старый пароль', category='danger')
            else:
                if password != password_confirm:
                    flash('Неправильный пароль подтверждения', category='danger')
                else:
                    current_user.psswd = generate_password_hash(password)
                    current_user.auth_token = token_urlsafe(32)
                    try:
                        db.session.commit()
                        flash("Изменение пароля прошло успешно", category='success')
                    except exc.SQLAlchemyError:
                        flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.ViewAccount:account'))

    @route('/login_handler', methods=["POST"])
    def login_handler(self):
        login_form = LoginForm()
        if not login_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
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
