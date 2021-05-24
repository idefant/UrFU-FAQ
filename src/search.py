import csv
import pymorphy2
import enchant
import difflib
import re
from enchant.checker import SpellChecker
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import fuzz
from sqlalchemy import exc

from app import app
from dbase import db, Categories, Questions


db = SQLAlchemy(app)
morph = pymorphy2.MorphAnalyzer()
language = enchant.Dict("ru_RU")
checker = SpellChecker("ru_RU")


def convert_text(string):
    word_list = (clear_string(string))
    result_word = []
    for word in word_list:
        word = initial_form(word)
        if len(word) > 2:
            result_word.append(word)
    return ' '.join(result_word)


def initial_form(word):

    similar_word = morph.parse(word)[0]
    return similar_word.normal_form


def clear_string(text):
    return re.split('[^а-яА-Я]', text)


def correct_error(text):
    checker.set_text(text)
    word_list_mistakes = [i.word for i in checker]
    word_list = text.split()

    for i in range(len(word_list)):
        if word_list_mistakes.__contains__(word_list[i]):
            dictionary = dict()
            suggestions = set(language.suggest(word_list[i]))
            for word in suggestions:
                measure = difflib.SequenceMatcher(None, word_list[i], word).ratio()
                dictionary[measure] = word
            word_list[i] = dictionary[max(dictionary.keys())]
    return word_list


def parse_table():
    categories = list()  # Заменить этот массив на БД
    with open("FAQ_CSV.csv") as r_file:
        file_reader = csv.DictReader(r_file, delimiter=",")
        for row in file_reader:
            if not row["Категория"] in categories:
                categories.append(row["Категория"])
                category = Categories(name=row["Категория"], priority=0)
                try:
                    # db.session.add(category)
                    # db.session.commit()
                    print("OK")
                except exc.SQLAlchemyError:
                    print("___ERROR___")
            qa = Questions(question=row["Вопрос"], clear_question=convert_text(row["Вопрос"]), answer=row["Ответ"],
                           cat_id=int(categories.index(row["Категория"]) + 1), priority=0)
            try:
                db.session.add(qa)
                db.session.commit()
                print("OK")
            except exc.SQLAlchemyError:
                print("___ERROR___")


def get_answer(request):
    qa_list = db.session.query(Questions)
    scores = []
    clear_text = correct_error(convert_text(request))
    clear_text = ' '.join(clear_text)
    for qa in qa_list:
        scores += [(fuzz.token_sort_ratio(qa.question.lower(), clear_text.lower()), qa)]

    max_scores = sorted(scores, key=lambda score: score[0], reverse=True)
    for max_score in max_scores:
        if max_score[0] < 50:  # или WRatio
            break
        print(max_score[0])
        print(max_score[1].question)
