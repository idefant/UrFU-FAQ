from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_required, logout_user, current_user
from sqlalchemy import desc

from search import update_cleared_questions_dbase
from .form_handlers.black_word import FormHandlerBlackWord
from dbase import db, Users, Questions, Categories, BlackWords, SynonymousWords
import forms
from .form_handlers.user import FormHandlerUser
from .form_handlers.account import FormHandlerAccount
from .form_handlers.category import FormHandlerCategory
from .form_handlers.qa import FormHandlerQA
from .form_handlers.synonym import FormHandlerSynonym
from .form_handlers.login import FormHandlerLogin

from . import functions

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


FormHandlerQA.register(admin)
FormHandlerCategory.register(admin)
FormHandlerAccount.register(admin)
FormHandlerUser.register(admin)
FormHandlerBlackWord.register(admin)
FormHandlerSynonym.register(admin)
FormHandlerLogin.register(admin)


@admin.route('/')
@login_required
def index():
    try:
        categories = Categories.query
        questions = Questions.query
        users_count = Users.query.count()
    except (NameError, AttributeError):
        return "Ошибка чтения из БД"
    categories_count = categories.count()
    questions_count = questions.count()

    categories_id_count = functions.get_categories_id_count(categories_count, questions)

    categories_questions_count = []
    for category in categories:
        categories_questions_count += [(category, categories_id_count[category.id])]
    return render_template("admin/dashboard.html", categories_count=categories_count, users_count=users_count,
                           categories_questions_count=categories_questions_count, questions_count=questions_count)


@admin.route('/category')
@login_required
def category():
    if not current_user.right_category:
        return render_template('admin/access_denied.html')
    add_category_form = forms.AddCategoryForm()
    edit_category_form = forms.EditCategoryForm()
    delete_category_form = forms.DeleteCategoryForm()
    try:
        categories = Categories.query.order_by(Categories.priority)
        questions = Questions.query
    except (NameError, AttributeError):
        return "Ошибка чтения из БД"
    categories_id_count = functions.get_categories_id_count(categories.count(), questions)
    categories_questions_count = []
    for category in categories:
        categories_questions_count += [(category, categories_id_count[category.id])]
    return render_template("admin/category.html", add_category_form=add_category_form,
                           edit_category_form=edit_category_form, delete_category_form=delete_category_form,
                           categories_questions_count=categories_questions_count)


@admin.route('/category/sort')
@login_required
def category_sort():
    if not current_user.right_category:
        return render_template('admin/access_denied.html')
    try:
        categories = Categories.query.filter(Categories.id != 0).order_by(Categories.priority)
    except (NameError, AttributeError):
        return "Ошибка чтения из БД"
    return render_template("admin/category_sort.html", categories=categories)


@admin.route('/qa')
@login_required
def qa():
    if not current_user.right_qa:
        return render_template('admin/access_denied.html')
    cat_id_data = request.args.get("cat_id")
    popular_data = request.args.get("popular")
    add_qa_form = forms.AddQAForm()
    edit_qa_form = forms.EditQAForm()
    delete_qa_form = forms.DeleteQAForm()
    current_category = None

    try:
        categories = Categories.query
        categories_questions = db.session.query(Categories, Questions)\
            .join(Questions, Categories.id == Questions.cat_id)\
            .order_by(Questions.id)
    except (NameError, AttributeError):
        return "Ошибка чтения из БД"

    if cat_id_data is not None:
        try:
            cat_id_data = int(cat_id_data)
        except ValueError:
            return "ID категории должен быть числом"
        current_category = categories.get(cat_id_data)
        if current_category is None or cat_id_data == 0:
            return "Нет такой категории в БД"
        categories_questions = categories_questions.filter(Questions.cat_id == cat_id_data)
        add_qa_form.cat_id.default = cat_id_data

    if popular_data is not None:
        if popular_data == 'True':
            popular_data = True
        elif popular_data == 'False':
            popular_data = False
        categories_questions = categories_questions.filter(Questions.is_popular == popular_data)
        add_qa_form.popular.default = popular_data

    categories = categories.filter(Categories.id != 0)
    category_choices = [(0, "Выберете категорию")]
    category_choices += [(i.id, i.name) for i in categories]
    add_qa_form.cat_id.choices = category_choices
    edit_qa_form.cat_id.choices = category_choices
    add_qa_form.process()

    return render_template("admin/qa.html", add_qa_form=add_qa_form, edit_qa_form=edit_qa_form,
                           delete_qa_form=delete_qa_form, categories_questions=categories_questions,
                           categories=categories, cat_id_data=cat_id_data, popular_data=popular_data,
                           current_category=current_category)


@admin.route('/qa/sort')
@login_required
def qa_sort():
    if not current_user.right_qa:
        return render_template('admin/access_denied.html')
    questions = Questions.query
    message = ""
    cat_id_data = request.args.get("cat_id")

    try:
        categories = Categories.query
    except NameError:
        return "Ошибка чтения из БД"

    current_category = categories.get(cat_id_data)

    if cat_id_data is None:
        message = "Выбирите категорию из списка"
    elif cat_id_data == "popular":
        try:
            questions = questions.filter(Questions.is_popular).order_by(Questions.popular_priority)
        except (NameError, AttributeError):
            return "Ошибка чтения из БД"
    else:
        try:
            cat_id_data = int(cat_id_data)
        except ValueError:
            return "ID категории должен быть числом"

        if current_category is None or cat_id_data == 0:
            return "Нет такой категории в БД"

        try:
            questions = questions.filter(Questions.cat_id == cat_id_data).order_by(Questions.priority)
        except (NameError, AttributeError):
            return "Ошибка чтения из БД"

    categories = categories.filter(Categories.id != 0)

    return render_template("admin/qa_sort.html", questions=questions, categories=categories, message=message,
                           current_category=current_category, cat_id_data=cat_id_data)


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы совершили выход из админ-панели", category='danger')
    return redirect(url_for('.login'))


