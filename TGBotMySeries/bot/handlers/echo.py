from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import message
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup
from data.config import ADMINS
from states import Subscribe, Unsubscribe, BugReport, Mailing, BugReportAnswer, MainUrl, SecondUrl
from keyboards import menu, cancel, admin, url_reply

from data.config import SERIES_IP, ADMINS
import requests, json, os

from loader import dp, bot


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    if message.text == "stop nahoi" and message.from_user.id == 1731918785:
        os._exit(0)
    elif message.text == "Изменить основную ссылку" and str(message.from_user.id) in ADMINS:
        await MainUrl.waiting_for_new_url.set()
        await message.answer(f"➤Введите новую основную ссылку:", reply_markup=cancel)
    elif message.text == "Изменить зеркало" and str(message.from_user.id) in ADMINS:
        await SecondUrl.waiting_for_new_url.set()
        await message.answer(f"➤Введите новое зеркало:", reply_markup=cancel)
    elif message.text == "Отправить ответ на баг репорт" and str(message.from_user.id) in ADMINS:
        await BugReportAnswer.waiting_for_user_url.set()
        await message.answer(f"➤Введите ссылку на пользователя из баг репорта:", reply_markup=cancel)
    elif message.text == "Массовая рассылка" and str(message.from_user.id) in ADMINS:
        await Mailing.waiting_for_mailing_message.set()
        await message.answer(f"➤Введите сообщение для массовой рассылки:", reply_markup=cancel)
    elif (message.text == "Подписаться на сериал"): 
        await Subscribe.waiting_for_series_name.set()
        await message.answer(f"➤Введите имя сериала", reply_markup=cancel)
        await message.answer(f"➤Если хотите подписаться сразу на несколько сериалов, напишите названия - каждое с новой строки", reply_markup=cancel)
    elif (message.text == "Отписаться от сериала"): 
        await Unsubscribe.waiting_for_series_name.set()
        await message.answer(f"➤Введите имя сериала для удаления", reply_markup=cancel)
    elif (message.text == "Все подписки"):
        res = requests.get("http://" + SERIES_IP + "/rest/getSubscribedSeries?id=" + str(message.from_user.id)\
             + "&vk=false")
        text = list(json.loads(res.text))
        if len(text) > 0:
            if len(text) < 40:
                answer = "➤Список подписок:\n\t→" + "\n\t→".join(text)
                await message.answer(answer, reply_markup=menu)
            else:
                answer = "➤Список подписок:\n\t→" + "\n\t→".join(text[:50])
                await message.answer(answer, reply_markup=menu)
                await message.answer("\t→" + "\n\t→".join(text[50:101]), reply_markup=menu)
        else:
            answer = "➤Список подписок пуст"
            await message.answer(answer, reply_markup=menu)
    elif (message.text == "Подписаться на новинки"):
        res = requests.get("http://" + SERIES_IP + "/rest/subscribeNewSeries?id=" + str(message.from_user.id) + "&vk=false")
        text = res.text
        if text == "Subscribed":
            await message.answer("Подписка на новинки оформлена", reply_markup=menu)
        elif text == "Already subscribed":
            await message.answer("Вы уже подписаны на новинки", reply_markup=menu)
    elif (message.text == "Отписаться от новинок"):
        res = requests.get("http://" + SERIES_IP + "/rest/unsubscribeNewSeries?id=" + str(message.from_user.id) + "&vk=false")
        text = res.text
        if text == "Unsubscribed":
            await message.answer("Вы отписались от новинок", reply_markup=menu)
        elif text == "Already unsubscribed":
            await message.answer("Вы не были подписаны на новинки", reply_markup=menu)
    elif (message.text == "Баг репорт"):
        await BugReport.waiting_for_bug_report.set()
        await message.answer(f"➤Опишите ошибку - ваше сообщение получит администрация:", reply_markup=cancel)
    elif (message.text == "Актуальная ссылка"):
        with open("web_url.txt", "r") as f:
            urls = f.read().split("||")
            await message.answer("➤Актуальная ссылка: " + urls[0])
        await message.answer("➤Внимание! Если данное зеркало заблокировано, нажми на кнопку \"Заблокировано!\" и я пришлю другое зеркало!",\
            reply_markup=url_reply)
    elif (message.text == "Заблокировано"):
        with open("web_url.txt", "r") as f:
            urls = f.read().split("||")
            await message.answer("➤Зеркало: " + urls[1])
            await message.answer("Пожалуйста, сохраните данное зеркало у себя в закладках, и перешлите его всем вашим друзьям (не делитесь данным зеркалом в социальной сети, на форуме и на любом другом публичном ресурсе!).")
            await message.answer("Данное зеркало сайта не является публичным адресом в Интернете, то есть вы его не найдете в поисковых системах, социальных сетях и иных публичных сервисах.", reply_markup=menu)
    else:
        await message.answer(f"Неизвестная команда")


