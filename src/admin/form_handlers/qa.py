import re
from flask import request, flash, url_for, render_template, redirect
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from markupsafe import Markup
from sqlalchemy import exc

from models import db, Categories, Questions
from admin.forms import AddQAForm, EditQAForm, DeleteQAForm
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
            questions = Questions.query
        except NameError:
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")

        categories_list = [(i.id, i.name) for i in categories]
        add_qa_form.cat_id.choices = categories_list

        if not add_qa_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            question = " ".join(add_qa_form.question.data.split())
            answer = re.sub(r'<p><br></p>', '', add_qa_form.answer.data)
            cat_id = add_qa_form.cat_id.data
            is_popular = add_qa_form.popular.data

            if not (question and answer and cat_id):
                flash('Неправильно заполнены поля', category='danger')
            else:
                clear_question = convert_text(question)
                try:
                    count_questions_this_category = questions.filter(Questions.cat_id == cat_id).count()
                    count_questions_popular = questions.filter(Questions.is_popular).count()
                except (NameError, AttributeError):
                    return render_template("admin/error_page.html", message="Ошибка чтения из БД")

                priority = count_questions_this_category + 1
                popular_priority = count_questions_popular + 1

                qa = Questions(question=question, clear_question=clear_question, answer=answer, cat_id=cat_id,
                               priority=priority, is_popular=is_popular, popular_priority=popular_priority)
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
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")
        if available_categories.first() is None:
            flash('Нет ни одной категории', category='danger')
        else:
            categories_list = [(i.id, i.name) for i in available_categories]
            edit_qa_form.cat_id.choices = categories_list
            if not edit_qa_form.validate_on_submit():
                flash('Заполнены не все поля', category='danger')
            else:
                qa_id = edit_qa_form.id.data
                question = " ".join(edit_qa_form.question.data.split())
                answer = re.sub(r'<p><br></p>', '', edit_qa_form.answer.data)
                cat_id = edit_qa_form.cat_id.data
                is_popular = edit_qa_form.popular.data

                if not (question and answer and cat_id):
                    flash('Неправильно заполнены поля', category='danger')
                else:
                    clear_question = convert_text(question)

                    try:
                        questions = Questions.query
                    except NameError:
                        return render_template("admin/error_page.html", message="Ошибка чтения из БД")

                    qa = questions.get(qa_id)
                    if qa is None:
                        flash('Этот вопрос не найден', category='danger')
                    else:
                        if not qa.is_popular:
                            qa.popular_priority = questions.filter(Questions.is_popular).count() + 1
                        qa.question = question
                        qa.clear_question = clear_question
                        qa.answer = answer
                        qa.cat_id = cat_id
                        qa.is_popular = is_popular
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
        if not delete_qa_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            qa_id = delete_qa_form.id.data
            try:
                qa = Questions.query.get(qa_id)
            except NameError:
                return render_template("admin/error_page.html", message="Ошибка чтения из БД")
            if qa is None:
                flash('Эта категория не найдена', category='danger')
            else:
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
        if not sequence_id:
            flash('Последовательность элементов не была обнаружена. Порядок сортировки не был сохранен',
                  category='danger')

        list_sequence_id = sequence_id.split(",")
        cat_id = request.args.get("cat_id")

        try:
            questions = Questions.query
        except NameError:
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")

        for i in range(len(list_sequence_id)):
            if not list_sequence_id[i].isdigit():
                flash('Последовательность элементов должна из себя представлять список чисел', category='danger')
                return redirect(url_for('.ViewCategory:qa_sort'))
            if cat_id == "popular":
                questions.get(int(list_sequence_id[i])).popular_priority = i + 1
            else:
                questions.get(int(list_sequence_id[i])).priority = i + 1
        try:
            db.session.commit()
            flash('Порядок сортировки успешно обновлен', category='success')
        except exc.SQLAlchemyError:
            flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.ViewQA:qa_sort', cat_id=cat_id))
