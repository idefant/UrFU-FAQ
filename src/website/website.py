from flask import Blueprint, render_template
from models import Categories, Questions

website = Blueprint('website', __name__, template_folder='templates', static_folder='static', static_url_path='website')


@website.route('/')
def index():
    try:
        categories = Categories.query
        questions = Questions.query
    except NameError:
        return "Ошибка чтения из БД"

    result_list = []
    num = 0

    popular_qa_list_assembly = []
    for popular_qa in questions.filter(Questions.is_popular).order_by(Questions.popular_priority):
        category = categories.get(popular_qa.cat_id)
        if category is not None:
            popular_qa_list_assembly += [(popular_qa, category.icon_name)]

    result_popular_list = (categories.get(0), popular_qa_list_assembly)

    for category in reversed(categories.filter(Categories.id != 0).order_by(Categories.priority).all()):
        qa_list = questions.filter(Questions.cat_id == category.id).order_by(Questions.priority)
        result_list += [(num, category, qa_list)]
        num = num + 1
    return render_template('website/index.html', result_list=result_list, result_popular_list=result_popular_list)