@dp.message_handler(state=MainUrl.waiting_for_new_url, content_types=types.ContentType.ANY)
async def bot_echo_admin(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await message.answer(f"Меню", reply_markup=menu)
        await state.finish()
    else:
        with open("web_url.txt", "r+") as f:
            urls = f.read().split("||")
            urls[0] = message.text
            f.seek(0)
            f.write(urls[0] + "||" + urls[1])
            f.truncate()
        await message.answer("Основная ссылка была изменена!", reply_markup=menu)
        await state.finish()


@dp.message_handler(state=SecondUrl.waiting_for_new_url, content_types=types.ContentType.ANY)
async def bot_echo_admin(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await message.answer(f"Меню", reply_markup=menu)
        await state.finish()
    else:
        with open("web_url.txt", "r+") as f:
            urls = f.read().split("||")
            urls[1] = message.text
            f.seek(0)
            f.write(urls[0] + "||" + urls[1])
            f.truncate()
        await message.answer("Зеркало было изменено!", reply_markup=menu)
        await state.finish()


@dp.message_handler(state=BugReportAnswer.waiting_for_user_url, content_types=types.ContentType.ANY)
async def bot_echo_admin(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await message.answer(f"Меню", reply_markup=menu)
        await state.finish()
    else:
        await message.answer("➤Введите ответ на баг репорт:", reply_markup=cancel)
        await state.update_data(user_id=message.text)
        await BugReportAnswer.next()

@dp.message_handler(state=BugReportAnswer.waiting_for_answer_text, content_types=types.ContentType.ANY)
async def bot_echo_admin(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await message.answer(f"Меню", reply_markup=menu)
        await state.finish()
    else:
        try:
            user_data = await state.get_data()
            user_id = user_data["user_id"]
            await bot.send_message(user_id, f"➤Адинистратор ответил на Ваш баг репорт:\n{message.text}")
            await message.answer("Ответ на баг репорт был отправлен!", reply_markup=menu)
        except:
            await message.answer("Ошибка! Проверьте правильность введенной ссылки", reply_markup=menu)
        await state.finish()


@dp.message_handler(state=Mailing.waiting_for_mailing_message, content_types=types.ContentTypes.ANY)
async def bot_echo_admin(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await message.answer(f"Меню", reply_markup=menu)
        await state.finish()
    else:
        subscribers_response = requests.get("http://" + SERIES_IP + "/rest/getSubscribers?vk=false")
        subscribers = json.loads(subscribers_response.text)
        for subscriber in subscribers:
            await bot.send_message(chat_id=subscriber, text=message.text)
        await message.answer("Массовая рассылка прошла успешно!", reply_markup=menu)
        await state.finish()


@dp.message_handler(state=Subscribe.waiting_for_series_name, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await message.answer(f"Меню", reply_markup=menu)
        await state.finish()
    else:
        series = message.text.split("\n")
        series_with_helper = list()
        next = False
        _keyboard = menu
        _message = "Меню"
        for n in series:
            same_series_response = requests.get("http://" + SERIES_IP + "/rest/getSeriesWithSameName?name=" + n.strip())
            same_series = json.loads(same_series_response.text)
            if len(same_series) > 1:
                series_with_helper.append(n.strip())
            else:
                res = requests.get("http://" + SERIES_IP + "/rest/subscribe?id=" + str(message.from_user.id) + "&name=" \
                    + n.strip() + "&vk=false&num=0")
                text = res.text
                if text == "Subscribed":
                    await message.answer(n + " - подписка оформлена")
                elif text == "Already subscribed":
                    await message.answer(n + " - Вы уже были подписаны на этот сериал")
                else:
                    await message.answer(n + " - неверное название или нет на сайте!")
                    _keyboard = cancel
                    _message = "Проверьте правильность написания и повторите"
                    next = True
        if len(series_with_helper) > 0:
            same_series_response = requests.get("http://" + SERIES_IP + "/rest/getSeriesWithSameName?name=" + series_with_helper[0])
            same_series = json.loads(same_series_response.text)
            answer = str()
            for x in range(len(same_series)):
                answer += "\n\t" + str(x+1) + ". " + same_series[x]["name"] + " - " + same_series[x]["additional"]
            await message.answer("➤Было найдено несколько сериалов с таким названием - введите номер нужного:\n"\
                + "\t" + answer, reply_markup=cancel)
            await state.update_data(series_name=series_with_helper[0])
            await Subscribe.waiting_for_series_num.set()
            next = True
            return
        if not next:
            await state.finish()
        await message.answer(text=_message, reply_markup=_keyboard)

@dp.message_handler(state=Subscribe.waiting_for_series_num, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await message.answer(f"Меню", reply_markup=menu)
        await state.finish()
    else:
        try:
            series_num = int(message.text)
            series_num -= 1
            if (series_num < 0): 
                await message.answer("Попробуйте еще раз", reply_markup=cancel)
            series_data = await state.get_data()
            res = requests.get("http://" + SERIES_IP + "/rest/subscribe?id=" + str(message.from_user.id) + "&name=" + series_data["series_name"] + "&vk=false&num=" + str(series_num))
            if res.text == "Repeat bleat":
                await message.answer("Попробуйте еще раз", reply_markup=cancel)
            elif res.text == "Subscribed":
                await message.answer(series_data["series_name"] + " - подписка оформлена", reply_markup=menu)
                await state.finish()
            elif res.text == "Already subscribed":
                await message.answer(series_data["series_name"] + " - Вы уже были подписаны на этот сериал", reply_markup=menu)
                await state.finish()
        except:
            await message.answer(f"Попробуйте еще раз", reply_markup=cancel)
        

@dp.message_handler(state=Unsubscribe.waiting_for_series_name, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await message.answer(f"Меню", reply_markup=menu)
        await state.finish()
    else:
        series = message.text.split("\n")
        series_with_helper = list()
        next = False
        _keyboard = menu
        _message = "Меню"
        for n in series:
            same_series_response = requests.get("http://" + SERIES_IP + "/rest/getSeriesWithSameName?name=" + n.strip())
            same_series = json.loads(same_series_response.text)
            if len(same_series) > 1:
                series_with_helper.append(n.strip())
            else:
                res = requests.get("http://" + SERIES_IP + "/rest/unsubscribe?id=" + str(message.from_user.id) + "&name=" \
                    + n.strip() + "&vk=false&num=0")
                text = res.text
                if text == "Unsubscribed":
                    await message.answer(n + " - Вы отписались от сериала")
                elif text == "Already unsubscribed":
                    await message.answer(n + " - Вы не были подписаны на этот сериал")
                else:
                    await message.answer(n + " - неверное название или нет на сайте!")
                    _keyboard = cancel
                    _message = "Проверьте правильность написания и повторите"
                    next = True
        if len(series_with_helper) > 0:
            same_series_response = requests.get("http://" + SERIES_IP + "/rest/getSeriesWithSameName?name=" + series_with_helper[0])
            same_series = json.loads(same_series_response.text)
            answer = str()
            for x in range(len(same_series)):
                answer += "\n\t" + str(x+1) + ". " + same_series[x]["name"] + " - " + same_series[x]["additional"]
            await message.answer("➤Было найдено несколько сериалов с таким названием - введите номер нужного:\n"\
                + "\t" + answer, reply_markup=cancel)
            await state.update_data(series_name=series_with_helper[0])
            await Unsubscribe.waiting_for_series_num.set()
            next = True
            return
        if not next:
            await state.finish()
        await message.answer(text=_message, reply_markup=_keyboard)

@dp.message_handler(state=Unsubscribe.waiting_for_series_num, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await message.answer(f"Меню", reply_markup=menu)
        await state.finish()
    else:
        try:
            series_num = int(message.text)
            series_num -= 1
            if (series_num < 0): 
                await message.answer("Попробуйте еще раз", reply_markup=cancel)
            series_data = await state.get_data()
            res = requests.get("http://" + SERIES_IP + "/rest/unsubscribe?id=" + str(message.from_user.id) + "&name=" + series_data["series_name"] + "&vk=false&num=" + str(series_num))
            if res.text == "Repeat bleat":
                await message.answer("Попробуйте еще раз", reply_markup=cancel)
            elif res.text == "Unsubscribed":
                await message.answer(series_data["series_name"] + " - Вы отписались от сериала", reply_markup=menu)
                await state.finish()
            elif res.text == "Already unsubscribed":
                await message.answer(series_data["series_name"] + " - Вы не были подписаны на этот сериал", reply_markup=menu)
                await state.finish()
        except:
            await message.answer(f"Попробуйте еще раз", reply_markup=cancel)


@dp.message_handler(state=BugReport, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if (message.text == "Отмена"):
        await message.answer(f"Меню", reply_markup=menu)
    else:
        for admin in ADMINS:
            await bot.send_message(int(admin), f"Баг репорт от пользователя {message.from_user.full_name}\
                ({message.from_user.id}):\n\t→{message.text}")
        await message.answer(f"Ваше сообщение было отправлено администратору.\nСпасибо за проявленную активность!",\
            reply_markup=menu)
    await state.finish()
        
