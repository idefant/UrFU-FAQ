from flask import request, flash, url_for, render_template
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from markupsafe import Markup
from werkzeug.utils import redirect

from dbase import db, Categories, Questions
from forms import AddQAForm, EditQAForm, DeleteQAForm


class FormHandlerQA(FlaskView):
    route_base = '/'


    @route('/add_qa', methods=["POST"])
    @login_required
    def add_qa(self):
        if (not current_user.right_qa):
            return render_template('admin/access_denied.html')
        cat_id_data = request.args.get("cat_id")
        popular_data = request.args.get("popular")
        addQAForm = AddQAForm()
        categories = db.session.query(Categories)
        categories_list = [(i.id, i.name) for i in categories]
        addQAForm.cat_id.choices = categories_list
        if addQAForm.validate_on_submit():
            questions = db.session.query(Questions)


            question = addQAForm.question.data
            clear_question = question
            answer = addQAForm.answer.data
            cat_id = addQAForm.cat_id.data

            count_questions_this_cat = questions.filter(Questions.cat_id == cat_id).count()
            count_questions_popular = questions.filter(Questions.is_popular).count()

            priority = count_questions_this_cat + 1
            is_popular = addQAForm.popular.data
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
                    flash(Markup("<strong>Добавлен вопрос:</strong> " + question + "<br><strong>Категория:</strong> " + categories.get(cat_id).name), category='success')
                except:
                    flash('Ошибка внесения изменений в базу данных', category='danger')

        return redirect(url_for('.qa', cat_id=cat_id_data, popular=popular_data))


    @route('/edit_qa', methods=["POST"])
    @login_required
    def edit_qa(self):
        if (not current_user.right_qa):
            return render_template('admin/access_denied.html')
        cat_id_data = request.args.get("cat_id")
        popular_data = request.args.get("popular")

        editQAForm = EditQAForm()
        available_categories = db.session.query(Categories).all()
        categories_list = [(i.id, i.name) for i in available_categories]
        editQAForm.cat_id.choices = categories_list
        if editQAForm.validate_on_submit():
            id = editQAForm.id.data
            question = editQAForm.question.data
            clear_question = question
            answer = editQAForm.answer.data
            cat_id = editQAForm.cat_id.data
            priority = 0
            is_popular = editQAForm.popular.data
            popular_priority = 0

            if not (question and answer):
                flash('Неправильно заполнены поля', category='danger')
            else:
                qa = Questions.query.get(id)

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
                    # return redirect(url_for('.qa'))
                except:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.qa', cat_id=cat_id_data, popular=popular_data))


    @route('/delete_qa', methods=["POST"])
    @login_required
    def delete_qa(self):
        if (not current_user.right_qa):
            return render_template('admin/access_denied.html')
        cat_id_data = request.args.get("cat_id")
        popular_data = request.args.get("popular")

        deleteQAForm = DeleteQAForm()
        if deleteQAForm.validate_on_submit():
            id = deleteQAForm.id.data
            qa = Questions.query.get(id)
            question = qa.question
            try:
                db.session.delete(qa)
                db.session.commit()
                flash(Markup("<strong>Удален вопрос:</strong> " + question), category='success')
            except:
                flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.qa', cat_id=cat_id_data, popular=popular_data))


    @route('/change_order_qa', methods=['GET', 'POST'])
    def change_order_qa(self):
        if (not current_user.right_qa):
            return render_template('admin/access_denied.html')
        sequence_id = request.args.get("sequence_id")

        sequence_id = sequence_id.split(",")
        cat_id = request.args.get("cat_id")

        categories_list = Questions.query
        if (cat_id == "popular"):
            for i in range(len(sequence_id)):
                categories_list.get(int(sequence_id[i])).popular_priority = i + 1
        else:
            for i in range(len(sequence_id)):
                categories_list.get(int(sequence_id[i])).priority = i + 1
        try:
            db.session.commit()
            flash('Порядок сортировки успешно обновлен', category='success')
        except:
            flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.qa_sort', cat_id=cat_id))