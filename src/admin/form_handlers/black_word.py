from flask import request, flash, url_for, render_template
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from markupsafe import Markup
from werkzeug.utils import redirect

from dbase import db, BlackWords
from forms import AddBlackWordForm, EditBlackWordForm, DeleteBlackWordForm


class FormHandlerBlackWord(FlaskView):
    route_base = '/'

    @route('/add_black_word', methods=["POST"])
    @login_required
    def add_black_word(self):
        if (not current_user.right_black_word):
            return render_template('admin/access_denied.html')
        addBlackWordForm = AddBlackWordForm()
        if addBlackWordForm.validate_on_submit():
            word = addBlackWordForm.word.data
            black_word = BlackWords(word=word)

            try:
                db.session.add(black_word)
                db.session.commit()
                flash(Markup("<strong>Добавлено слово:</strong> " + word), category='success')
            except:
                flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.black_words'))

    @route('/edit_black_word', methods=["POST"])
    @login_required
    def edit_black_word(self):
        if (not current_user.right_black_word):
            return render_template('admin/access_denied.html')
        editBlackWordForm = EditBlackWordForm()
        if editBlackWordForm.validate_on_submit():
            id = editBlackWordForm.id.data
            word = editBlackWordForm.word.data

            black_word = BlackWords.query.get(id)
            black_word.word = word
            try:
                db.session.commit()
                flash(Markup("<strong>Изменено слово:</strong> " + word), category='success')
            except:
                flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.black_words'))

    @route('/delete_black_word', methods=["POST"])
    @login_required
    def delete_black_word(self):
        if (not current_user.right_black_word):
            return render_template('admin/access_denied.html')
        deleteBlackWordForm = DeleteBlackWordForm()
        if deleteBlackWordForm.validate_on_submit():
            id = deleteBlackWordForm.id.data
            black_word = BlackWords.query.get(id)
            word = black_word.word
            try:
                db.session.delete(black_word)
                db.session.commit()
                flash(Markup("<strong>Удалено слово:</strong> " + word), category='success')
            except:
                flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.black_words'))