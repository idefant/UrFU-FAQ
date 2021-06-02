from flask import render_template
from flask_classy import FlaskView, route
from flask_login import login_required, current_user

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
            return "Ошибка чтения из БД"
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
            return "Ошибка чтения из БД"
        return render_template("admin/category_sort.html", categories=categories)

    @route('/cheat_sheet_icons')
    @login_required
    def cheat_sheet_icons(self):
        return render_template('admin/cheat_sheet_icons.html')