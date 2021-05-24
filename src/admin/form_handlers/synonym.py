from flask import request, flash, url_for
from flask_classy import FlaskView, route
from flask_login import login_required
from markupsafe import Markup
from sqlalchemy import exc
from werkzeug.utils import redirect

from dbase import db, SynonymousWords
from forms import AddSynonymsDependentForm, EditSynonymsDependentForm, DeleteSynonymsDependentForm


class FormHandlerSynonym(FlaskView):
    route_base = '/'

    @route('/add_synonym', methods=["POST"])
    @login_required
    def add_synonym(self):
        add_synonyms_dependent_form = AddSynonymsDependentForm()
        main_word_id = request.args.get("word_id")
        if add_synonyms_dependent_form.validate_on_submit():
            word = add_synonyms_dependent_form.word.data
            if main_word_id:
                synonym = SynonymousWords(word=word, synonym_id=main_word_id)
            else:
                synonym = SynonymousWords(word=word)
            try:
                db.session.add(synonym)
                db.session.commit()
                flash(Markup("<strong>Добавлено слово:</strong> " + word), category='success')
            except exc.SQLAlchemyError:
                flash('Ошибка внесения изменений в базу данных', category='danger')
        if main_word_id:
            return redirect(url_for('.synonyms_replacement', word_id=main_word_id))
        return redirect(url_for('.synonyms'))

    @route('/edit_synonym', methods=["POST"])
    @login_required
    def edit_synonym(self):
        editSynonymsDependentForm = EditSynonymsDependentForm()
        main_word_id = request.args.get("word_id")
        if editSynonymsDependentForm.validate_on_submit():
            word_id = editSynonymsDependentForm.word_id.data
            word = editSynonymsDependentForm.word.data

            try:
                synonym = SynonymousWords.query.get(word_id)
            except NameError:
                return "Ошибка чтения из БД"

            if synonym is None:
                return "Нет такого слова"

            synonym.word = word
            try:
                db.session.commit()
                flash(Markup("<strong>Изменено слово:</strong> " + word), category='success')
            except exc.SQLAlchemyError:
                flash('Ошибка внесения изменений в базу данных', category='danger')
        if main_word_id:
            return redirect(url_for('.synonyms_replacement', word_id=main_word_id))
        return redirect(url_for('.synonyms'))

    @route('/delete_synonym', methods=["POST"])
    @login_required
    def delete_synonym(self):
        delete_synonyms_dependent_form = DeleteSynonymsDependentForm()
        main_word_id = request.args.get("word_id")
        if delete_synonyms_dependent_form.validate_on_submit():
            word_id = delete_synonyms_dependent_form.word_id.data

            if word_id == main_word_id:
                return "Нельзя удалять главный синоним"

            try:
                synonyms = [SynonymousWords.query.get(word_id)]
            except NameError:
                return "Ошибка чтения из БД"

            if synonyms is None:
                return "Такого слова нет"

            if not main_word_id:
                synonyms += SynonymousWords.query.filter(SynonymousWords.synonym_id == word_id).all()

            word = synonyms[0].word
            try:
                for synonym in synonyms:
                    db.session.delete(synonym)
                db.session.commit()
                if len(synonyms) > 1:
                    flash(Markup("<strong>Удалено слово:</strong> " + word
                                 + " <strong>и все слова синонимичные ему</strong>"), category='success')
                else:
                    flash(Markup("<strong>Удалено слово:</strong> " + word), category='success')
            except exc.SQLAlchemyError:
                flash('Ошибка внесения изменений в базу данных', category='danger')
        if main_word_id:
            return redirect(url_for('.synonyms_replacement', word_id=main_word_id))
        return redirect(url_for('.synonyms'))
