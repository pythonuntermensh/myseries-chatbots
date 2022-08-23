from glob import escape
from vkbottle.bot import Message
from random import randint
import requests, json, os

from loader import bot
from data.config import ADMINS, SERIES_IP, NEW_SERIES_IP
from keyboard import MENU_KEYBOARD, CANCEL_KEYBOARD, ADMIN_KEYBOARD, URL_REPLY
from states import SubscribeState, UnsubscribeState, BugReport, Mailing, MainUrl, SecondUrl, BugReportAnswer


@bot.on.message(text=["Меню", "Начать", "начать", "меню"])
@bot.on.message(payload={"cmd": "menu"})
async def start_message(message: Message):
    await message.answer("Выберите опцию", keyboard=MENU_KEYBOARD)


@bot.on.message(text="stop nahoi")
async def stop_nahoi(message: Message):
    if str(message.from_id) in ADMINS:
        os._exit(0)


@bot.on.message(text=["Админ", "админ", "Admin", "admin"])
async def admin_message(message: Message):
    if str(message.from_id) in ADMINS:
        await message.answer("Выберите опцию", keyboard=ADMIN_KEYBOARD)


@bot.on.message(text="Массовая рассылка")
@bot.on.message(payload={"cmd": "mailing"})
async def mailing_message(message: Message):
    if str(message.from_id) in ADMINS:
        await message.answer("➤Введите сообщение для массовой рассылки:", keyboard=CANCEL_KEYBOARD)
        await bot.state_dispenser.set(message.from_id, Mailing.WAITING_FOR_MAILING_MESSAGE)

@bot.on.message(state=Mailing.WAITING_FOR_MAILING_MESSAGE)
async def maling_message_handler(message: Message):
    if (message.text == "Отмена"):
        await message.answer("Меню", keyboard=MENU_KEYBOARD)
        await bot.state_dispenser.delete(message.from_id)
    else:
        subscribers_response = requests.get("http://" + SERIES_IP + "/rest/getSubscribers?vk=true")
        subscribers = json.loads(subscribers_response.text)
        for subscriber in subscribers:
            await bot.api.messages.send(user_id=int(subscriber), message=message.text, random_id=randint(0, 9999999))
        await message.answer("Маcсовая рассылка прошла успешно!", keyboard=MENU_KEYBOARD)
        await bot.state_dispenser.delete(message.from_id)


@bot.on.message(text="Изменить основную ссылку")
@bot.on.message(payload={"cmd": "change_main_url"})
async def mailing_message(message: Message):
    if str(message.from_id) in ADMINS:
        await message.answer("➤Введите новую основную ссылку:", keyboard=CANCEL_KEYBOARD)
        await bot.state_dispenser.set(message.from_id, MainUrl.WAITING_FOR_NEW_URL)

@bot.on.message(state=MainUrl.WAITING_FOR_NEW_URL)
async def new_main_url_handler(message: Message):        
    if (message.text == "Отмена"):
        await message.answer("Меню", keyboard=MENU_KEYBOARD)
        await bot.state_dispenser.delete(message.from_id)
    else:
        with open("web_url.txt", "r+") as f:
            urls = f.read().split("||")
            urls[0] = message.text
            f.seek(0)
            f.write(urls[0] + "||" + urls[1])
            f.truncate()
        await message.answer("Основная ссылка была изменена!", keyboard=MENU_KEYBOARD)
        await bot.state_dispenser.delete(message.from_id)


@bot.on.message(text="Изменить зеркало")
@bot.on.message(payload={"cmd": "change_second_url"})
async def mailing_message(message: Message):
    if str(message.from_id) in ADMINS:
        await message.answer("➤Введите новое зеркало:", keyboard=CANCEL_KEYBOARD)
        await bot.state_dispenser.set(message.from_id, SecondUrl.WAITING_FOR_NEW_URL)

@bot.on.message(state=SecondUrl.WAITING_FOR_NEW_URL)
async def new_main_url_handler(message: Message):        
    if (message.text == "Отмена"):
        await message.answer("Меню", keyboard=MENU_KEYBOARD)
        await bot.state_dispenser.delete(message.from_id)
    else:
        with open("web_url.txt", "r+") as f:
            urls = f.read().split("||")
            urls[1] = message.text
            f.seek(0)
            f.write(urls[0] + "||" + urls[1])
            f.truncate()
        await message.answer("Зеркало было изменено!", keyboard=MENU_KEYBOARD)
        await bot.state_dispenser.delete(message.from_id)


