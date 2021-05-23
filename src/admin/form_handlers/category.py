from flask import flash, url_for, request, render_template, redirect
from flask_classy import FlaskView, route
from flask_login import login_required, current_user
from markupsafe import Markup

from dbase import db, Categories
from forms import AddCategoryForm, EditCategoryForm, DeleteCategoryForm


class FormHandlerCategory(FlaskView):
    route_base = '/'

    @route('/add_category', methods=["POST"])
    @login_required
    def add_category(self):
        if (not current_user.right_category):
            return render_template('admin/access_denied.html')
        addCategoryForm = AddCategoryForm()
        if addCategoryForm.validate_on_submit():
            categories_count = db.session.query(Categories).count()
            name = addCategoryForm.category.data
            icon_name = addCategoryForm.icon_name.data

            if not name:
                flash('Неправильно заполнены поля', category='danger')
            else:
                category = Categories(name=name, priority=categories_count, icon_name=icon_name)
                try:
                    db.session.add(category)
                    db.session.commit()
                    flash(Markup("<strong>Добавлена категория:</strong> " + name), category='success')
                except:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.category'))


    @route('/edit_category', methods=["POST"])
    @login_required
    def edit_category(self):
        if (not current_user.right_category):
            return render_template('admin/access_denied.html')
        editCategoryForm = EditCategoryForm()
        if editCategoryForm.validate_on_submit():
            id = editCategoryForm.id.data
            name = editCategoryForm.name.data
            icon_name = editCategoryForm.icon_name.data

            if not name:
                flash('Неправильно заполнены поля', category='danger')
            else:
                category = Categories.query.get(id)
                category.name = name
                category.icon_name = icon_name
                try:
                    db.session.commit()
                    flash(Markup("<strong>Изменен вопрос:</strong> " + name), category='success')
                except:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.category'))


    @route('/delete_category', methods=["POST"])
    @login_required
    def delete_category(self):
        if (not current_user.right_category):
            return render_template('admin/access_denied.html')
        deleteCategoryForm = DeleteCategoryForm()
        if deleteCategoryForm.validate_on_submit():
            id = deleteCategoryForm.id.data
            count_qa = deleteCategoryForm.count_qa.data
            if int(id) == 0:
                flash('Нельзя удалять категорию "Популярное"', category='danger')
            elif int(count_qa) != 0:
                flash('Нельзя удалять категорию в которой есть вопросы. Переместите их в другую категорию или удалите', category='danger')
            else:
                category = Categories.query.get(id)
                name = category.name
                try:
                    db.session.delete(category)
                    db.session.commit()
                    flash(Markup("<strong>Удалена категория:</strong> " + name), category='success')
                except:
                    flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.category'))


    @route('/change_color', methods=["POST", "GET"])
    @login_required
    def change_color(self):
        if (not current_user.right_category):
            return render_template('admin/access_denied.html')
        color = request.args.get("color")
        cat_id = request.args.get("cat_id")
        category = Categories.query.get(cat_id)
        category.color = color

        try:
            db.session.commit()
            flash("Цвет категории успешно изменен", category='success')
        except:
            flash('Ошибка внесения изменений в базу данных', category='danger')

        return redirect(url_for('.category'))


    @route('/change_order_category', methods=['GET', 'POST'])
    def change_order_category(self):
        if (not current_user.right_category):
            return render_template('admin/access_denied.html')
        sequence_id = request.args.get("sequence_id")
        sequence_id = sequence_id.split(",")

        categories_list = Categories.query

        for i in range(len(sequence_id)):
            categories_list.get(int(sequence_id[i])).priority = i + 1

        try:
            db.session.commit()
            flash('Порядок сортировки категорий успешно обновлен', category='success')
        except:
            flash('Ошибка внесения изменений в базу данных', category='danger')
        return redirect(url_for('.category_sort'))