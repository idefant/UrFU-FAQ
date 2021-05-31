from flask import flash, url_for, render_template, redirect, request
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from markupsafe import Markup
from sqlalchemy import exc

from models import db, BlackWords, WhiteWords
from forms import DeleteExceptionWordForm, EditExceptionWordForm, AddExceptionWordForm


class FormHandlerExceptionWord(FlaskView):
    route_base = '/'

    @route('/add_exception_word', methods=["POST"])
    @login_required
    def add_exception_word(self):
        if not current_user.right_black_word:
            return render_template('admin/access_denied.html')

        word_type = request.args.get("word_type")

        add_exception_word_form = AddExceptionWordForm()
        if add_exception_word_form.validate_on_submit():
            word = add_exception_word_form.word.data
            if not word:
                flash('Неправильно заполнены поля', category='danger')
            else:
                if word_type == "white":
                    black_word = WhiteWords(word=word)
                elif word_type == "black":
                    black_word = BlackWords(word=word)
                else:
                    return "Ни черный ни белый"

                try:
                    db.session.add(black_word)
                    db.session.commit()
                    flash(Markup("<strong>Добавлено слово:</strong> " + word), category='success')
                except exc.SQLAlchemyError:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        if word_type == "white":
            return redirect(url_for('.white_words'))
        elif word_type == "black":
            return redirect(url_for('.black_words'))
        else:
            return "Ни черныйб ни белый"


    @route('/edit_exception_word', methods=["POST"])
    @login_required
    def edit_exception_word(self):
        if not current_user.right_black_word:
            return render_template('admin/access_denied.html')
        edit_exception_word_form = EditExceptionWordForm()
        if edit_exception_word_form.validate_on_submit():
            word_id = edit_exception_word_form.id.data
            word = edit_exception_word_form.word.data

            try:
                black_word = BlackWords.query.get(word_id)
            except NameError:
                return "Ошибка чтения из БД"
            if black_word is None:
                return "Этого слова не существует"
            black_word.word = word
            try:
                db.session.commit()
                flash(Markup("<strong>Изменено слово:</strong> " + word), category='success')
            except exc.SQLAlchemyError:
                flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.black_words'))

    @route('/delete_exception_word', methods=["POST"])
    @login_required
    def delete_exception_word(self):
        if not current_user.right_black_word:
            return render_template('admin/access_denied.html')
        delete_exception_word_form = DeleteExceptionWordForm()
        if delete_exception_word_form.validate_on_submit():
            word_id = delete_exception_word_form.id.data
            try:
                black_word = BlackWords.query.get(word_id)
            except NameError:
                return "Ошибка чтения из БД"

            if black_word is None:
                return "Этого слова не существует"
            word = black_word.word
            
            try:
                db.session.delete(black_word)
                db.session.commit()
                flash(Markup("<strong>Удалено слово:</strong> " + word), category='success')
            except exc.SQLAlchemyError:
                flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.black_words'))