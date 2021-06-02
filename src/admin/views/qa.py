from flask import render_template, request
from flask_classy import FlaskView, route
from flask_login import login_required, current_user

import forms
from models import Categories, Questions, db


class ViewQA(FlaskView):
    route_base = '/'
    
    @route('/qa')
    @login_required
    def qa(self):
        if not current_user.right_qa:
            return render_template('admin/access_denied.html')
        cat_id_data = request.args.get("cat_id")
        popular_data = request.args.get("popular")
        add_qa_form = forms.AddQAForm()
        edit_qa_form = forms.EditQAForm()
        delete_qa_form = forms.DeleteQAForm()
        current_category = None

        try:
            categories = Categories.query
            categories_questions = db.session.query(Categories, Questions) \
                .join(Questions, Categories.id == Questions.cat_id) \
                .order_by(Questions.id)
        except (NameError, AttributeError):
            return "Ошибка чтения из БД"

        if cat_id_data is not None:
            try:
                cat_id_data = int(cat_id_data)
            except ValueError:
                return "ID категории должен быть числом"
            current_category = categories.get(cat_id_data)
            if current_category is None or cat_id_data == 0:
                return "Нет такой категории в БД"
            categories_questions = categories_questions.filter(Questions.cat_id == cat_id_data)
            add_qa_form.cat_id.default = cat_id_data

        if popular_data is not None:
            if popular_data == 'True':
                popular_data = True
            elif popular_data == 'False':
                popular_data = False
            categories_questions = categories_questions.filter(Questions.is_popular == popular_data)
            add_qa_form.popular.default = popular_data

        categories = categories.filter(Categories.id != 0)
        category_choices = [(0, "Выберете категорию")]
        category_choices += [(i.id, i.name) for i in categories]
        add_qa_form.cat_id.choices = category_choices
        edit_qa_form.cat_id.choices = category_choices
        add_qa_form.process()

        return render_template("admin/qa.html", add_qa_form=add_qa_form, edit_qa_form=edit_qa_form,
                               delete_qa_form=delete_qa_form, categories_questions=categories_questions,
                               categories=categories, cat_id_data=cat_id_data, popular_data=popular_data,
                               current_category=current_category)


    @route('/qa/sort')
    @login_required
    def qa_sort(self):
        if not current_user.right_qa:
            return render_template('admin/access_denied.html')
        questions = Questions.query
        message = ""
        cat_id_data = request.args.get("cat_id")

        try:
            categories = Categories.query
        except NameError:
            return "Ошибка чтения из БД"

        current_category = categories.get(cat_id_data)

        if cat_id_data is None:
            message = "Выбирите категорию из списка"
        elif cat_id_data == "popular":
            try:
                questions = questions.filter(Questions.is_popular).order_by(Questions.popular_priority)
            except (NameError, AttributeError):
                return "Ошибка чтения из БД"
        else:
            try:
                cat_id_data = int(cat_id_data)
            except ValueError:
                return "ID категории должен быть числом"

            if current_category is None or cat_id_data == 0:
                return "Нет такой категории в БД"

            try:
                questions = questions.filter(Questions.cat_id == cat_id_data).order_by(Questions.priority)
            except (NameError, AttributeError):
                return "Ошибка чтения из БД"

        categories = categories.filter(Categories.id != 0)

        return render_template("admin/qa_sort.html", questions=questions, categories=categories, message=message,
                               current_category=current_category, cat_id_data=cat_id_data)