from flask import render_template
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from admin import forms
from models import Users


class ViewUser(FlaskView):
    route_base = '/'

    @route('/users')
    @login_required
    def users(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')
        add_user_form = forms.AddUserForm()
        edit_user_form = forms.EditUserForm()
        deactivate_user_form = forms.DeactivateUserForm()
        change_password_user_form = forms.ChangePasswordUserForm()
        try:
            users = Users.query.filter(Users.is_deactivated.is_(False))
        except (NameError, AttributeError):
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")
        return render_template('admin/users.html', users=users, add_user_form=add_user_form,
                               edit_user_form=edit_user_form,
                               deactivate_user_form=deactivate_user_form,
                               change_password_user_form=change_password_user_form)

    @route('/users/deactivate')
    @login_required
    def users_deactivate(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')

        activate_user_form = forms.ActivateUserForm()
        delete_user_form = forms.DeleteUserForm()
        try:
            users = Users.query.filter(Users.is_deactivated)
        except (NameError, AttributeError):
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")
        return render_template('admin/users_deactivate.html', activate_user_form=activate_user_form,
                               delete_user_form=delete_user_form, users=users)

    @route('/users/rights')
    @login_required
    def users_rights(self):
        if not current_user.right_users:
            return render_template('admin/access_denied.html')
        edit_user_rights_form = forms.EditUserRightsForm()
        try:
            users = Users.query
        except NameError:
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")
        return render_template('admin/users_rights.html', users=users, edit_user_rights_form=edit_user_rights_form)
