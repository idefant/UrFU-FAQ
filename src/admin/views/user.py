from flask import render_template, request, flash, url_for
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from sqlalchemy import desc
from werkzeug.utils import redirect

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
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")
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
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")
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
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")
        return render_template('admin/users_rights.html', users=users, edit_user_rights_form=edit_user_rights_form)

    @route('/colors')
    @login_required
    def colors(self):
        if not current_user.right_category:
            return render_template('admin/access_denied.html')
        cat_id_data = request.args.get("cat_id")

        try:
            questions = Questions.query
            categories = Categories.query.order_by(desc(Categories.priority))
        except (NameError, AttributeError):
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")

        if cat_id_data is None:
            flash('Категория не выбрана', category='danger')
            return redirect(url_for('.ViewCategory:category'))
        elif cat_id_data == "popular":
            is_popular_category = True

            current_category = categories.get(0)
            if current_category is None:
                flash('Нет такой категории в БД', category='danger')
                return redirect(url_for('.ViewCategory:category'))
            category_index = categories.all().index(current_category)
            try:
                popular_qa_list = questions.filter(Questions.is_popular).order_by(Questions.popular_priority)
            except (NameError, AttributeError):
                return render_template("admin/error_page.html", message="Ошибка чтения из БД")

            qa_list = []
            for qa in popular_qa_list:
                category = categories.get(qa.cat_id)
                if category is not None:
                    qa_list += [(qa, category.icon_name)]

        else:
            is_popular_category = False
            if not cat_id_data.isdigit():
                flash('ID категории должен быть числом', category='danger')
                return redirect(url_for('.ViewCategory:category'))
            else:
                cat_id = int(cat_id_data)
            current_category = categories.get(cat_id)
            if current_category is None or cat_id == 0:
                flash('Нет такой категории в БД', category='danger')
                return redirect(url_for('.ViewCategory:category'))

            category_index = categories.all().index(current_category)

            try:
                qa_list = questions.filter(Questions.cat_id == cat_id).order_by(Questions.priority)
            except (NameError, AttributeError):
                return render_template("admin/error_page.html", message="Ошибка чтения из БД")

        return render_template('admin/color_picker.html', qa_list=qa_list, categories_list=categories,
                               current_category=current_category, index=category_index,
                               is_popular_category=is_popular_category)
