from flask import flash, url_for, render_template, redirect, request
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from markupsafe import Markup
from sqlalchemy import exc

from models import db, BlackWords, WhiteWords
from forms import AddBlackWordForm, EditBlackWordForm, DeleteBlackWordForm


class FormHandlerBlackWord(FlaskView):
    route_base = '/'

    @route('/add_black_word', methods=["POST"])
    @login_required
    def add_black_word(self):
        if not current_user.right_black_word:
            return render_template('admin/access_denied.html')

        word_type = request.args.get("word_type")

        add_black_word_form = AddBlackWordForm()
        if add_black_word_form.validate_on_submit():
            word = add_black_word_form.word.data
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


    @route('/edit_black_word', methods=["POST"])
    @login_required
    def edit_black_word(self):
        if not current_user.right_black_word:
            return render_template('admin/access_denied.html')
        edit_black_word_form = EditBlackWordForm()
        if edit_black_word_form.validate_on_submit():
            word_id = edit_black_word_form.id.data
            word = edit_black_word_form.word.data

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

    @route('/delete_black_word', methods=["POST"])
    @login_required
    def delete_black_word(self):
        if not current_user.right_black_word:
            return render_template('admin/access_denied.html')
        delete_black_word_form = DeleteBlackWordForm()
        if delete_black_word_form.validate_on_submit():
            word_id = delete_black_word_form.id.data
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