@bot.on.message(text="Ответить на баг репорт")
@bot.on.message(payload={"cmd": "bug_report_answer"})
async def bug_report_answer_message(message: Message):
    if str(message.from_id) in ADMINS:
        await message.answer("➤Введите ссылку на страницу из баг репорта:", keyboard=CANCEL_KEYBOARD)
        await bot.state_dispenser.set(message.from_id, BugReportAnswer.WAITING_FOR_USER_URL)

@bot.on.message(state=BugReportAnswer.WAITING_FOR_USER_URL)
async def bug_report_url_answer_handler(message: Message):        
    if (message.text == "Отмена"):
        await message.answer("Меню", keyboard=MENU_KEYBOARD)
        await bot.state_dispenser.delete(message.from_id)
    else:
        await message.answer("➤Введите ответ на баг репорт:", keyboard=CANCEL_KEYBOARD)
        await bot.state_dispenser.set(message.from_id, BugReportAnswer.WAITING_FOR_ANSWER_MESSAGE, user_url=message.text)

@bot.on.message(state=BugReportAnswer.WAITING_FOR_ANSWER_MESSAGE)
async def bug_report_text_answer_handler(message: Message):   
    if (message.text == "Отмена"):
        await message.answer("Меню", keyboard=MENU_KEYBOARD)
        await bot.state_dispenser.delete(message.from_id)
    else:
        try:
            user_id = message.state_peer.payload["user_url"].split("id")[1]
            await bot.api.messages.send(user_id=user_id, message=f"➤Адинистратор ответил на Ваш баг репорт:\n{message.text}",\
            random_id=randint(0, 9999999))
            await message.answer("Ответ на баг репорт был отправлен!", keyboard=MENU_KEYBOARD)
        except:
            await message.answer("Ошибка! Проверьте правильность введенной ссылки", keyboard=MENU_KEYBOARD)
        await bot.state_dispenser.delete(message.from_id)


@bot.on.message(text="Все подписки")
@bot.on.message(payload={"cmd": "subs"})
async def subscribes_message(message: Message):
    res = requests.get("http://" + SERIES_IP + "/rest/getSubscribedSeries?id=" + str(message.from_id)\
            + "&vk=true&number=25")
    text = list(json.loads(res.text))
    if len(text) > 0:
        answer = "➤Список подписок:\n\t→" + "\n\t→".join(text)
    else:
        answer = "➤Список подписок пуст"
    await message.answer(answer, keyboard=MENU_KEYBOARD)


@bot.on.message(text="Подписаться на новинки")
@bot.on.message(payload={"cmd": "subscribe_novelties"})
async def subscribe_novelties(message: Message):
    res = requests.get("http://" + SERIES_IP + "/rest/subscribeNewSeries?id=" + str(message.from_id) + "&vk=true")
    text = res.text
    if text == "Subscribed":
        await message.answer("Подписка на новинки оформлена", keyboard=MENU_KEYBOARD)
    elif text == "Already subscribed":
        await message.answer("Вы уже подписаны на новинки", keyboard=MENU_KEYBOARD)


@bot.on.message(text="Отписаться от новинок")
@bot.on.message(payload={"cmd": "unsubscribe_novelties"})
async def subscribe_novelties(message: Message):
    res = requests.get("http://" + SERIES_IP + "/rest/unsubscribeNewSeries?id=" + str(message.from_id) + "&vk=true")
    text = res.text
    if text == "Unsubscribed":
        await message.answer("Вы отписались от новинок", keyboard=MENU_KEYBOARD)
    elif text == "Already unsubscribed":
        await message.answer("Вы не были подписаны на новинки", keyboard=MENU_KEYBOARD)


@bot.on.message(text="Баг репорт")
@bot.on.message(payload={"cmd": "bug_report"})
async def bug_report(message: Message):
    await bot.state_dispenser.set(message.from_id, BugReport.WAITING_FOR_REPORT)
    await message.answer("➤Опишите ошибку - ваше сообщение получит администрация:", keyboard=CANCEL_KEYBOARD)

@bot.on.message(state=BugReport.WAITING_FOR_REPORT)
async def bug_report_handler(message: Message):
    if (message.text == "Отмена"):
        await message.answer("Меню", keyboard=MENU_KEYBOARD)
        await bot.state_dispenser.delete(message.from_id)
    else:
        for admin in ADMINS:
            await bot.api.messages.send(user_id=int(admin), message=f"Баг репорт от пользователя https://vk.com/id{message.from_id} :\n\t→{message.text}",\
                random_id=randint(0, 9999999))
        await message.answer("Ваше сообщение было отправлено администратору.\nСпасибо за проявленную активность!", keyboard=MENU_KEYBOARD)
    await bot.state_dispenser.delete(message.from_id)


