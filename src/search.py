import csv
from datetime import datetime

import pymorphy2
import enchant
import difflib
import re
from enchant.checker import SpellChecker
from fuzzywuzzy import fuzz
from sqlalchemy import exc

from config import bot_messages_emoji, bot_messages_not_found, bot_messages_break_search
from models import db, Categories, Questions, BlackWords, SynonymousWords, Requests, WhiteWords

morph = pymorphy2.MorphAnalyzer()
language = enchant.Dict("ru_RU")
checker = SpellChecker("ru_RU")


def convert_text(text):
    try:
        white_words = WhiteWords.query
        black_words = BlackWords.query
        synonyms = SynonymousWords.query
    except NameError:
        return "Ошибка чтения из БД"
    cleared_text = clear_string(text)
    correct_word_list = correct_error(cleared_text, white_words)
    result_word = []
    for correct_word in correct_word_list:
        correct_word = initial_form(correct_word, white_words)
        if len(correct_word) > 2:
            try:
                black_word = black_words.filter(BlackWords.word == correct_word).first()

                if black_word is None:
                    synonym_word = synonyms.filter(SynonymousWords.word == correct_word).first()
                    if synonym_word is not None and synonym_word.synonym_id is not None:
                        correct_word = synonyms.get(synonym_word.synonym_id).word
                    result_word.append(correct_word)

            except (NameError, AttributeError):
                return "Ошибка чтения из БД"
    return ' '.join(result_word)


def initial_form(word, white_words):
    try:
        is_white = white_words.filter(WhiteWords.word == word).first()
    except (NameError, AttributeError):
        return "Ошибка чтения из БД"
    if is_white:
        return word
    similar_word = morph.parse(word)[0]
    return similar_word.normal_form


def clear_string(text):
    return re.sub('[^а-я]', ' ', text.lower())


def correct_error(text, white_words):
    checker.set_text(text)
    word_list_mistakes = [i.word for i in checker]
    word_list = text.split()

    for word in word_list:
        is_white = white_words.filter(WhiteWords.word == word).first()
        if not is_white:
            if word_list_mistakes.__contains__(word):
                dictionary = dict()
                suggestions = set(language.suggest(word))
                for suggestion in suggestions:
                    measure = difflib.SequenceMatcher(None, word, suggestion).ratio()
                    dictionary[measure] = suggestion
                if len(dictionary) != 0:
                    word = dictionary[max(dictionary.keys())]
    return word_list


def parse_table():
    categories = list()
    with open("FAQ_CSV.csv") as r_file:
        file_reader = csv.DictReader(r_file, delimiter=",")
        try:
            if not (Categories.query.first() is None or Questions.query.first() is None):
                print("Таблицы категорий и вопросов должны быть пусты")
                return
        except NameError:
            print("Ошибка чтения из БД")
            return

        try:
            db.session.add(Categories(id=0, name="Популярное", priority=0))
        except exc.SQLAlchemyError:
            print("___ERROR___")
            return
        for row in file_reader:
            if not row["Категория"] in categories:
                categories.append(row["Категория"])
                category = Categories(name=row["Категория"], priority=len(categories))
                try:
                    db.session.add(category)
                except exc.SQLAlchemyError:
                    print("___ERROR___")
                    return
            qa = Questions(question=row["Вопрос"], clear_question=convert_text(row["Вопрос"]), answer=row["Ответ"],
                           cat_id=int(categories.index(row["Категория"]) + 1), priority=0)
            try:
                db.session.add(qa)
            except exc.SQLAlchemyError:
                print("___ERROR___")
                return
        try:
            db.session.commit()
            print("Все удачно добавлено")
        except exc.SQLAlchemyError:
            print("___ERROR___")


def get_answer(user_question):
    try:
        qa_list = Questions.query
    except NameError:
        print("Ошибка чтения БД")
        bot_message_text = (bot_messages_emoji["not_found"] + " ") if "not_found" in bot_messages_emoji else ""
        return bot_message_text + bot_messages_break_search
    scores = []
    clear_text = convert_text(user_question)
    request = Requests(original=re.sub("\n", " ", user_question), cleared=clear_text, date_time=datetime.now())
    try:
        db.session.add(request)
        db.session.commit()
    except exc.SQLAlchemyError:
        print('Ошибка внесения изменений в базу данных')
        bot_message_text = (bot_messages_emoji["not_found"] + " ") if "not_found" in bot_messages_emoji else ""
        return bot_message_text + bot_messages_break_search

    if not clear_text:
        bot_message_text = (bot_messages_emoji["not_found"] + " ") if "not_found" in bot_messages_emoji else ""
        return bot_message_text + bot_messages_not_found

    for qa in qa_list:
        scores += [(fuzz.token_sort_ratio(qa.clear_question.lower(), clear_text.lower()), qa)]
    max_scores = sorted(scores, key=lambda score: score[0], reverse=True)

    result = []
    for max_score in max_scores[:3]:
        if max_score[0] > 40:
            result += [max_score]
    return result
