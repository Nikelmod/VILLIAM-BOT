# импорты
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from toks import main_token
import random
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
import sys
import requests
import pyowm
import pymongo
from mongoclient import quotes, jokes

# работа с вк, подключение токена

vk_session = vk_api.VkApi(token=main_token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# токен погоды и подключение

owm = OWM('c33406334cf075dbd650847df2eb3ef4')
mgr = owm.weather_manager()

# текст для меню
# дополнять при необходимости
menu_text = '''Я Вильем Бот, я много чего умею и постоянно стараюсь развиваться, но иногда мне бывает лень.
            А еще всякие людишки говорят, что я тупой, но они просто не понимают, что развитие всегда идет постепенно!
            Кстати, я умею неплохо так шутиить.
            Мои возможности:
            &#128073; !меню - это доступ к этой панельке
            &#128073; !погода - информация о температуре в городе
            &#128073; !котик - разные котики на разные дни &#128521;
            &#128073; !угадайка - попробуй угадать страну
            &#128073; !шутка - случайная шутка от известного человека или из фильма
            &#128073; !цитата - цитаты на каждый день &#128521;
            &#128073; !калькулятор - поможет вам посчитать что-нибудь
            &#128073; !предложитьшутку - напишите эту команду, а следом за ней через пробел шутку, которую хотите добавить.
            &#128073; !предложитьцитату - напишите эту команду, а следом за ней через пробел цитату, которую хотите добавить.
            &#128073; !помощь - вся информация о том как мной руководить'''


# cписок всех шуток для бд

# joke
def joke(id):
    jokes_list = ['Есть только две бесконечные вещи: Вселенная и глупость. Хотя насчет Вселенной я не уверен.'
                  '(Альберт Эйнштейн)',
                  'Иногда надо рассмешить людей, чтобы отвлечь их от желания вас повесить.(Б. Шоу)',

                  'Страшный радикулит. Старожилы не помнят, чтобы у человека так болела ****.(Ф. Раневская)',

                  'Индиана Джонс неожиданно выигрывает дуэль на саблях с помощью пистолета.',

                  'Только что преждевременно скончался мой двоюродный брат. Ему было всего 19 лет. Его ужалила пчела, '
                  'вечный враг канатоходца.'
                  '(Дэн Разер, телеведущий)',

                  'Когда до моих родителей наконец дошло, что меня похитили, они не медлили ни минуты'
                  'и сразу же сдали внаем мою комнату.(В. Аллен)',

                  'Река была такой грязной, что временами казалось, будто она течет дном вверх.(Т. Пратчетт)',

                  'Человек может долго жить на деньги, которые ждет.(Уильям Фолкнер)',

                  'Пунктуальность — это вежливость зануд.(Ивлин Во)',

                  'Женщина может сделать миллионером любого мужчину-миллиардера.(Чарли Чаплин)',

                  'Мужчины любят женщин, женщины любят детей, дети любят хомячков, хомячки никого не любят.'
                  '(Эйлис Эллис)',

                  'Небьющаяся игрушка — это такая игрушка, которой ребенок может разбить все остальные свои игрушки.'
                  '(Бейтс Каунти)',

                  'Одно неловкое движение — и ты отец.(М. Жванецкий)']
    joke_text = random.choice(jokes_list)
    vk_session.method('messages.send', {'user_id': id, 'message': joke_text, 'random_id': 0})


# список цитат для бд

# quote
def quote(id):
    quotes_list = ['Что разум человека может постигнуть и во что он может поверить, того он способен достичь'
                   '(Наполеон Хилл)',

                   'Стремитесь не к успеху, а к ценностям, которые он дает(Альберт Эйнштейн)',

                   'Своим успехом я обязана тому, что никогда не оправдывалась и не принимала оправданий от других.'
                   '(Флоренс Найтингейл)',

                   'Надо любить жизнь больше, чем смысл жизни.(Федор Достоевский)',

                   'Жизнь - это то, что с тобой происходит, пока ты строишь планы.(Джон Леннон)',

                   'Логика может привести Вас от пункта А к пункту Б, а воображение — куда угодно.(Альберт Эйнштейн)',

                   'Начинать всегда стоит с того, что сеет сомнения.(Борис Стругацкий)',

                   'Настоящая ответственность бывает только личной.(Фазиль Искандер)',

                   'Неосмысленная жизнь не стоит того, чтобы жить.(Сократ)',

                   '80% успеха - это появиться в нужном месте в нужное время.(Вуди Аллен)',

                   'Ваше время ограничено, не тратьте его, живя чужой жизнью.(Стив Джобс)',

                   'Победа - это еще не все, все - это постоянное желание побеждать.(Винс Ломбарди)',

                   'В моем словаре нет слова «невозможно».(Наполеон Бонапарт)']
    quote_text = random.choice(quotes_list)
    vk_session.method('messages.send', {
        'user_id': id,
        'message': quote_text,
        'random_id': 0
    })


# отправка цитат

def quote_sender(id):
    n = random.randint(1, 13)
    message = quotes.find_one({'myid': n})['quote']
    sender(id, message)


# отправка шуток

def joke_sender(id):
    n = random.randint(1, 13)
    message = jokes.find_one({'myid': n})['joke']
    sender(id, message)


# обработка команды !погода

# температуры в больших городах
def temperature(id):
    text = 'Напиши название города, который тебя интересует(что бы прекратить напиши !стоп)'
    vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})

    for event in longpoll.listen():

        if (event.type == VkEventType.MESSAGE_NEW) & event.to_me:
            id = event.user_id
            city = event.text.lower()

            if city != '!стоп':

                try:
                    observation = mgr.weather_at_place(city)
                    weather = observation.weather
                    temperature = str(weather.temperature('celsius')['temp']) + '°C'  # вывод температуры

                except:
                    temperature = 'Сорян, я такого города не знаю('  # обработка ошибок

                sender(id, temperature)

            else:
                sender(id, menu_text)
                break


