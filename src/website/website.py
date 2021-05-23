from flask import Blueprint, render_template

from dbase import db, Categories, Questions

website = Blueprint('website', __name__, template_folder='templates', static_folder='static', static_url_path='website')


@website.route('/')
def index():
    categories_list = db.session.query(Categories)
    popular_qa_list = db.session.query(Questions).filter(Questions.is_popular).order_by(Questions.popular_priority)
    result_list = []
    num = 0

      # (Категория популярного, [qa, icon])
    popular_qa_list_assembly = []
    for popular_qa in popular_qa_list:
        category = categories_list.get(popular_qa.cat_id)
        if category != None:
            icon_name = category.icon_name
            popular_qa_list_assembly += [(popular_qa, icon_name)]

    result_popular_list = (categories_list[0], popular_qa_list_assembly)

    categories_list = categories_list.order_by(Categories.priority)
    for category in reversed(categories_list.offset(1).all()):
        qa_list = db.session.query(Questions).filter(Questions.cat_id == category.id).order_by(Questions.priority).all()
        result_list += [(num, category, qa_list)]
        num = num + 1
    return render_template('website/index.html', result_list=result_list, result_popular_list=result_popular_list)