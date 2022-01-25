import random


def get_ready():
    text = ['Ну давай попробуем...', 'Сейчас делаю.', 'Без проблем.',
            'Чуть синей изоленты и...', 'За **ACOG** сделаю всё, что угодно.',
            'Потерпи чуть, я не такой быстрый. У меня 2 скорости.\n*плачет по-ягерски*',
            'Ставлю **Систему отражения гранат**.', 'Vierundzwanzigstundenglück!', 'Подержи-ка мой ягермейстер...']
    return random.choice(text)


def get_hello(name):
    if name is None:
        name = "Незнакомец"
    text = ['Guten Tag, {}', 'Здаров {}', 'Привет {}', '{} и тебе привет.', "Ку, {}"]
    return random.choice(text).format(name)


def get_no_roots():
    text = ['Не превышайся. У мебя нет таких возможностей.',
            'Сам это делай. Ты ещё не настолько крутой, чтобы пользоваться всеми моими возможностями',
            '*ругается на немецком*']
    return random.choice(text)


def get_top_killer(name, kills):
    text = ['{} стырил **больше всего** фрагов.\nОбщее количество: {} убийств',
            '**Благодаря** {} в мире стало на {} трупов больше',
            '**Лучший убийца**: {}. Рекорд дня: {} убийств.\nБольше и нечего говорить.',
            'Святой покровитель убийств {} сегодня дает жару!\n{} убийств!']
    return random.choice(text).format(name, kills)


def get_top_winner(name, wins):
    text = ['Успей сыграть с {}! Сегодня он **вытащил** {} катки!',
            '**Неудержимый** {} не знает, что такое поражение после {} выигранных матчей',
            '**Героем дня** по победам становится {}\nРекорд: {} выигранных каток',
            '"I play for **win**!" - говорит {}\n{} битв выиграно!']
    return random.choice(text).format(name, wins)


def get_random_phrase():
    text = ['Как-то тихо здесь... Пошли в R6!', '**IMPOSTER**']
    return random.choice(text)


def get_how_to_play():
    text = ['Никак. Просто удаляй эту игру.']
    return random.choice(text)


def get_incorrect_input():
    text = ['К сожалению, не могу понять вас...']
    return random.choice(text)