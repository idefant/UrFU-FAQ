from flask import Blueprint, render_template, flash, url_for, redirect, session
from flask_login import login_required, logout_user, current_user

from config import bot_link
from models import Users, Questions, Categories
from search import parse_table
from .functions import get_categories_id_count

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

from .form_handlers.user import FormHandlerUser
from .form_handlers.account import FormHandlerAccount
from .form_handlers.category import FormHandlerCategory
from .form_handlers.qa import FormHandlerQA
from .form_handlers.synonym import FormHandlerSynonym
from .form_handlers.login import FormHandlerLogin
from .form_handlers.exception_word import FormHandlerExceptionWord

FormHandlerQA.register(admin)
FormHandlerCategory.register(admin)
FormHandlerAccount.register(admin)
FormHandlerUser.register(admin)
FormHandlerExceptionWord.register(admin)
FormHandlerSynonym.register(admin)
FormHandlerLogin.register(admin)

from .views.qa import ViewQA
from .views.category import ViewCategory
from .views.user import ViewUser
from .views.tech_setting import ViewTechSetting
from .views.request import ViewRequest
from .views.account import ViewAccount

ViewQA.register(admin)
ViewCategory.register(admin)
ViewUser.register(admin)
ViewTechSetting.register(admin)
ViewRequest.register(admin)
ViewAccount.register(admin)


@admin.route('/')
@login_required
def index():

    # parse_table() # Это убрать


    try:
        categories = Categories.query
        questions = Questions.query
        users_count = Users.query.count()
    except (NameError):
        return render_template("admin/error_page.html", message="Ошибка чтения из БД")

    categories_count = categories.count()
    questions_count = questions.count()
    categories_id_count = get_categories_id_count(categories_count, questions)

    categories_questions_count = []
    for category in categories:
        categories_questions_count += [(category, categories_id_count[category.id])]
    return render_template("admin/dashboard.html", categories_count=categories_count, users_count=users_count,
                           categories_questions_count=categories_questions_count, questions_count=questions_count,
                           bot_link=bot_link)


@admin.before_request
def before_request():
    session.permanent = True
    if current_user.is_authenticated:
        if 'auth_token' not in session or format(session.get('auth_token')) != current_user.auth_token:
            logout_user()
            flash("Для продолжения авторизуйтесь", category='danger')
            return redirect(url_for('.ViewAccount:login'))

        if current_user.is_deactivated:
            logout_user()
            flash("Ваш аккаунт заблокирован. Для получения дополнительных сведений обратитесь к администратору",
                  category='danger')
            return redirect(url_for('.ViewAccount:login'))
