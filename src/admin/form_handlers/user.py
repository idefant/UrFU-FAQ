import re
from secrets import token_urlsafe

from flask import flash, redirect, url_for, render_template, request
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from markupsafe import Markup
from sqlalchemy import exc
from werkzeug.security import generate_password_hash

from models import db, Users
from admin.forms import AddUserForm, EditUserForm, DeactivateUserForm, EditUserRightsForm, ActivateUserForm, \
    ChangePasswordUserForm, DeleteUserForm


class FormHandlerUser(FlaskView):
    route_base = '/'

    @route('/add_user', methods=['POST'])
    def add_user(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')
        add_user_form = AddUserForm()
        if not add_user_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            name = " ".join(add_user_form.name.data.split())
            username = add_user_form.username.data.lower()
            password = generate_password_hash(add_user_form.password.data)
            post = " ".join(add_user_form.post.data.split())
            right_category = add_user_form.right_category.data
            right_users = add_user_form.right_user.data
            right_qa = add_user_form.right_qa.data
            right_synonym = add_user_form.right_synonym.data
            right_exception_word = add_user_form.right_exception_word.data
            right_request = add_user_form.right_request.data

            if not (name and username and password and post):
                flash('Неправильно заполнены поля', category='danger')
            else:

                if not bool(re.match("^[a-z0-9._-]*$", username)):
                    flash('Логин может состоять только из латинских букв, цифр, знаков нижнего подчеркивания ( _ ), '
                          'тире ( - ), точки ( . )', category='danger')
                else:
                    try:
                        user = Users.query.filter(Users.username == username).first()
                    except (NameError, AttributeError):
                        return render_template("admin/error_page.html", message="Ошибка чтения из БД")
                    if user is not None:
                        flash('Не должно быть 2 пользователей с одинаковыми логинами', category='danger')
                    else:
                        user = Users(username=username, name=name, psswd=password, post=post,
                                     right_category=right_category, right_users=right_users, right_qa=right_qa,
                                     right_synonym=right_synonym, right_exception_word=right_exception_word,
                                     right_request=right_request, auth_token = token_urlsafe(32))
                        try:
                            db.session.add(user)
                            db.session.commit()
                            flash("Пользователь добавлен", category='success')
                        except exc.SQLAlchemyError:
                            flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.ViewUser:users'))

    @route('/edit_user', methods=["POST"])
    @login_required
    def edit_user(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')
        edit_user_form = EditUserForm()
        if not edit_user_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            name = " ".join(edit_user_form.name.data.split())
            username = edit_user_form.username.data.lower()
            post = " ".join(edit_user_form.post.data.split())

            if not edit_user_form.id.data.isdigit():
                flash('ID пользователя должен представлять из себя число', category='danger')
            else:
                user_id = int(edit_user_form.id.data)
                if current_user.id == user_id or user_id == 1:
                    flash('Вы не можете редактировать собственный аккаунт или аккаунт админа через страницу '
                          'пользователей. Воспользуйтесь аккаунтом', category='danger')
                else:

                    if not (name and username and post):
                        flash('Неправильно заполнены поля', category='danger')
                    else:
                        if not bool(re.match("^[a-z0-9._-]*$", username)):
                            flash('Логин может состоять только из латинских букв, цифр, знаков нижнего подчеркивания ( _ ), '
                                  'тире ( - ), точки ( . )', category='danger')
                        else:
                            try:
                                users = Users.query
                            except NameError:
                                return render_template("admin/error_page.html", message="Ошибка чтения из БД")
                            user = users.get(user_id)

                            if user is None:
                                flash('Нет такого пользователя', category='danger')
                            else:
                                try:
                                    another_user = users.filter(Users.username == username).first()
                                except (NameError, AttributeError):
                                    return render_template("admin/error_page.html", message="Ошибка чтения из БД")
                                if another_user is not None and another_user != user:
                                    flash('Не должно быть 2 пользователей с одинаковыми логинами', category='danger')
                                else:
                                    user.name = name
                                    user.username = username
                                    user.post = post
                                    try:
                                        db.session.commit()
                                        flash("Изменение пользовательских данных прошло успешно", category='success')
                                    except exc.SQLAlchemyError:
                                        flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.ViewUser:users'))

    @route('/change_status_user', methods=["POST"])
    @login_required
    def change_status_user(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')
        action = request.args.get("action")
        if action == "deactivate":
            change_status_user_form = DeactivateUserForm()
        elif action == "activate":
            change_status_user_form = ActivateUserForm()
        else:
            flash(Markup("Пользователь может быть лишь активированным и деактивированным. Третьего не дано"),
                  category='success')
            return redirect(url_for('.ViewUser:users'))
        if not change_status_user_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            if not change_status_user_form.id.data.isdigit():
                flash('ID пользователя должен представлять из себя число', category='danger')
            else:
                user_id = int(change_status_user_form.id.data)
                if current_user.id == user_id or user_id == 1:
                    flash('Вы не можете деактивировать собственный аккаунт или аккаунт админа', category='danger')
                else:
                    try:
                        user = Users.query.get(user_id)
                    except NameError:
                        return render_template("admin/error_page.html", message="Ошибка чтения из БД")
                    if user is None:
                        flash('Пользователя не существует', category='danger')
                    else:
                        name = user.name
                        user.is_deactivated = action == "deactivate"

                        try:
                            db.session.commit()
                            if action == "deactivate":
                                flash(Markup("<strong>Деактивирован пользователь:</strong> " + name),
                                      category='success')
                            else:
                                flash(Markup("<strong>Заново активирован пользователь:</strong> " + name),
                                      category='success')
                        except exc.SQLAlchemyError:
                            flash('Ошибка внесения изменений в базу данных', category='danger')
        if action == "deactivate":
            return redirect(url_for('.ViewUser:users'))
        return redirect(url_for('.ViewUser:users_deactivate'))

    @route('/delete_user', methods=["POST"])
    @login_required
    def delete_user(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')
        delete_user_form = DeleteUserForm()
        if not delete_user_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            if current_user.id != 1:
                flash("Удалять пользователей может лишь админ", category='danger')
            else:
                if not delete_user_form.id.data.isdigit():
                    flash('ID пользователя должен представлять из себя число', category='danger')
                else:
                    user_id = int(delete_user_form.id.data)
                    if current_user.id == user_id:
                        flash('Вы не можете удалвить собственный аккаунт', category='danger')
                    else:
                        try:
                            user = Users.query.get(user_id)
                        except NameError:
                            return render_template("admin/error_page.html", message="Ошибка чтения из БД")

                        if user is None:
                            flash('Пользователя не существует', category='danger')
                        else:
                            name = user.name
                            try:
                                db.session.delete(user)
                                db.session.commit()
                                flash(Markup("<strong>Удален пользователь:</strong> " + name), category='success')
                            except exc.SQLAlchemyError:
                                flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.ViewUser:users_deactivate'))

    @route('/edit_user_rights', methods=["POST"])
    @login_required
    def edit_user_rights(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')
        edit_user_form = EditUserRightsForm()
        if not edit_user_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:

            if not edit_user_form.id.data.isdigit():
                flash('ID пользователя должен представлять из себя число', category='danger')
            else:
                user_id = int(edit_user_form.id.data)

                right_category = edit_user_form.right_category.data
                right_users = edit_user_form.right_users.data
                right_qa = edit_user_form.right_qa.data
                right_synonym = edit_user_form.right_synonym.data
                right_exception_word = edit_user_form.right_exception_word.data
                right_request = edit_user_form.right_request.data
                if current_user.id == user_id or user_id == 1:
                    flash('Вы не можете менять собственные права или права админа', category='danger')
                else:
                    try:
                        user = Users.query.get(user_id)
                    except NameError:
                        return render_template("admin/error_page.html", message="Ошибка чтения из БД")

                    if user is None:
                        flash('Пользователя не существует', category='danger')
                    else:
                        user.right_category = right_category
                        user.right_users = right_users
                        user.right_qa = right_qa
                        user.right_synonym = right_synonym
                        user.right_exception_word = right_exception_word
                        user.right_request = right_request
                        try:
                            db.session.commit()
                            flash("Изменение пользовательских данных прошло успешно", category='success')
                        except exc.SQLAlchemyError:
                            flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.ViewUser:users_rights'))

    @route('/change_user_password', methods=["POST"])
    @login_required
    def change_user_password(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')
        change_password_user_form = ChangePasswordUserForm()
        if not change_password_user_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            password = change_password_user_form.password.data
            if not password:
                flash('Неправильно заполнены поля', category='danger')
            else:
                if not change_password_user_form.id.data.isdigit():
                    flash('ID пользователя должен представлять из себя число', category='danger')
                else:
                    user_id = int(change_password_user_form.id.data)
                    if current_user.id == user_id or user_id == 1:
                        flash('Вы не сменить собственный пароль или пароль админа', category='danger')
                    else:
                        try:
                            user = Users.query.get(user_id)
                        except NameError:
                            return render_template("admin/error_page.html", message="Ошибка чтения из БД")

                        user.psswd = generate_password_hash(password)
                        user.auth_token = token_urlsafe(32)
                        try:
                            db.session.commit()
                            flash("Изменение пароля прошло успешно", category='success')
                        except exc.SQLAlchemyError:
                            flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.ViewUser:users'))
