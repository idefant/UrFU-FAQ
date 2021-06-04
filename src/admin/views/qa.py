from flask import render_template, request, flash, url_for
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from admin import forms
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
                .join(Questions, Categories.id == Questions.cat_id)
        except (NameError, AttributeError):
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")

        if popular_data is not None:
            if popular_data == 'True':
                is_popular = True
            elif popular_data == 'False':
                is_popular = False
            else:
                flash('Фильтр может быть популярным, непопулярным и гибридным. Четвертого не дано. Фильтр сброшен',
                      category='danger')
                return redirect(url_for('.ViewQA:qa'))
            try:
                categories_questions = categories_questions.filter(Questions.is_popular == is_popular)
            except (NameError, AttributeError):
                return render_template("admin/error_page.html", message="Ошибка чтения из БД")
            if is_popular:
                categories_questions = categories_questions.order_by(Questions.popular_priority)
            add_qa_form.popular.default = is_popular

        if cat_id_data is not None:
            if not cat_id_data.isdigit():
                flash('ID категории должен быть числом', category='danger')
            else:
                cat_id_data = int(cat_id_data)
                current_category = categories.get(cat_id_data)
                if current_category is None or cat_id_data == 0:
                    flash('Нет такой категории в БД. Фильтр был сброшен', category='danger')
                    return redirect(url_for('.ViewQA:qa'))
                else:
                    try:
                        categories_questions = categories_questions.filter(Questions.cat_id == cat_id_data)\
                            .order_by(Questions.priority)
                    except (NameError, AttributeError):
                        return render_template("admin/error_page.html", message="Ошибка чтения из БД")
                    # add_qa_form.cat_id.default = cat_id_data

        try:
            categories = categories.filter(Categories.id != 0)
        except (NameError, AttributeError):
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")

        category_choices = [(0, "Выберете категорию")]
        category_choices += [(i.id, i.name) for i in categories]
        add_qa_form.cat_id.choices = category_choices
        edit_qa_form.cat_id.choices = category_choices
        # add_qa_form.process()

        return render_template("admin/qa.html", add_qa_form=add_qa_form, edit_qa_form=edit_qa_form,
                               delete_qa_form=delete_qa_form, current_category=current_category,
                               categories_questions=categories_questions.order_by(Questions.id),
                               categories=categories, cat_id_data=cat_id_data, popular_data=popular_data)

    @route('/qa/sort')
    @login_required
    def qa_sort(self):
        if not current_user.right_qa:
            return render_template('admin/access_denied.html')
        try:
            questions = Questions.query
            categories = Categories.query
        except NameError:
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")

        cat_id_data = request.args.get("cat_id")
        current_category = categories.get(cat_id_data)

        if cat_id_data is None:
            flash('Выбирите категорию из списка', category='danger')
        elif cat_id_data == "popular":
            try:
                questions = questions.filter(Questions.is_popular).order_by(Questions.popular_priority)
            except (NameError, AttributeError):
                return render_template("admin/error_page.html", message="Ошибка чтения из БД")
        else:
            if not cat_id_data.isdigit():
                flash('ID категории должен быть числом', category='danger')
            else:
                cat_id_data = int(cat_id_data)

                if current_category is None or cat_id_data == 0:
                    flash('Нет такой категории в БД. Фильтр сброшен', category='danger')
                    return redirect(url_for('.ViewQA:qa_sort'))
                else:
                    try:
                        questions = questions.filter(Questions.cat_id == cat_id_data).order_by(Questions.priority)
                    except (NameError, AttributeError):
                        return render_template("admin/error_page.html", message="Ошибка чтения из БД")

        categories = categories.filter(Categories.id != 0)

        return render_template("admin/qa_sort.html", questions=questions, categories=categories,
                               current_category=current_category, cat_id_data=cat_id_data)
