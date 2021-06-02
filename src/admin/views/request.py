import math

from flask import render_template, request, send_file, flash
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from six import BytesIO
from sqlalchemy import desc
from werkzeug.utils import redirect

from models import Questions, Requests, db
from search import convert_text


class ViewRequest(FlaskView):
    route_base = '/'

    @route('/requests')
    @login_required
    def requests(self):
        if not current_user.right_request:
            return render_template('admin/access_denied.html')
        requests_page_count = 5
        page_data = request.args.get("page")
        if page_data == None:
            page = 1
        else:
            page = int(page_data)
        requests = Requests.query
        requests_count = requests.count()
        requests = requests.order_by(desc(Requests.id)).paginate(page, requests_page_count, False).items

        if page - 5 > 0:
            first_pages = list(range(page - 5, page))
        else:
            first_pages = list(range(1, page))

        if page + 5 < math.ceil(requests_count / requests_page_count):
            last_pages = list(range(page + 1, page + 6))
        else:
            last_pages = list(range(page + 1, math.ceil(requests_count / requests_page_count) + 1))

        return render_template('admin/requests.html', requests=requests, current_page=page, first_pages=first_pages,
                               last_pages=last_pages)

    @route('/requests_history.txt')
    def requests_history(self):
        if not current_user.right_request:
            return render_template('admin/access_denied.html')
        requests = Requests.query.order_by(desc(Requests.id))
        output = "Тут какая-то инструкция" + "\n\n"
        for request in requests:
            output += "_" * 100 + "\n\n"
            output += request.original + "\n\n"
            output += request.cleared + "\n\n"
            output += str(request.date_time.strftime("%d.%m.%Y  %H:%M:%S")) + "\n"

        return send_file(BytesIO(bytes(output.encode())), as_attachment=True,
                         attachment_filename='requests_history.txt', mimetype='text/plain')

    @route('/update_cleared_questions_dbase')
    def update_cleared_questions_dbase(self):
        qa_list = Questions.query
        next_to_data = request.args.get("next_to")
        for qa in qa_list:
            qa.clear_question = convert_text(qa.question)
        try:
            db.session.commit()
            flash("Очистка вопросов прошла успешно", category='success')
        except:
            flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(next_to_data)