@bot.on.message(text="Актуальная ссылка")
@bot.on.message(payload={"cmd": "web_url"})
async def url_message(message: Message):
    with open("web_url.txt", "r") as f:
        urls = f.read().split("||")
        await message.answer("➤Актуальная ссылка: " + urls[0])
    await message.answer("➤Внимание! Если данное зеркало заблокировано, нажми на кнопку \"Заблокировано!\" и я пришлю другое зеркало!",\
        keyboard=URL_REPLY)


@bot.on.message(text="Заблокировано")
@bot.on.message(payload={"cmd": "banned_url"})
async def banned_url_message(message: Message):
    with open("web_url.txt", "r") as f:
        urls = f.read().split("||")
        await message.answer("Зеркало: " + urls[1])
    await message.answer("Пожалуйста, сохраните данное зеркало у себя в закладках, и перешлите его всем вашим друзьям (не делитесь данным зеркалом в социальной сети, на форуме и на любом другом публичном ресурсе!).")
    await message.answer("Данное зеркало сайта не является публичным адресом в Интернете, то есть вы его не найдете в поисковых системах, социальных сетях и иных публичных сервисах.", keyboard=MENU_KEYBOARD)


@bot.on.message(text="Подписаться на сериал")
@bot.on.message(payload={"cmd": "subscribe_series"})
async def subscribe_series_message(message: Message):
    await message.answer("➤Введите имя сериала")
    await message.answer("➤Если хотите подписаться сразу на несколько сериалов, напишите названия - каждое с новой строки", keyboard=CANCEL_KEYBOARD)
    await bot.state_dispenser.set(message.from_id, SubscribeState.WAITING_FOR_SERIES_NAME)

@bot.on.message(state=SubscribeState.WAITING_FOR_SERIES_NAME)
async def subscribe_main_handler(message: Message):
    if (message.text == "Отмена"):
        await message.answer("Меню", keyboard=MENU_KEYBOARD)
        await bot.state_dispenser.delete(message.from_id)
    else:
        next = False
        series = message.text.split("\n")
        series_with_help = list()
        _keyboard = MENU_KEYBOARD
        _message = "Меню"
        for n in series:
            same_series_response = requests.get("http://" + SERIES_IP + "/rest/getSeriesWithSameName?name=" + n.strip())
            same_series = json.loads(same_series_response.text)
            if len(same_series) > 1:
                series_with_help.append(n.strip())
            else:
                res = requests.get("http://" + SERIES_IP + "/rest/subscribe?id=" + str(message.from_id) + "&name=" \
                    + n.strip() + "&vk=true&num=0")
                text = res.text
                if text == "Subscribed":
                    await message.answer(n + " - подписка оформлена")
                elif text == "Already subscribed":
                    await message.answer(n + " - Вы уже были подписаны на этот сериал")
                else:
                    await message.answer(n + " - неверное название или нет на сайте!")
                    _keyboard=CANCEL_KEYBOARD
                    _message = "Проверьте правильность написания и повторите"
                    next = True
        if len(series_with_help) > 0:
            answer = str()
            same_series_response = requests.get("http://" + SERIES_IP + "/rest/getSeriesWithSameName?name=" + series_with_help[0])
            same_series = json.loads(same_series_response.text)
            for x in range(len(same_series)):
                answer += "\n\t" + str(x+1) + ". " + same_series[x]["name"] + " - " + same_series[x]["additional"]
            await message.answer("➤Было найдено несколько сериалов с таким названием - введите номер нужного:\n"\
                + "\t" + answer, keyboard=CANCEL_KEYBOARD)
            await bot.state_dispenser.set(message.from_id, SubscribeState.WAITING_FOR_SERIES_NUM, series_name=series_with_help[0])
            next = True
            return 
        if not next:
            await bot.state_dispenser.delete(message.from_id)
        await message.answer(message=_message, keyboard=_keyboard)

@bot.on.message(state=SubscribeState.WAITING_FOR_SERIES_NUM)
async def subscribe_help_handler(message: Message):
    if (message.text == "Отмена"):
        await message.answer(f"Меню", reply_markup=MENU_KEYBOARD)
        await bot.state_dispenser.delete(message.from_id)
    else:
        try:
            series_num = int(message.text)
            series_num -= 1
            if (series_num < 0): 
                await message.answer("Попробуйте еще раз", keyboard=CANCEL_KEYBOARD)
            series_name = message.state_peer.payload["series_name"]
            res = requests.get("http://" + SERIES_IP + "/rest/subscribe?id=" + str(message.from_id) + "&name=" + series_name + "&vk=true&num=" + str(series_num))
            if res.text == "Repeat bleat":
                await message.answer("Попробуйте еще раз", keyboard=CANCEL_KEYBOARD)
            elif res.text == "Subscribed":
                await message.answer(series_name + " - подписка оформлена", keyboard=MENU_KEYBOARD)
                await bot.state_dispenser.delete(message.from_id)
            elif res.text == "Already subscribed":
                await message.answer(series_name + " - Вы уже были подписаны на этот сериал", keyboard=MENU_KEYBOARD)
                await bot.state_dispenser.delete(message.from_id)
        except Exception as err:
            await message.answer(f"Попробуйте еще раз", keyboard=CANCEL_KEYBOARD)


