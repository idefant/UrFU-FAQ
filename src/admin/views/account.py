import math

from flask import render_template, request, send_file, flash, url_for
from flask_classy import FlaskView, route
from flask_login import login_required, current_user, logout_user
from six import BytesIO
from sqlalchemy import desc
from werkzeug.utils import redirect

import forms
from models import Questions, Requests, db
from search import convert_text


class ViewAccount(FlaskView):
    route_base = '/'

    @route('/logout')
    @login_required
    def logout(self):
        logout_user()
        flash("Вы совершили выход из админ-панели", category='danger')
        return redirect(url_for('.ViewAccount:login'))

    @route('/login', methods=['post', 'get'])
    def login(self):
        if current_user.is_authenticated:
            return redirect(url_for('.ViewAccount:account'))
        login_form = forms.LoginForm()

        return render_template('admin/login.html', login_form=login_form)

    @route('/account')
    @login_required
    def account(self):
        edit_account_form = forms.EditAccountForm()
        change_password_account_form = forms.ChangePasswordAccountForm()
        edit_account_form.username.default = current_user.username
        edit_account_form.name.default = current_user.name
        edit_account_form.process()
        return render_template('admin/account.html', edit_account_form=edit_account_form,
                               change_password_account_form=change_password_account_form, current_user=current_user)