from flask import render_template, url_for, request, flash
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from admin import forms
from models import SynonymousWords


class ViewSynonym(FlaskView):
    route_base = '/'

    @route('/synonyms')
    @login_required
    def synonyms(self):
        if not current_user.right_synonym:
            return render_template('admin/access_denied.html')
        add_synonyms_dependent_form = forms.AddSynonymsDependentForm()
        edit_synonyms_dependent_form = forms.EditSynonymsDependentForm()
        delete_synonyms_dependent_form = forms.DeleteSynonymsDependentForm()

        main_dependent_words = []
        try:
            synonyms = SynonymousWords.query
            main_words = synonyms.filter(SynonymousWords.synonym_id.is_(None)).order_by(SynonymousWords.word)
            for main_word in main_words:
                dependent_words = synonyms.filter(main_word.id == SynonymousWords.synonym_id)
                main_dependent_words += [(main_word, dependent_words)]
        except (NameError, AttributeError):
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")

        return render_template('admin/synonyms.html', add_synonyms_dependent_form=add_synonyms_dependent_form,
                               edit_synonyms_dependent_form=edit_synonyms_dependent_form,
                               delete_synonyms_dependent_form=delete_synonyms_dependent_form,
                               main_dependent_words=main_dependent_words)

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
            flash('Не задан ID слова', category='danger')
            return redirect(url_for('.ViewSynonym:synonyms'))
        else:
            if not main_word_id.isdigit():
                flash('ID слова должен быть числом', category='danger')
                return redirect(url_for('.ViewSynonym:synonyms'))
            else:
                main_word_id = int(main_word_id)

                try:
                    synonyms = SynonymousWords.query
                    main_word = synonyms.get(main_word_id)
                    synonyms = synonyms.filter(SynonymousWords.synonym_id == main_word_id)\
                        .order_by(SynonymousWords.word)
                except(NameError, AttributeError):
                    return render_template("admin/error_page.html", message="Ошибка чтения из БД")
                if main_word is None:
                    flash('Нет слова с таким ID', category='danger')
                    return redirect(url_for('.ViewSynonym:synonyms'))
                if main_word.synonym_id is not None:
                    flash('Слово, которое уже является синонимичным к какому-либо слову, не может иметь синонимов',
                          category='danger')
                    return redirect(url_for('.ViewSynonym:synonyms'))

        return render_template('admin/synonyms_replacement.html',
                               add_synonyms_dependent_form=add_synonyms_dependent_form,
                               edit_synonyms_dependent_form=edit_synonyms_dependent_form,
                               delete_synonyms_dependent_form=delete_synonyms_dependent_form,
                               main_word=main_word, synonyms=synonyms, word_id=main_word_id)
