from flask import render_template
from flask_classy import FlaskView, route
from flask_login import login_required, current_user

from admin import forms
from models import BlackWords, WhiteWords


class ViewExceptionWord(FlaskView):
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
            black_words = BlackWords.query.order_by(BlackWords.word)
        except (NameError, AttributeError):
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")
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
            white_words = WhiteWords.query.order_by(WhiteWords.word)
        except (NameError, AttributeError):
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")
        return render_template('admin/exception_words.html', add_exception_word_form=add_exception_word_form,
                               edit_exception_word_form=edit_exception_word_form,
                               delete_exception_word_form=delete_exception_word_form,
                               black_words=white_words, word_type="white")
