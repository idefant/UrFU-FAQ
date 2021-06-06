from flask import flash, url_for, render_template, redirect, request
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from markupsafe import Markup
from sqlalchemy import exc
from models import db, BlackWords, WhiteWords
from admin.forms import DeleteExceptionWordForm, EditExceptionWordForm, AddExceptionWordForm


class FormHandlerExceptionWord(FlaskView):
    route_base = '/'

    @route('/add_exception_word', methods=["POST"])
    @login_required
    def add_exception_word(self):
        if not current_user.right_exception_word:
            return render_template('admin/access_denied.html')

        word_type = request.args.get("word_type")

        add_exception_word_form = AddExceptionWordForm()
        if not add_exception_word_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            word = add_exception_word_form.word.data.lower()
            word = " ".join(word.split())
            if not word:
                flash('Неправильно заполнены поля', category='danger')
            else:
                if word_type == "white":
                    try:
                        word_from_db = WhiteWords.query.filter(WhiteWords.word == word).first()
                    except (NameError, AttributeError):
                        return render_template("admin/error_page.html", message="Ошибка чтения из БД")
                    exception_word = WhiteWords(word=word)
                elif word_type == "black":
                    try:
                        word_from_db = BlackWords.query.filter(BlackWords.word == word).first()
                    except (NameError, AttributeError):
                        return render_template("admin/error_page.html", message="Ошибка чтения из БД")
                    exception_word = BlackWords(word=word)
                else:
                    flash('Это должен быть либо белый список, либо черный список слов. Третьего не дано',
                          category='danger')
                    return redirect(url_for('.index'))

                if word_from_db is not None:
                    flash('Такое слово уже существует', category='danger')
                else:
                    try:
                        db.session.add(exception_word)
                        db.session.commit()
                        flash(Markup("<strong>Добавлено слово:</strong> " + word), category='success')
                    except exc.SQLAlchemyError:
                        flash('Ошибка внесения изменений в базу данных', category='danger')
        if word_type == "white":
            return redirect(url_for('.ViewExceptionWord:white_words'))
        elif word_type == "black":
            return redirect(url_for('.ViewExceptionWord:black_words'))
        else:
            flash('Это должен быть либо белый список, либо черный список слов. Третьего не дано', category='danger')
            return redirect(url_for('.index'))

    @route('/edit_exception_word', methods=["POST"])
    @login_required
    def edit_exception_word(self):
        if not current_user.right_exception_word:
            return render_template('admin/access_denied.html')
        edit_exception_word_form = EditExceptionWordForm()

        word_type = request.args.get("word_type")

        if not edit_exception_word_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            word_id = edit_exception_word_form.id.data
            word = edit_exception_word_form.word.data.lower()
            word = " ".join(word.split())

            if not word:
                flash('Неправильно заполнены поля', category='danger')
            else:
                try:
                    white_words = WhiteWords.query
                    black_words = BlackWords.query
                except NameError:
                    return render_template("admin/error_page.html", message="Ошибка чтения из БД")

                if word_type == "white":
                    try:
                        word_from_db = WhiteWords.query.filter(WhiteWords.word == word).first()
                    except (NameError, AttributeError):
                        return render_template("admin/error_page.html", message="Ошибка чтения из БД")
                    exception_word = white_words.get(word_id)
                elif word_type == "black":
                    try:
                        word_from_db = BlackWords.query.filter(BlackWords.word == word).first()
                    except (NameError, AttributeError):
                        return render_template("admin/error_page.html", message="Ошибка чтения из БД")
                    exception_word = black_words.get(word_id)
                else:
                    flash('Это должен быть либо белый список, либо черный список слов. Третьего не дано',
                          category='danger')
                    return redirect(url_for('.index'))

                if exception_word is None:
                    flash('Этого слова не существует', category='danger')
                else:
                    if word_from_db is not None and word_from_db != exception_word:
                        flash('Такое слово уже существует. Изменения не сохранены', category='danger')
                    else:
                        exception_word.word = word
                        try:
                            db.session.commit()
                            flash(Markup("<strong>Изменено слово:</strong> " + word), category='success')
                        except exc.SQLAlchemyError:
                            flash('Ошибка внесения изменений в базу данных', category='danger')
        if word_type == "white":
            return redirect(url_for('.ViewExceptionWord:white_words'))
        elif word_type == "black":
            return redirect(url_for('.ViewExceptionWord:black_words'))
        else:
            flash('Это должен быть либо белый список, либо черный список слов. Третьего не дано', category='danger')
            return redirect(url_for('.index'))

    @route('/delete_exception_word', methods=["POST"])
    @login_required
    def delete_exception_word(self):
        if not current_user.right_exception_word:
            return render_template('admin/access_denied.html')
        word_type = request.args.get("word_type")
        delete_exception_word_form = DeleteExceptionWordForm()
        if not delete_exception_word_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            word_id = delete_exception_word_form.id.data
            try:
                white_words = WhiteWords.query
                black_words = BlackWords.query
            except NameError:
                return render_template("admin/error_page.html", message="Ошибка чтения из БД")

            if word_type == "white":
                exception_word = white_words.get(word_id)
            elif word_type == "black":
                exception_word = black_words.get(word_id)
            else:
                flash('Это должен быть либо белый список, либо черный список слов. Третьего не дано', category='danger')
                return redirect(url_for('.index'))

            if exception_word is None:
                flash('Этого слова не существует', category='danger')
            else:
                try:
                    db.session.delete(exception_word)
                    db.session.commit()
                    flash(Markup("<strong>Удалено слово:</strong> " + exception_word.word), category='success')
                except exc.SQLAlchemyError:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        if word_type == "white":
            return redirect(url_for('.ViewExceptionWord:white_words'))
        elif word_type == "black":
            return redirect(url_for('.ViewExceptionWord:black_words'))
        else:
            flash('Это должен быть либо белый список, либо черный список слов. Третьего не дано', category='danger')
            return redirect(url_for('.index'))
