import re
from flask import request, flash, url_for, render_template, redirect
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from markupsafe import Markup
from sqlalchemy import exc

from models import db, Categories, Questions
from forms import AddQAForm, EditQAForm, DeleteQAForm
from search import convert_text


class FormHandlerQA(FlaskView):
    route_base = '/'

    @route('/add_qa', methods=["POST"])
    @login_required
    def add_qa(self):
        if not current_user.right_qa:
            return render_template('admin/access_denied.html')
        cat_id_data = request.args.get("cat_id")
        popular_data = request.args.get("popular")
        add_qa_form = AddQAForm()
        try:
            categories = Categories.query
        except NameError:
            return "Ошибка чтения из БД"
        categories_list = [(i.id, i.name) for i in categories]
        add_qa_form.cat_id.choices = categories_list
        if add_qa_form.validate_on_submit():
            try:
                questions = Questions.query
            except NameError:
                return "Ошибка чтения из БД"

            question = add_qa_form.question.data
            clear_question = convert_text(question)

            answer = add_qa_form.answer.data
            answer = re.sub(r'<p><br></p>|<br>', '', answer)


            cat_id = add_qa_form.cat_id.data

            count_questions_this_cat = questions.filter(Questions.cat_id == cat_id).count()
            count_questions_popular = questions.filter(Questions.is_popular).count()

            priority = count_questions_this_cat + 1
            is_popular = add_qa_form.popular.data
            popular_priority = count_questions_popular + 1

            if not (question and answer):
                flash('Неправильно заполнены поля', category='danger')
            else:
                qa = Questions(question=question, clear_question=clear_question, answer=answer, cat_id=cat_id,
                               priority=priority,
                               is_popular=is_popular, popular_priority=popular_priority)
                try:
                    db.session.add(qa)
                    db.session.commit()
                    flash(Markup("<strong>Добавлен вопрос:</strong> " + question + "<br><strong>Категория:</strong> "
                                 + categories.get(cat_id).name), category='success')
                except exc.SQLAlchemyError:
                    flash('Ошибка внесения изменений в базу данных', category='danger')

        return redirect(url_for('.ViewQA:qa', cat_id=cat_id_data, popular=popular_data))

    @route('/edit_qa', methods=["POST"])
    @login_required
    def edit_qa(self):
        if not current_user.right_qa:
            return render_template('admin/access_denied.html')
        cat_id_data = request.args.get("cat_id")
        popular_data = request.args.get("popular")

        edit_qa_form = EditQAForm()
        try:
            available_categories = Categories.query
        except NameError:
            return "Ошибка чтения из БД"
        if available_categories is None:
            return "Нет ни одной категории"
        categories_list = [(i.id, i.name) for i in available_categories]
        edit_qa_form.cat_id.choices = categories_list
        if edit_qa_form.validate_on_submit():
            qa_id = edit_qa_form.id.data
            question = edit_qa_form.question.data
            clear_question = question
            answer = edit_qa_form.answer.data
            cat_id = edit_qa_form.cat_id.data
            priority = 0
            is_popular = edit_qa_form.popular.data
            popular_priority = 0

            if not (question and answer):
                flash('Неправильно заполнены поля', category='danger')
            else:
                try:
                    qa = Questions.query.get(qa_id)
                except NameError:
                    return "Ошибка чтения из БД"

                if qa is None:
                    return "Такого вопроса нет"

                qa.question = question
                qa.clear_question = clear_question
                qa.answer = answer
                qa.cat_id = cat_id
                qa.is_popular = is_popular
                # old_question.priority = priority
                # old_question.popular_priority = popular_priority
                try:
                    db.session.commit()
                    flash(Markup("<strong>Изменен вопрос:</strong> " + question), category='success')
                except exc.SQLAlchemyError:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.ViewQA:qa', cat_id=cat_id_data, popular=popular_data))

    @route('/delete_qa', methods=["POST"])
    @login_required
    def delete_qa(self):
        if not current_user.right_qa:
            return render_template('admin/access_denied.html')
        cat_id_data = request.args.get("cat_id")
        popular_data = request.args.get("popular")

        delete_qa_form = DeleteQAForm()
        if delete_qa_form.validate_on_submit():
            qa_id = delete_qa_form.id.data
            try:
                qa = Questions.query.get(qa_id)
            except NameError:
                return "Ошибка чтения из БД"
            if qa is None:
                return "Такой категории нет"
            question = qa.question
            try:
                db.session.delete(qa)
                db.session.commit()
                flash(Markup("<strong>Удален вопрос:</strong> " + question), category='success')
            except exc.SQLAlchemyError:
                flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.ViewQA:qa', cat_id=cat_id_data, popular=popular_data))

    @route('/change_order_qa', methods=['GET', 'POST'])
    def change_order_qa(self):
        if not current_user.right_qa:
            return render_template('admin/access_denied.html')
        sequence_id = request.args.get("sequence_id")

        sequence_id = sequence_id.split(",")
        cat_id = request.args.get("cat_id")

        try:
            categories_list = Questions.query
        except NameError:
            return "Ошибка чтения из БД"
        if cat_id == "popular":
            for i in range(len(sequence_id)):
                categories_list.get(int(sequence_id[i])).popular_priority = i + 1
        else:
            for i in range(len(sequence_id)):
                categories_list.get(int(sequence_id[i])).priority = i + 1
        try:
            db.session.commit()
            flash('Порядок сортировки успешно обновлен', category='success')
        except exc.SQLAlchemyError:
            flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.ViewQA:qa_sort', cat_id=cat_id))
