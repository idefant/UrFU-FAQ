from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, HiddenField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


class AddQAForm(FlaskForm):
    question = StringField("Вопрос", validators=[DataRequired()])
    answer = TextAreaField('Ответ', render_kw={"rows": 5, "cols": 50})
    popular = BooleanField("Популярное")
    cat_id = SelectField("Категория: ", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Добавить")


class EditQAForm(FlaskForm):
    id = HiddenField("id")
    question = StringField("Вопрос", validators=[DataRequired()])
    answer = TextAreaField('Ответ', render_kw={"rows": 5, "cols": 50})
    popular = BooleanField("Популярное")
    cat_id = SelectField("Категория: ", coerce=int)
    submit = SubmitField("Сохранить изменения")


class DeleteQAForm(FlaskForm):
    id = HiddenField("id")
    submit = SubmitField("Удалить")


class AddCategoryForm(FlaskForm):
    category = StringField("Категория", validators=[DataRequired()])
    icon_name = StringField("Имя иконки*", validators=[DataRequired()])
    submit = SubmitField("Добавить")


class EditCategoryForm(FlaskForm):
    id = HiddenField("id")
    name = StringField("Категория", validators=[DataRequired()])
    icon_name = StringField("Имя иконки*", validators=[DataRequired()])
    submit = SubmitField("Сохранить изменения")


class DeleteCategoryForm(FlaskForm):
    id = HiddenField("id")
    count_qa = HiddenField("count_qa")
    submit = SubmitField("Удалить")


class EditAccountForm(FlaskForm):
    name = StringField("ФИО", validators=[DataRequired()])
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Подтвердите паролем", validators=[DataRequired()])
    submit = SubmitField("Сохранить изменения")


class ChangePasswordAccountForm(FlaskForm):
    old_password = PasswordField("Старый пароль", validators=[DataRequired()])
    password = StringField("Новый пароль", validators=[DataRequired()])
    password_confirm = PasswordField("Повторите пароль", validators=[DataRequired()])
    submit = SubmitField("Обновить пароль")


class AddUserForm(FlaskForm):
    name = StringField("ФИО", validators=[DataRequired()])
    username = StringField("Логин", validators=[DataRequired()])
    password = StringField("Пароль", validators=[DataRequired()])
    post = StringField("Должность", validators=[DataRequired()])

    right_category = BooleanField("Категории")
    right_user = BooleanField("Доступ к странице пользователей")
    right_qa = BooleanField("Вопросы")
    right_synonym = BooleanField("Синонимы")
    right_black_word = BooleanField("Список черных слов")
    submit = SubmitField("Добавить")


class EditUserForm(FlaskForm):
    id = HiddenField("id")
    name = StringField("ФИО", validators=[DataRequired()])
    username = StringField("Логин", validators=[DataRequired()])
    post = StringField("Должность", validators=[DataRequired()])
    submit = SubmitField("Сохранить изменения")


class DeactivateUserForm(FlaskForm):
    id = HiddenField("id")
    submit = SubmitField("Деактивировать")


class ActivateUserForm(FlaskForm):
    id = HiddenField("id")
    submit = SubmitField("Активировать заново")


class DeleteUserForm(FlaskForm):
    id = HiddenField("id")
    submit = SubmitField("Удалить навсегда")


class ChangePasswordUserForm(FlaskForm):
    id = HiddenField("id")
    password = StringField("Новый пароль", validators=[DataRequired()])
    submit = SubmitField("Сменить пароль")


class EditUserRightsForm(FlaskForm):
    id = HiddenField("id")
    right_category = BooleanField("Категории")
    right_users = BooleanField("Пользователи")
    right_qa = BooleanField("Вопросы")
    right_synonym = BooleanField("Синонимы")
    right_black_word = BooleanField("Список черных слов")
    submit = SubmitField("Сохранить изменения")


class AddExceptionWordForm(FlaskForm):
    word = StringField("Слово", validators=[DataRequired()])
    submit = SubmitField("Добавить")


class EditExceptionWordForm(FlaskForm):
    id = HiddenField("id")
    word = StringField("Слово", validators=[DataRequired()])
    submit = SubmitField("Сохранить изменения")


class DeleteExceptionWordForm(FlaskForm):
    id = HiddenField("id")
    submit = SubmitField("Удалить")


class AddSynonymsDependentForm(FlaskForm):
    word = StringField("Слово", validators=[DataRequired()])
    submit = SubmitField("Добавить")


class EditSynonymsDependentForm(FlaskForm):
    word_id = HiddenField("id")
    word = StringField("Слово", validators=[DataRequired()])
    submit = SubmitField("Сохранить изменения")


class DeleteSynonymsDependentForm(FlaskForm):
    word_id = HiddenField("id")
    submit = SubmitField("Удалить")
