from flask import flash, url_for, request, render_template, redirect
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from markupsafe import Markup
from sqlalchemy import exc

from models import db, Categories
from admin.forms import AddCategoryForm, EditCategoryForm, DeleteCategoryForm


class FormHandlerCategory(FlaskView):
    route_base = '/'

    @route('/add_category', methods=["POST"])
    @login_required
    def add_category(self):
        if not current_user.right_category:
            return render_template('admin/access_denied.html')
        add_category_form = AddCategoryForm()
        if not add_category_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            try:
                categories_count = Categories.query.count()
            except NameError:
                return render_template("admin/error_page.html", message="Ошибка чтения из БД")

            name = " ".join(add_category_form.category.data.split())
            icon_name = " ".join(add_category_form.icon_name.data.split())

            if not (name, icon_name):
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
        return redirect(url_for('.ViewCategory:category'))

    @route('/edit_category', methods=["POST"])
    @login_required
    def edit_category(self):
        if not current_user.right_category:
            return render_template('admin/access_denied.html')
        edit_category_form = EditCategoryForm()
        if not edit_category_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            cat_id = edit_category_form.id.data
            name = " ".join(edit_category_form.name.data.split())
            icon_name = " ".join(edit_category_form.icon_name.data.split())

            if not (name and cat_id):
                flash('Неправильно заполнены поля', category='danger')
            else:
                try:
                    category = Categories.query.get(cat_id)
                except NameError:
                    return render_template("admin/error_page.html", message="Ошибка чтения из БД")

                if category is None:
                    flash("Категории не существует", category='danger')
                else:
                    category.name = name
                    category.icon_name = icon_name
                    try:
                        db.session.commit()
                        flash(Markup("<strong>Изменен вопрос:</strong> " + name), category='success')
                    except exc.SQLAlchemyError:
                        flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.ViewCategory:category'))

    @route('/delete_category', methods=["POST"])
    @login_required
    def delete_category(self):
        if not current_user.right_category:
            return render_template('admin/access_denied.html')
        delete_category_form = DeleteCategoryForm()
        if not delete_category_form.validate_on_submit():
            flash('Заполнены не все поля', category='danger')
        else:
            cat_id = delete_category_form.id.data
            count_qa = delete_category_form.count_qa.data
            if not (count_qa and cat_id):
                flash('В форме не заполнены некоторые скрытые поля', category='danger')
            else:
                if not (cat_id.isdigit() and count_qa.isdigit()):
                    flash('Категория и количество записей должно быть представлено в виде чисел', category='danger')
                else:
                    cat_id = int(cat_id)

                    if cat_id == 0:
                        flash('Нельзя удалять категорию "Популярное"', category='danger')
                    elif int(count_qa) != 0:
                        flash('Нельзя удалять категорию в которой есть вопросы. Переместите их в другую категорию или'
                              'удалите', category='danger')
                    else:
                        try:
                            category = Categories.query.get(cat_id)
                        except NameError:
                            return render_template("admin/error_page.html", message="Ошибка чтения из БД")
                        name = category.name
                        try:
                            db.session.delete(category)
                            db.session.commit()
                            flash(Markup("<strong>Удалена категория:</strong> " + name), category='success')
                        except exc.SQLAlchemyError:
                            flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.ViewCategory:category'))

    @route('/change_color', methods=["POST", "GET"])
    @login_required
    def change_color(self):
        if not current_user.right_category:
            return render_template('admin/access_denied.html')
        color = request.args.get("color")
        cat_id = request.args.get("cat_id")
        if not (color and cat_id):
            flash('Невозможно распознать цвет или категорию', category='danger')
        try:
            category = Categories.query.get(cat_id)
        except NameError:
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")
        if category is None:
            flash('Категории не существует. Цвет не был изменен', category='danger')
        else:
            category.color = color
            try:
                db.session.commit()
                flash("Цвет категории успешно изменен", category='success')
            except exc.SQLAlchemyError:
                flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.ViewCategory:category'))

    @route('/change_order_category', methods=['GET', 'POST'])
    def change_order_category(self):
        if not current_user.right_category:
            return render_template('admin/access_denied.html')
        sequence_id = request.args.get("sequence_id")
        if not sequence_id:
            flash('Последовательность элементов не была обнаружена. Порядок сортировки не был сохранен',
                  category='danger')
        list_sequence_id = sequence_id.split(",")
        try:
            categories = Categories.query
        except NameError:
            return render_template("admin/error_page.html", message="Ошибка чтения из БД")

        for i in range(len(list_sequence_id)):
            if not list_sequence_id[i].isdigit():
                flash('Последовательность элементов должна из себя представлять список чисел', category='danger')
                return redirect(url_for('.ViewCategory:category_sort'))
            else:
                categories.get(int(list_sequence_id[i])).priority = i + 1

        try:
            db.session.commit()
            flash('Порядок сортировки категорий успешно обновлен', category='success')
        except exc.SQLAlchemyError:
            flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.ViewCategory:category_sort'))
