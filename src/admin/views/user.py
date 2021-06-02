from flask import render_template, request
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from sqlalchemy import desc

import forms
from models import Categories, Questions, Users


class ViewUser(FlaskView):
    route_base = '/'

    @route('/users')
    @login_required
    def users(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')
        add_user_form = forms.AddUserForm()
        edit_user_form = forms.EditUserForm()
        deactivate_user_form = forms.DeactivateUserForm()
        change_password_user_form = forms.ChangePasswordUserForm()
        try:
            users = Users.query.filter(Users.is_deactivated.is_(False))
        except (NameError, AttributeError):
            return "Ошибка чтения из БД"
        return render_template('admin/users.html', users=users, add_user_form=add_user_form,
                               edit_user_form=edit_user_form,
                               deactivate_user_form=deactivate_user_form,
                               change_password_user_form=change_password_user_form)

    @route('/users/deactivate')
    @login_required
    def users_deactivate(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')

        activate_user_form = forms.ActivateUserForm()
        delete_user_form = forms.DeleteUserForm()
        try:
            users = Users.query.filter(Users.is_deactivated)
        except (NameError, AttributeError):
            return "Ошибка чтения из БД"
        return render_template('admin/users_deactivate.html', activate_user_form=activate_user_form,
                               delete_user_form=delete_user_form, users=users)

    @route('/users/rights')
    @login_required
    def users_rights(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')
        edit_user_rights_form = forms.EditUserRightsForm()
        try:
            users = Users.query
        except NameError:
            return "Ошибка чтения из БД"
        return render_template('admin/users_rights.html', users=users, edit_user_rights_form=edit_user_rights_form)

    @route('/colors')
    @login_required
    def colors(self):
        if not current_user.right_category:
            return render_template('admin/access_denied.html')
        cat_id_data = request.args.get("cat_id")

        qa_list = []
        is_popular_category = False

        questions = Questions.query

        try:
            categories_list = Categories.query.order_by(desc(Categories.priority))
        except (NameError, AttributeError):
            return "Ошибка чтения из БД"

        if cat_id_data is None:
            return "Категория не выбрана"
        elif cat_id_data == "popular":
            is_popular_category = True

            current_category = categories_list.get(0)
            if current_category is None:
                return "Нет такой категории в БД"
            index = categories_list.all().index(current_category)
            try:
                popular_qa_list = questions.filter(Questions.is_popular).order_by(Questions.popular_priority)
            except (NameError, AttributeError):
                return "Ошибка чтения из БД"

            for qa in popular_qa_list:
                category = categories_list.get(qa.cat_id)
                if category is not None:
                    qa_list += [(qa, category.icon_name)]

        else:

            try:
                cat_id_data = int(cat_id_data)
            except ValueError:
                return "ID категории должен быть числом"
            current_category = categories_list.get(cat_id_data)
            if current_category is None:
                return "Нет такой категории в БД"
            index = categories_list.all().index(current_category)
            if (categories_list.get(cat_id_data) == None):
                return "Нет такой категории"
            try:
                qa_list = questions.filter(Questions.cat_id == cat_id_data).order_by(Questions.priority)
            except (NameError, AttributeError):
                return "Ошибка чтения из БД"

        return render_template('admin/color_picker.html', qa_list=qa_list, categories_list=categories_list,
                               current_category=current_category, index=index, is_popular_category=is_popular_category)