@admin.route('/login', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('.account'))
    login_form = forms.LoginForm()

    return render_template('admin/login.html', login_form=login_form)


@admin.route('/account')
@login_required
def account():
    edit_account_form = forms.EditAccountForm()
    change_password_account_form = forms.ChangePasswordAccountForm()
    edit_account_form.username.default = current_user.username
    edit_account_form.name.default = current_user.name
    edit_account_form.process()
    return render_template('admin/account.html', edit_account_form=edit_account_form,
                           change_password_account_form=change_password_account_form, current_user=current_user)


@admin.route('/users')
@login_required
def users():
    if not current_user.right_users:
        return render_template('admin/access_denied.html')
    add_user_form = forms.AddUserForm()
    edit_user_form = forms.EditUserForm()
    deactivate_user_form = forms.DeactivateUserForm()
    try:
        users = Users.query.filter(Users.is_deactivated.is_(False))
    except (NameError, AttributeError):
        return "Ошибка чтения из БД"
    return render_template('admin/users.html', users=users, add_user_form=add_user_form, edit_user_form=edit_user_form,
                           deactivate_user_form=deactivate_user_form)


@admin.route('/users/deactivate')
@login_required
def users_deactivate():
    if not current_user.right_users:
        return render_template('admin/access_denied.html')

    activate_user_form = forms.ActivateUserForm()
    delete_user_form = forms.DeleteUserForm()
    try:
        users = Users.query.filter(Users.is_deactivated)
    except (NameError, AttributeError):
        return "Ошибка чтения из БД"
    return render_template('admin/users_deactivate.html', activate_user_form=activate_user_form,
                           delete_user_form=delete_user_form, users=users)


@admin.route('/users/rights')
@login_required
def users_rights():
    if not current_user.right_users:
        return render_template('admin/access_denied.html')
    edit_user_rights_form = forms.EditUserRightsForm()
    try:
        users = Users.query
    except NameError:
        return "Ошибка чтения из БД"
    return render_template('admin/users_rights.html', users=users, edit_user_rights_form=edit_user_rights_form)


@admin.route('/colors')
@login_required
def colors():
    if not current_user.right_category:
        return render_template('admin/access_denied.html')
    cat_id_data = request.args.get("cat_id")

    qa_list = []
    is_popular_category = False

    questions = Questions.query

    try:
        categories_list = Categories.query.order_by(desc(Categories.priority))
    except (NameError, AttributeError):
        return "Ошибка чтения из БД"

    if cat_id_data is None:
        return "Категория не выбрана"
    elif cat_id_data == "popular":
        is_popular_category = True

        current_category = categories_list.get(0)
        if current_category is None:
            return "Нет такой категории в БД"
        index = categories_list.all().index(current_category)
        try:
            popular_qa_list = questions.filter(Questions.is_popular).order_by(Questions.popular_priority)
        except (NameError, AttributeError):
            return "Ошибка чтения из БД"

        for qa in popular_qa_list:
            category = categories_list.get(qa.cat_id)
            if category is not None:
                qa_list += [(qa, category.icon_name)]

    else:

        try:
            cat_id_data = int(cat_id_data)
        except ValueError:
            return "ID категории должен быть числом"
        current_category = categories_list.get(cat_id_data)
        if current_category is None:
            return "Нет такой категории в БД"
        index = categories_list.all().index(current_category)
        if (categories_list.get(cat_id_data) == None):
            return "Нет такой категории"
        try:
            qa_list = questions.filter(Questions.cat_id == cat_id_data).order_by(Questions.priority)
        except (NameError, AttributeError):
            return "Ошибка чтения из БД"

    return render_template('admin/color_picker.html', qa_list=qa_list, categories_list=categories_list,
                           current_category=current_category, index=index, is_popular_category=is_popular_category)


@admin.route('/cheat_sheet_icons')
@login_required
def cheat_sheet_icons():
    return render_template('admin/cheat_sheet_icons.html')


@admin.route('/black_words')
@login_required
def black_words():
    if not current_user.right_black_word:
        return render_template('admin/access_denied.html')
    add_black_word_form = forms.AddBlackWordForm()
    edit_black_word_form = forms.EditBlackWordForm()
    delete_black_word_form = forms.DeleteBlackWordForm()
    try:
        black_words = BlackWords.query
    except NameError:
        return "Ошибка чтения из БД"
    return render_template('admin/black_words.html', add_black_word_form=add_black_word_form,
                           edit_black_word_form=edit_black_word_form, delete_black_word_form=delete_black_word_form,
                           black_words=black_words)


@admin.route('/synonyms')
@login_required
def synonyms():
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
                           main_dependent_words=main_dependent_words)


@admin.route('/synonyms/replacement')
@login_required
def synonyms_replacement():
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

    return render_template('admin/synonyms_replacement.html', add_synonyms_dependent_form=add_synonyms_dependent_form,
                           edit_synonyms_dependent_form=edit_synonyms_dependent_form,
                           delete_synonyms_dependent_form=delete_synonyms_dependent_form,
                           main_word=main_word, synonyms=synonyms, word_id=main_word_id)


@admin.before_request
def before_request():
    if current_user.is_authenticated:
        if current_user.is_deactivated:
            logout_user()
            flash("Ваш аккаунт заблокирован. Для получения дополнительных сведений обратитесь к администратору",
                  category='danger')
            return redirect(url_for('.login'))
