from flask import flash, url_for
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from dbase import Users, db
from forms import EditAccountForm, ChangePasswordAccountForm


class FormHandlerAccount(FlaskView):
    route_base = '/'

    @route('/edit_account', methods=["POST"])
    @login_required
    def edit_account(self):
        editAccountForm = EditAccountForm()
        if editAccountForm.validate_on_submit():

            name = editAccountForm.name.data
            username = editAccountForm.username.data
            if not (name and username):
                flash('Неправильно заполнены поля', category='danger')
            else:
                user = Users.query.get(current_user.id)
                user.name = name
                user.username = username

                try:
                    db.session.commit()
                    flash("Изменение пользовательских данных прошло успешно", category='success')
                except:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.account'))


    @route('/change_password_account', methods=["POST"])
    @login_required
    def change_password_account(self):
        changePasswordAccountForm = ChangePasswordAccountForm()
        if changePasswordAccountForm.validate_on_submit():
            old_password = changePasswordAccountForm.old_password.data
            password = changePasswordAccountForm.password.data
            password_confirm = changePasswordAccountForm.password_confirm.data
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
                        flash("Изменение пользовательских данных прошло успешно", category='success')
                    except:
                        flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.account'))