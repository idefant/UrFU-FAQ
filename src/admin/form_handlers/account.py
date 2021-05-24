from flask import flash, url_for, redirect
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from sqlalchemy import exc
from werkzeug.security import check_password_hash, generate_password_hash

from dbase import Users, db
from forms import EditAccountForm, ChangePasswordAccountForm


class FormHandlerAccount(FlaskView):
    route_base = '/'

    @route('/edit_account', methods=["POST"])
    @login_required
    def edit_account(self):
        edit_account_form = EditAccountForm()
        if edit_account_form.validate_on_submit():

            name = edit_account_form.name.data
            username = edit_account_form.username.data
            if not (name and username):
                flash('Неправильно заполнены поля', category='danger')
            else:
                try:
                    user = Users.query.get(current_user.id)
                except NameError:
                    return "Ошибка чтения из БД"

                if user is None:
                    return "Пользователя не существует"
                user.name = name
                user.username = username

                try:
                    db.session.commit()
                    flash("Изменение пользовательских данных прошло успешно", category='success')
                except exc.SQLAlchemyError:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.account'))

    @route('/change_password_account', methods=["POST"])
    @login_required
    def change_password_account(self):
        change_password_account_form = ChangePasswordAccountForm()
        if change_password_account_form.validate_on_submit():
            old_password = change_password_account_form.old_password.data
            password = change_password_account_form.password.data
            password_confirm = change_password_account_form.password_confirm.data
            user = Users.query.get(current_user.id)
            if not check_password_hash(user.psswd, old_password):
                flash('Неправильный старый пароль', category='danger')
            else:
                if password != password_confirm:
                    flash('Неправильный пароль подтверждения', category='danger')
                else:
                    user.psswd = generate_password_hash(password)
                    try:
                        db.session.commit()
                        flash("Изменение пароля прошло успешно", category='success')
                    except exc.SQLAlchemyError:
                        flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.account'))
