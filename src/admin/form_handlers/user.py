from datetime import datetime

from flask import flash, redirect, url_for, render_template
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from markupsafe import Markup
from werkzeug.security import generate_password_hash

from dbase import db, Users
from forms import AddUserForm, EditUserForm, DeactivateUserForm, EditUserRightsForm


class FormHandlerUser(FlaskView):
    route_base = '/'

    @route('/add_user', methods=['POST'])
    def add_user(self):
        if (not current_user.right_users):
            return render_template('admin/access_denied.html')
        addUserForm = AddUserForm()
        if addUserForm.validate_on_submit():
            name = addUserForm.name.data
            username = addUserForm.username.data
            password = generate_password_hash(addUserForm.password.data)
            post = addUserForm.post.data
            right_users = addUserForm.right_user.data
            if not (name and username):
                flash('Неправильно заполнены поля', category='danger')
            else:
                user = Users(username=username, name=name, psswd=password, post=post, right_users=right_users)
                try:
                    db.session.add(user)
                    db.session.commit()
                    flash("Пользователь добавлен", category='success')
                except:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.users'))


    @route('/edit_user', methods=["POST"])
    @login_required
    def edit_user(self):
        if (not current_user.right_users):
            return render_template('admin/access_denied.html')
        editUserForm = EditUserForm()
        if editUserForm.validate_on_submit():
            id = editUserForm.id.data
            name = editUserForm.name.data
            username = editUserForm.username.data
            post = editUserForm.post.data

            if not (name and username):
                flash('Неправильно заполнены поля', category='danger')
            else:
                user = Users.query.get(id)
                user.name = name
                user.username = username
                user.post = post
                try:
                    db.session.commit()
                    flash("Изменение пользовательских данных прошло успешно", category='success')
                except:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.users'))


    @route('/deactivate_user', methods=["POST"])
    @login_required
    def deactivate_user(self):
        if (not current_user.right_users):
            return render_template('admin/access_denied.html')
        deactivateUserForm = DeactivateUserForm()
        if deactivateUserForm.validate_on_submit():

            id = int(deactivateUserForm.id.data)
            if current_user.id == id or id == 1:
                flash('Вы не можете деактивировать собственный аккаунт или аккаунт админа', category='danger')
            else:
                user = Users.query.get(id)
                name = user.name
                user.is_deactivated = True
                user.deactivation_date = datetime.now()
                try:
                    db.session.commit()
                    flash(Markup("<strong>Деактивирован пользователь:</strong> " + name), category='success')
                except:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.users'))


    @route('/edit_user_rights', methods=["POST"])
    @login_required
    def edit_user_rights(self):
        if (not current_user.right_users):
            return render_template('admin/access_denied.html')
        editUserForm = EditUserRightsForm()
        if editUserForm.validate_on_submit():
            id = int(editUserForm.id.data)
            right_category = editUserForm.right_category.data
            right_users = editUserForm.right_users.data
            right_qa = editUserForm.right_qa.data
            right_synonym = editUserForm.right_synonym.data
            right_black_word = editUserForm.right_black_word.data
            if current_user.id == id or id == 1:
                flash('Вы не можете менять собственные права или права админа', category='danger')
            else:
                user = Users.query.get(id)
                user.right_category = right_category
                user.right_users = right_users
                user.right_qa = right_qa
                user.right_synonym = right_synonym
                user.right_black_word = right_black_word
                try:
                    db.session.commit()
                    flash("Изменение пользовательских данных прошло успешно", category='success')
                except:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.users_rights'))