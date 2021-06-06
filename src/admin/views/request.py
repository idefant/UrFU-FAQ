import math
from flask import render_template, request, send_file, flash, url_for
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from six import BytesIO
from sqlalchemy import desc
from werkzeug.utils import redirect
from models import Questions, Requests, db
from search import convert_text
from sqlalchemy import exc


class ViewRequest(FlaskView):
    route_base = '/'

    @route('/requests')
    @login_required
    def requests(self):
        if not current_user.right_request:
            return render_template('admin/access_denied.html')
        requests_page_count = 300
        page_data = request.args.get("page")
        if page_data is None:
            page = 1
        else:
            if not page_data.isdigit():
                flash('ID категории должен быть числом. Номер страницы сброшен', category='danger')
                return redirect(url_for('.ViewRequest:requests'))
            else:
                page = int(page_data)
        try:
            requests = Requests.query
            requests_count = requests.count()
            requests = requests.order_by(desc(Requests.id)).paginate(page, requests_page_count, False).items
        except (NameError, AttributeError):
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")

        if math.ceil(requests_count / requests_page_count) < page or page == 0:
            flash('Нет такой страницы. Номер страницы был сброшен', category='danger')
            return redirect(url_for('.ViewRequest:requests'))

        if page - requests_page_count > 0:
            first_pages = list(range(page - requests_page_count, page))
        else:
            first_pages = list(range(1, page))

        if page + requests_page_count < math.ceil(requests_count / requests_page_count):
            last_pages = list(range(page + 1, page + requests_page_count + 1))
        else:
            last_pages = list(range(page + 1, math.ceil(requests_count / requests_page_count) + 1))

        return render_template('admin/requests.html', requests=requests, current_page=page, first_pages=first_pages,
                               last_pages=last_pages)

    @route('/requests_history.txt')
    def requests_history(self):
        if not current_user.right_request:
            return render_template('admin/access_denied.html')
        try:
            requests = Requests.query.order_by(desc(Requests.id))
        except (NameError, AttributeError):
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")
        output = "База пользовательских запросов представляет из себя список состоящий из запроса, очишенного " \
                 "запроса, даты/времени сообщения. Элементы списка отделены друг от друга горизонтальной чертой \n\n"
        for request_elem in requests:
            output += "-" * 100 + "\n"
            output += request_elem.original + "\n\n"
            output += request_elem.cleared + "\n\n"
            output += str(request_elem.date_time.strftime("%d.%m.%Y  %H:%M:%S")) + "\n"

        return send_file(BytesIO(bytes(output.encode())), as_attachment=True,
                         attachment_filename='requests_history.txt', mimetype='text/plain')

    @route('/update_cleared_questions_dbase')
    def update_cleared_questions_dbase(self):
        try:
            questions = Questions.query
        except NameError:
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")
        next_to_data = request.args.get("next_to")
        if next_to_data is None:
            flash('Не найден адрес предыдущей страницы', category='danger')
            return redirect(url_for('.index'))
        for qa in questions:
            qa.clear_question = convert_text(qa.question)
        try:
            db.session.commit()
            flash("Очистка вопросов прошла успешно", category='success')
        except exc.SQLAlchemyError:
            flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(next_to_data)