# функция для отправки сообщений

def sender(id, text):
    vk_session.method('messages.send', {
        'user_id': id,
        'message': text,
        'random_id': 0
    })


# функция для !котик

# выводить фото случайного кота

def cats(id):
    upload = vk_api.VkUpload(vk_session)
    n = random.randint(1, 8)  # генерация случайно фото
    photo = upload.photo_messages(f'./images/cats/{n}.jpg')  # выбор фото из папки

    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0]['access_key']
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'

    vk_session.method('messages.send', {'peer_id': id, 'attachment': attachment, 'random_id': 0})  # вывод фото


# функция для игры в угадайку

# выводить случайное фото из 3 и просит угадать страну
def pole(id):
    start_message = 'Какая страна изображения на фотографии?\n1. Россия\n2. Африка\n3. Англия'

    countries = [
        ['россия', 'photo-203505771_457239022'],

        ['африка', 'photo-203505771_457239023'],

        ['англия', 'photo-203505771_457239024'],
    ]

    country = countries[random.randint(0, 2)]

    vk_session.method('messages.send', {'peer_id': id,
                                        'message': start_message,
                                        'attachment': country[1],
                                        'random_id': 0
                                        })

    for event in longpoll.listen():

        if (event.type == VkEventType.MESSAGE_NEW) & event.to_me:
            user_message = event.text.lower()

            if user_message != '!стоп':

                if user_message == country[0]:

                    sender(id, 'Ты угадал! Это -' + country[0])
                    sender(id, menu_text)
                    break

                else:
                    sender(id, 'Не правильно, попробуй ещё. Если ты хочешь выйти - напиши !стоп')
            else:
                sender(id, menu_text)
                break


# функция для вывода помощи

def help(id):
    sender(id, '''Команда !меню поможет вам узнать какие команды присутсвуют в боте. 
            Все команды начинаются с восклицательного знака и без пробела''')


# основной цикл программы

# все функции и переходы к ним - здесь

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:

            msg = event.text.lower()
            id = event.user_id
            if 'привет' in msg or msg == 'ку' or msg == 'хай' or 'салам' in msg:
                sender(id, 'Привет &#9995; , напиши !меню')

            elif msg == '!меню':
                sender(id, menu_text)

            elif msg == '!помощь':
                help(id)

            elif msg == '!шутка':
                joke_sender(id)

            elif msg == '!цитата':
                quote_sender(id)

            elif msg == '!калькулятор':
                sender(id, 'Я тебе не рабочий, в гугле есть калькулятор -_-')

            elif '!предложитьшутку' in msg:
                sender(id, 'Спасибо за шутку, администрация рассмотрит её и добавит, если посчитает нужной')

            elif '!предложитьцитату' in msg:
                sender(id, 'Спасибо за цитату, администрация рассмотрит её и добавит, если посчитает нужной')

            elif msg == '!погода':
                temperature(id)

            elif msg == '!котик':
                cats(id)

            elif msg == '!угадайка':
                pole(id)

            else:
                sender(id, 'Я немного дуб дубочек и вас не понял, напишите !меню, что бы узнать, что я умею')
# конец
