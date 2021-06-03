from flask import Blueprint, render_template
from models import Categories, Questions

website = Blueprint('website', __name__, template_folder='templates', static_folder='static', static_url_path='website')


@website.route('/')
def index():
    try:
        categories = Categories.query
        questions = Questions.query
        popular_questions = questions.filter(Questions.is_popular).order_by(Questions.popular_priority)
    except NameError:
        return render_template("admin/error_page.html", message="Ошибка чтения из БД")

    popular_qa_list_assembly = []
    for popular_question in popular_questions:
        category = categories.get(popular_question.cat_id)
        if category is not None:
            popular_qa_list_assembly += [(popular_question, category.icon_name)]

    result_popular_list = (categories.get(0), popular_qa_list_assembly)

    result_list = []
    num = 0

    for category in reversed(categories.filter(Categories.id != 0).order_by(Categories.priority).all()):
        try:
            usually_questions = questions.filter(Questions.cat_id == category.id).order_by(Questions.priority)
        except (NameError, AttributeError):
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")
        result_list += [(num, category, usually_questions)]
        num = num + 1
    return render_template('website/index.html', result_list=result_list, result_popular_list=result_popular_list)
