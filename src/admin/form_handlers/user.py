from datetime import datetime

from flask import flash, redirect, url_for, render_template
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from markupsafe import Markup
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, Users
from forms import AddUserForm, EditUserForm, DeactivateUserForm, EditUserRightsForm, ActivateUserForm, \
    ChangePasswordUserForm


class FormHandlerUser(FlaskView):
    route_base = '/'

    @route('/add_user', methods=['POST'])
    def add_user(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')
        addUserForm = AddUserForm()
        if addUserForm.validate_on_submit():
            name = addUserForm.name.data
            username = addUserForm.username.data
            password = generate_password_hash(addUserForm.password.data)
            post = addUserForm.post.data
            right_category = addUserForm.right_category.data
            right_users = addUserForm.right_user.data
            right_qa = addUserForm.right_qa.data
            right_synonym = addUserForm.right_synonym.data
            right_black_word = addUserForm.right_black_word.data

            if not (name and username):
                flash('Неправильно заполнены поля', category='danger')
            else:

                try:
                    user = Users.query.filter(Users.username == username).first()
                except (NameError, AttributeError):
                    return "Ошибка чтения из БД"
                if user is not None:
                    return "Не должно быть 2 пользователей с одинаковыми логинами"


                user = Users(username=username, name=name, psswd=password, post=post, right_category=right_category,
                             right_users=right_users, right_qa=right_qa, right_synonym=right_synonym,
                             right_black_word=right_black_word)
                try:
                    db.session.add(user)
                    db.session.commit()
                    flash("Пользователь добавлен", category='success')
                except exc.SQLAlchemyError:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.users'))

    @route('/edit_user', methods=["POST"])
    @login_required
    def edit_user(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')
        editUserForm = EditUserForm()
        if editUserForm.validate_on_submit():
            user_id = editUserForm.id.data
            name = editUserForm.name.data
            username = editUserForm.username.data
            post = editUserForm.post.data

            if not (name and username):
                flash('Неправильно заполнены поля', category='danger')
            else:
                try:
                    user = Users.query.get(user_id)
                except NameError:
                    return "Ошибка чтения из БД"

                if user is None:
                    return "Нет такого пользователя"



                try:
                    another_user = Users.query.filter(Users.username == username).first()
                except (NameError, AttributeError):
                    return "Ошибка чтения из БД"
                if another_user is not None and another_user != user:
                    return "Не должно быть 2 пользователей с одинаковыми логинами"



                user.name = name
                user.username = username
                user.post = post
                try:
                    db.session.commit()
                    flash("Изменение пользовательских данных прошло успешно", category='success')
                except exc.SQLAlchemyError:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.users'))

    @route('/deactivate_user', methods=["POST"])
    @login_required
    def deactivate_user(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')
        deactivateUserForm = DeactivateUserForm()
        if deactivateUserForm.validate_on_submit():

            user_id = int(deactivateUserForm.id.data)
            if current_user.id == user_id or user_id == 1:
                flash('Вы не можете деактивировать собственный аккаунт или аккаунт админа', category='danger')
            else:
                try:
                    user = Users.query.get(user_id)
                except NameError:
                    return "Ошибка чтения из БД"
                if user is None:
                    return "Пользователя не существует"
                name = user.name
                user.is_deactivated = True
                user.deactivation_date = datetime.now()
                try:
                    db.session.commit()
                    flash(Markup("<strong>Деактивирован пользователь:</strong> " + name), category='success')
                except exc.SQLAlchemyError:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.users'))




    @route('/activate_user', methods=["POST"])
    @login_required
    def activate_user(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')
        activate_user_form = ActivateUserForm()
        if activate_user_form.validate_on_submit():

            user_id = int(activate_user_form.id.data)
            if current_user.id == user_id or user_id == 1:
                flash('Вы не можете деактивировать собственный аккаунт или аккаунт админа', category='danger')
            else:
                try:
                    user = Users.query.get(user_id)
                except NameError:
                    return "Ошибка чтения из БД"
                if user is None:
                    return "Пользователя не существует"
                name = user.name
                user.is_deactivated = False
                user.deactivation_date = datetime.now()
                try:
                    db.session.commit()
                    flash(Markup("<strong>Активирован пользователь:</strong> " + name), category='success')
                except exc.SQLAlchemyError:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.users_deactivate'))






    @route('/delete_user', methods=["POST"])
    @login_required
    def delete_user(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')
        activate_user_form = ActivateUserForm()
        if activate_user_form.validate_on_submit():

            if current_user.id != 1:
                flash("Удалять пользователей может лишь админ", category='danger')
            else:
                user_id = int(activate_user_form.id.data)
                if current_user.id == user_id:
                    flash('Вы не можете удалвить собственный аккаунт', category='danger')
                else:
                    try:
                        user = Users.query.get(user_id)
                    except NameError:
                        return "Ошибка чтения из БД"
                    if user is None:
                        return "Пользователя не существует"
                    name = user.name
                    try:
                        db.session.delete(user)
                        db.session.commit()
                        flash(Markup("<strong>Удален пользователь:</strong> " + name), category='success')
                    except exc.SQLAlchemyError:
                        flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.users_deactivate'))









    @route('/edit_user_rights', methods=["POST"])
    @login_required
    def edit_user_rights(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')
        edit_user_form = EditUserRightsForm()
        if edit_user_form.validate_on_submit():
            try:
                user_id = int(edit_user_form.id.data)
            except ValueError:
                return "ID пользователя должен быть числом"
            right_category = edit_user_form.right_category.data
            right_users = edit_user_form.right_users.data
            right_qa = edit_user_form.right_qa.data
            right_synonym = edit_user_form.right_synonym.data
            right_black_word = edit_user_form.right_black_word.data
            if current_user.id == user_id or user_id == 1:
                flash('Вы не можете менять собственные права или права админа', category='danger')
            else:
                try:
                    user = Users.query.get(user_id)
                except NameError:
                    return "Ошибка чтения из БД"

                if user is None:
                    return "Пользователя не существует"

                user.right_category = right_category
                user.right_users = right_users
                user.right_qa = right_qa
                user.right_synonym = right_synonym
                user.right_black_word = right_black_word
                try:
                    db.session.commit()
                    flash("Изменение пользовательских данных прошло успешно", category='success')
                except exc.SQLAlchemyError:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.users_rights'))



    @route('/change_user_password', methods=["POST"])
    @login_required
    def change_user_password(self):
        change_password_user_form = ChangePasswordUserForm()
        if change_password_user_form.validate_on_submit():
            user_id = change_password_user_form.id.data
            password = change_password_user_form.password.data
            user = Users.query.get(int(user_id))

            user.psswd = generate_password_hash(password)
            try:
                db.session.commit()
                flash("Изменение пароля прошло успешно", category='success')
            except exc.SQLAlchemyError:
                flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.users'))