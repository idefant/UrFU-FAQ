from flask import request, flash, url_for, render_template
from flask_classy import FlaskView, route
from flask_login import login_required
from markupsafe import Markup
from sqlalchemy import exc
from werkzeug.utils import redirect

from models import db, SynonymousWords
from admin.forms import AddSynonymsDependentForm, EditSynonymsDependentForm, DeleteSynonymsDependentForm


class FormHandlerSynonym(FlaskView):
    route_base = '/'

    @route('/add_synonym', methods=["POST"])
    @login_required
    def add_synonym(self):
        add_synonyms_dependent_form = AddSynonymsDependentForm()
        main_word_id = request.args.get("word_id")
        if not add_synonyms_dependent_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            word = add_synonyms_dependent_form.word.data.lower()
            word = " ".join(word.split())

            if not word:
                flash('Неправильно заполнены поля', category='danger')
            else:
                if main_word_id:
                    main_word = SynonymousWords.query.get(main_word_id)
                    if main_word.synonym_id:
                        flash('Главный синоним не должен сам быть чьим-то синонимом. Фильтры сброшены',
                              category='danger')
                        return redirect(url_for('.ViewTechSetting:synonyms'))
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
            return redirect(url_for('.ViewTechSetting:synonyms_replacement', word_id=main_word_id))
        return redirect(url_for('.ViewTechSetting:synonyms'))

    @route('/edit_synonym', methods=["POST"])
    @login_required
    def edit_synonym(self):
        edit_synonyms_dependent_form = EditSynonymsDependentForm()
        main_word_id = request.args.get("word_id")
        if not edit_synonyms_dependent_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            word_id = edit_synonyms_dependent_form.word_id.data
            word = edit_synonyms_dependent_form.word.data.lower()
            word = " ".join(word.split())
            if not word:
                flash('Неправильно заполнены поля', category='danger')
            else:
                try:
                    synonym = SynonymousWords.query.get(word_id)
                except NameError:
                    return render_template("admin/error_page.html", message="Ошибка чтения из БД")

                if synonym is None:
                    flash('Нет такого слова', category='danger')
                else:
                    synonym.word = word
                    try:
                        db.session.commit()
                        flash(Markup("<strong>Изменено слово:</strong> " + word), category='success')
                    except exc.SQLAlchemyError:
                        flash('Ошибка внесения изменений в базу данных', category='danger')
        if main_word_id:
            return redirect(url_for('.ViewTechSetting:synonyms_replacement', word_id=main_word_id))
        return redirect(url_for('.ViewTechSetting:synonyms'))

    @route('/delete_synonym', methods=["POST"])
    @login_required
    def delete_synonym(self):
        delete_synonyms_dependent_form = DeleteSynonymsDependentForm()
        main_word_id = request.args.get("word_id")
        if not delete_synonyms_dependent_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            word_id = delete_synonyms_dependent_form.word_id.data

            if word_id == main_word_id:
                flash('Нельзя удалять главный синоним', category='danger')
            else:
                try:
                    synonyms = SynonymousWords.query
                except NameError:
                    return render_template("admin/error_page.html", message="Ошибка чтения из БД")

                synonyms_this_word = [synonyms.get(word_id)]

                if synonyms_this_word is None:
                    flash('Такого слова нет', category='danger')
                else:
                    if not main_word_id:
                        synonyms_this_word += synonyms.filter(SynonymousWords.synonym_id == word_id)

                    word = synonyms_this_word[0].word
                    try:
                        for synonyms in synonyms_this_word:
                            db.session.delete(synonyms)
                        db.session.commit()
                        if len(synonyms_this_word) > 1:
                            flash(Markup("<strong>Удалено слово:</strong> " + word
                                         + " <strong>и все слова синонимичные ему</strong>"), category='success')
                        else:
                            flash(Markup("<strong>Удалено слово:</strong> " + word), category='success')
                    except exc.SQLAlchemyError:
                        flash('Ошибка внесения изменений в базу данных', category='danger')
        if main_word_id:
            return redirect(url_for('.ViewTechSetting:synonyms_replacement', word_id=main_word_id))
        return redirect(url_for('.ViewTechSetting:synonyms'))