@bot.on.message(text="Отписаться от сериала")
@bot.on.message(payload={"cmd": "unsubscribe_series"})
async def subscribe_series_message(message: Message):
    await message.answer("➤Введите имя сериала для удаления", keyboard=CANCEL_KEYBOARD)
    await bot.state_dispenser.set(message.from_id, UnsubscribeState.WAITING_FOR_SERIES_NAME)

@bot.on.message(state=UnsubscribeState.WAITING_FOR_SERIES_NAME)
async def unsubscribe_main_handler(message: Message):
    if (message.text == "Отмена"):
        await message.answer("Меню", keyboard=MENU_KEYBOARD)
        await bot.state_dispenser.delete(message.from_id)
    else:
        next = False
        series = message.text.split("\n")
        series_with_help = list()
        _keyboard = MENU_KEYBOARD
        _message = "Меню"
        for n in series:
            same_series_response = requests.get("http://" + SERIES_IP + "/rest/getSeriesWithSameName?name=" + n.strip())
            same_series = json.loads(same_series_response.text)
            if len(same_series) > 1:
                series_with_help.append(n.strip())
            else:
                res = requests.get("http://" + SERIES_IP + "/rest/unsubscribe?id=" + str(message.from_id) + "&name=" \
                    + n.strip() + "&vk=true&num=0")
                text = res.text
                if text == "Unsubscribed":
                    await message.answer(n + " - Вы отписались от сериала")
                elif text == "Already unsubscribed":
                    await message.answer(n + " - Вы не были подписаны на этот сериал")
                else:
                    await message.answer(n + " - неверное название или нет на сайте!")
                    _keyboard=CANCEL_KEYBOARD
                    _message = "Проверьте правильность написания и повторите"
                    next = True
        if len(series_with_help) > 0:
            answer = str()
            same_series_response = requests.get("http://" + SERIES_IP + "/rest/getSeriesWithSameName?name=" + series_with_help[0])
            same_series = json.loads(same_series_response.text)
            for x in range(len(same_series)):
                answer += "\n\t" + str(x+1) + ". " + same_series[x]["name"] + " - " + same_series[x]["additional"]
            await message.answer("➤Было найдено несколько сериалов с таким названием - введите номер нужного:\n"\
                + "\t" + answer, keyboard=CANCEL_KEYBOARD)
            await bot.state_dispenser.set(message.from_id, UnsubscribeState.WAITING_FOR_SERIES_NUM, series_name=series_with_help[0])
            next = True
            return
        if not next:
            await bot.state_dispenser.delete(message.from_id)
        await message.answer(message=_message ,keyboard=_keyboard)

@bot.on.message(state=UnsubscribeState.WAITING_FOR_SERIES_NUM)
async def unsubscribe_help_handle(message: Message):
    if (message.text == "Отмена"):
        await message.answer("Меню", keyboard=MENU_KEYBOARD)
        await bot.state_dispenser.delete(message.from_id)
    else:
        try:
            series_num = int(message.text)
            series_num -= 1
            if (series_num < 0): 
                await message.answer("Попробуйте еще раз", keyboard=CANCEL_KEYBOARD)
            series_name = message.state_peer.payload["series_name"]
            res = requests.get("http://" + SERIES_IP + "/rest/unsubscribe?id=" + str(message.from_id) + "&name=" + series_name + "&vk=true&num=" + str(series_num))
            if res.text == "Repeat bleat":
                await message.answer("Попробуйте еще раз", keyboard=CANCEL_KEYBOARD)
            elif res.text == "Unsubscribed":
                await message.answer(series_name + " - Вы отписались от сериала", keyboard=MENU_KEYBOARD)
                await bot.state_dispenser.delete(message.from_id)
            elif res.text == "Already unsubscribed":
                await message.answer(series_name + " - Вы не были подписаны на этот сериал", keyboard=MENU_KEYBOARD)
                await bot.state_dispenser.delete(message.from_id)
        except:
            await message.answer("Попробуйте еще раз", keyboard=CANCEL_KEYBOARD)
