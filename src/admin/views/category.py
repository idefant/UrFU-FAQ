from flask import render_template, request, flash, url_for
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from sqlalchemy import desc
from werkzeug.utils import redirect

import forms
from admin import functions
from models import Categories, Questions


class ViewCategory(FlaskView):
    route_base = '/'

    @route('/category')
    @login_required
    def category(self):
        if not current_user.right_category:
            return render_template('admin/access_denied.html')
        add_category_form = forms.AddCategoryForm()
        edit_category_form = forms.EditCategoryForm()
        delete_category_form = forms.DeleteCategoryForm()
        try:
            categories = Categories.query.order_by(Categories.priority)
            questions = Questions.query
        except (NameError, AttributeError):
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")

        categories_id_count = functions.get_categories_id_count(categories.count(), questions)
        categories_questions_count = []
        for category in categories:
            categories_questions_count += [(category, categories_id_count[category.id])]
        return render_template("admin/category.html", add_category_form=add_category_form,
                               edit_category_form=edit_category_form, delete_category_form=delete_category_form,
                               categories_questions_count=categories_questions_count)

    @route('/category/sort')
    @login_required
    def category_sort(self):
        if not current_user.right_category:
            return render_template('admin/access_denied.html')
        try:
            categories = Categories.query.filter(Categories.id != 0).order_by(Categories.priority)
        except (NameError, AttributeError):
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")
        return render_template("admin/category_sort.html", categories=categories)

    @route('/cheat_sheet_icons')
    @login_required
    def cheat_sheet_icons(self):
        return render_template('admin/cheat_sheet_icons.html')

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
