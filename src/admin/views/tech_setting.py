from flask import render_template, url_for, request
from flask_classy import FlaskView, route
from flask_login import login_required, current_user

import forms
from models import BlackWords, WhiteWords, SynonymousWords


class ViewTechSetting(FlaskView):
    route_base = '/'

    @route('/black_words')
    @login_required
    def black_words(self):
        if not current_user.right_exception_word:
            return render_template('admin/access_denied.html')
        add_exception_word_form = forms.AddExceptionWordForm()
        edit_exception_word_form = forms.EditExceptionWordForm()
        delete_exception_word_form = forms.DeleteExceptionWordForm()
        try:
            black_words = BlackWords.query
        except NameError:
            return "Ошибка чтения из БД"
        return render_template('admin/exception_words.html', add_exception_word_form=add_exception_word_form,
                               edit_exception_word_form=edit_exception_word_form,
                               delete_exception_word_form=delete_exception_word_form,
                               black_words=black_words, word_type="black")

    @route('/white_words')
    @login_required
    def white_words(self):
        if not current_user.right_exception_word:
            return render_template('admin/access_denied.html')
        add_exception_word_form = forms.AddExceptionWordForm()
        edit_exception_word_form = forms.EditExceptionWordForm()
        delete_exception_word_form = forms.DeleteExceptionWordForm()
        try:
            black_words = WhiteWords.query
        except NameError:
            return "Ошибка чтения из БД"
        return render_template('admin/exception_words.html', add_exception_word_form=add_exception_word_form,
                               edit_exception_word_form=edit_exception_word_form,
                               delete_exception_word_form=delete_exception_word_form,
                               black_words=black_words, word_type="white")

    @route('/synonyms')
    @login_required
    def synonyms(self):
        if not current_user.right_synonym:
            return render_template('admin/access_denied.html')
        add_synonyms_dependent_form = forms.AddSynonymsDependentForm()
        edit_synonyms_dependent_form = forms.EditSynonymsDependentForm()
        delete_synonyms_dependent_form = forms.DeleteSynonymsDependentForm()
        try:
            synonyms = SynonymousWords.query
        except NameError:
            return "Ошибка чтения из БД"
        main_words = synonyms.filter(SynonymousWords.synonym_id.is_(None))
        main_dependent_words = []
        for main_word in main_words:
            dependent_words = synonyms.filter(main_word.id == SynonymousWords.synonym_id)
            main_dependent_words += [(main_word, dependent_words)]

        return render_template('admin/synonyms.html', add_synonyms_dependent_form=add_synonyms_dependent_form,
                               edit_synonyms_dependent_form=edit_synonyms_dependent_form,
                               delete_synonyms_dependent_form=delete_synonyms_dependent_form,
                               main_dependent_words=main_dependent_words, current_url=url_for('.ViewTechSetting:synonyms'))  # Зачем это здесь, почему не прописать юрл в html

    @route('/synonyms/replacement')
    @login_required
    def synonyms_replacement(self):
        if not current_user.right_synonym:
            return render_template('admin/access_denied.html')
        add_synonyms_dependent_form = forms.AddSynonymsDependentForm()
        edit_synonyms_dependent_form = forms.EditSynonymsDependentForm()
        delete_synonyms_dependent_form = forms.DeleteSynonymsDependentForm()

        main_word_id = request.args.get("word_id")
        if main_word_id is None:
            return "Слова синонима нет"
        else:
            try:
                main_word_id = int(main_word_id)
            except ValueError:
                return "ID слова должен быть числом"

            try:
                synonyms = SynonymousWords.query
                main_word = synonyms.get(main_word_id)
                synonyms = synonyms.filter(SynonymousWords.synonym_id == main_word_id)
            except(NameError, AttributeError):
                return "Ошибка чтения из БД"

        return render_template('admin/synonyms_replacement.html',
                               add_synonyms_dependent_form=add_synonyms_dependent_form,
                               edit_synonyms_dependent_form=edit_synonyms_dependent_form,
                               delete_synonyms_dependent_form=delete_synonyms_dependent_form,
                               main_word=main_word, synonyms=synonyms, word_id=main_word_id)