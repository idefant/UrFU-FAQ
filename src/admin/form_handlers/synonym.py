from flask import request, flash, url_for, render_template
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from markupsafe import Markup
from werkzeug.utils import redirect

from dbase import db, SynonymousWords
from forms import AddSynonymsDependentForm, EditSynonymsDependentForm, DeleteSynonymsDependentForm


class FormHandlerSynonym(FlaskView):
    route_base = '/'

    @route('/add_synonym', methods=["POST"])
    @login_required
    def add_synonym(self):
        addSynonymsDependentForm = AddSynonymsDependentForm()
        main_word_id = request.args.get("word_id")
        if addSynonymsDependentForm.validate_on_submit():
            word = addSynonymsDependentForm.word.data
            if main_word_id:
                synonym = SynonymousWords(word=word, synonym_id=main_word_id)
            else:
                synonym = SynonymousWords(word=word)
            try:
                db.session.add(synonym)
                db.session.commit()
                flash(Markup("<strong>Добавлено слово:</strong> " + word), category='success')
            except:
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

            synonym = SynonymousWords.query.get(word_id)
            synonym.word = word
            try:
                db.session.commit()
                flash(Markup("<strong>Изменено слово:</strong> " + word), category='success')
            except:
                flash('Ошибка внесения изменений в базу данных', category='danger')
        if main_word_id:
            return redirect(url_for('.synonyms_replacement', word_id=main_word_id))
        return redirect(url_for('.synonyms'))


    @route('/delete_synonym', methods=["POST"])
    @login_required
    def delete_synonym(self):
        deleteSynonymsDependentForm = DeleteSynonymsDependentForm()
        main_word_id = request.args.get("word_id")
        if deleteSynonymsDependentForm.validate_on_submit():
            word_id = deleteSynonymsDependentForm.word_id.data
            synonym = SynonymousWords.query.get(word_id)
            word = synonym.word
            try:
                db.session.delete(synonym)
                db.session.commit()
                flash(Markup("<strong>Удалено слово:</strong> " + word), category='success')
            except:
                flash('Ошибка внесения изменений в базу данных', category='danger')
        if main_word_id:
            return redirect(url_for('.synonyms_replacement', word_id=main_word_id))
        return redirect(url_for('.synonyms'))