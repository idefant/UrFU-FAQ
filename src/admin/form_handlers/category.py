from flask import flash, url_for, request, render_template, redirect
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from markupsafe import Markup
from sqlalchemy import exc

from models import db, Categories
from forms import AddCategoryForm, EditCategoryForm, DeleteCategoryForm


class FormHandlerCategory(FlaskView):
    route_base = '/'

    @route('/add_category', methods=["POST"])
    @login_required
    def add_category(self):
        if not current_user.right_category:
            return render_template('admin/access_denied.html')
        add_category_form = AddCategoryForm()
        if add_category_form.validate_on_submit():
            try:
                categories_count = Categories.query.count()
            except NameError:
                return "Ошибка чтения из БД"

            name = add_category_form.category.data
            icon_name = add_category_form.icon_name.data

            if not name:
                flash('Неправильно заполнены поля', category='danger')
            else:
                category = Categories(name=name, priority=categories_count, icon_name=icon_name)
                try:
                    db.session.add(category)
                    db.session.commit()
                    flash(Markup("<strong>Добавлена категория:</strong> " + name), category='success')
                    flash(Markup("<strong>Необходимо добавить цвет к категории:</strong> " + name), category='danger')
                except exc.SQLAlchemyError:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.category'))

    @route('/edit_category', methods=["POST"])
    @login_required
    def edit_category(self):
        if not current_user.right_category:
            return render_template('admin/access_denied.html')
        edit_category_form = EditCategoryForm()
        if edit_category_form.validate_on_submit():
            cat_id = edit_category_form.id.data
            name = edit_category_form.name.data
            icon_name = edit_category_form.icon_name.data

            if not name:
                flash('Неправильно заполнены поля', category='danger')
            else:
                try:
                    category = Categories.query.get(cat_id)
                except NameError:
                    return "Ошибка чтения из БД"

                if category is None:
                    return "Категории не существует"
                category.name = name
                category.icon_name = icon_name
                try:
                    db.session.commit()
                    flash(Markup("<strong>Изменен вопрос:</strong> " + name), category='success')
                except exc.SQLAlchemyError:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.category'))

    @route('/delete_category', methods=["POST"])
    @login_required
    def delete_category(self):
        if not current_user.right_category:
            return render_template('admin/access_denied.html')
        delete_category_form = DeleteCategoryForm()
        if delete_category_form.validate_on_submit():
            cat_id = delete_category_form.id.data
            count_qa = delete_category_form.count_qa.data
            try:
                cat_id = int(cat_id)
                count_qa = int(count_qa)
            except ValueError:
                return "Категория и количество записей должно быть представлено в виде чисел"
            if cat_id == 0:
                flash('Нельзя удалять категорию "Популярное"', category='danger')
            elif count_qa != 0:
                flash('Нельзя удалять категорию в которой есть вопросы. Переместите их в другую категорию или удалите',
                      category='danger')
            else:
                try:
                    category = Categories.query.get(cat_id)
                except NameError:
                    return "Ошибка чтения из БД"
                name = category.name
                try:
                    db.session.delete(category)
                    db.session.commit()
                    flash(Markup("<strong>Удалена категория:</strong> " + name), category='success')
                except exc.SQLAlchemyError:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.category'))

    @route('/change_color', methods=["POST", "GET"])
    @login_required
    def change_color(self):
        if not current_user.right_category:
            return render_template('admin/access_denied.html')
        color = request.args.get("color")
        cat_id = request.args.get("cat_id")
        try:
            category = Categories.query.get(cat_id)
        except NameError:
            return "Ошибка чтения из БД"
        if category is None:
            return "Категории не существует"
        category.color = color

        try:
            db.session.commit()
            flash("Цвет категории успешно изменен", category='success')
        except exc.SQLAlchemyError:
            flash('Ошибка внесения изменений в базу данных', category='danger')

        return redirect(url_for('.category'))

    @route('/change_order_category', methods=['GET', 'POST'])
    def change_order_category(self):
        if not current_user.right_category:
            return render_template('admin/access_denied.html')
        sequence_id = request.args.get("sequence_id")
        sequence_id = sequence_id.split(",")
        try:
            categories_list = Categories.query
        except NameError:
            return "Ошибка чтения из БД"

        for i in range(len(sequence_id)):
            categories_list.get(int(sequence_id[i])).priority = i + 1

        try:
            db.session.commit()
            flash('Порядок сортировки категорий успешно обновлен', category='success')
        except exc.SQLAlchemyError:
            flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.category_sort'))
