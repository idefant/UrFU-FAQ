import csv
from datetime import datetime

import pymorphy2
import enchant
import difflib
import re
from enchant.checker import SpellChecker
from flask_sqlalchemy import SQLAlchemy
from fuzzywuzzy import fuzz
from sqlalchemy import exc

# from app import app
from models import db, Categories, Questions, BlackWords, SynonymousWords, Requests, WhiteWords

# db = SQLAlchemy()
morph = pymorphy2.MorphAnalyzer()
language = enchant.Dict("ru_RU")
checker = SpellChecker("ru_RU")


def convert_text(string):
    white_words = WhiteWords.query
    cleared_text = clear_string(string)
    word_list = correct_error(cleared_text, white_words)
    result_word = []
    for word in word_list:
        word = initial_form(word, white_words)
        if len(word) > 2:
            db_word = BlackWords.query.filter(BlackWords.word == word).first()
            if db_word is None:
                syn_word = SynonymousWords.query.filter(SynonymousWords.word == word).first()
                if syn_word is not None and syn_word.synonym_id is not None:
                    word = SynonymousWords.query.get(syn_word.synonym_id).word
                result_word.append(word)
    return ' '.join(result_word)


def initial_form(word, white_words):
    is_white = white_words.filter(WhiteWords.word == word).first()
    if is_white:
        return word
    similar_word = morph.parse(word)[0]
    return similar_word.normal_form


def clear_string(text):
    return re.sub('[^а-яА-Я]', ' ', text)


def correct_error(text, white_words):
    checker.set_text(text)
    word_list_mistakes = [i.word for i in checker]
    word_list = text.split()

    for i in range(len(word_list)):
        is_white = white_words.filter(WhiteWords.word == word_list[i]).first()
        if not is_white:
            if word_list_mistakes.__contains__(word_list[i]):
                dictionary = dict()
                suggestions = set(language.suggest(word_list[i]))
                for word in suggestions:
                    measure = difflib.SequenceMatcher(None, word_list[i], word).ratio()
                    dictionary[measure] = word
                if len(dictionary) != 0:
                    word_list[i] = dictionary[max(dictionary.keys())] # падает на max
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


def get_answer(user_question):
    qa_list = Questions.query
    scores = []
    clear_text = convert_text(user_question)


    request = Requests(original=user_question, cleared=clear_text, date_time=datetime.now())

    try:
        db.session.add(request)
        db.session.commit()
    except exc.SQLAlchemyError:
        print('Ошибка внесения изменений в базу данных')


    # print(clear_text)
    for qa in qa_list:
        scores += [(fuzz.token_sort_ratio(qa.clear_question.lower(), clear_text.lower()), qa)]

    max_scores = sorted(scores, key=lambda score: score[0], reverse=True)

    result = []
    for max_score in max_scores[:3]:
        if max_score[0] > 40:  # или WRatio
            result += [(max_score)]
    return result