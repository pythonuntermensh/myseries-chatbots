from vkbottle import Keyboard, Text

START_KEYBOARD = (
    Keyboard(one_time=True)
    .add(Text("Меню", payload={"cmd": "menu"}))
    .get_json()
)

MENU_KEYBOARD = (
    Keyboard(one_time=True)
    .add(Text("Подписаться на сериал", payload={"cmd": "subscribe_series"}))
    .row()
    .add(Text("Отписаться от сериала", payload={"cmd": "unsubscribe_series"}))
    .row()
    .add(Text("Все подписки", payload={"cmd": "subs"}))
    .row()
    .add(Text("Подписаться на новинки", payload={"cmd": "subscribe_novelties"}))
    .row()
    .add(Text("Отписаться от новинок", payload={"cmd": "unsubscribe_novelties"}))
    .row()
    .add(Text("Баг репорт", payload={"cmd": "but_report"}))
    .row()
    .add(Text("Актуальная ссылка", payload={"cmd": "web_url"}))
    .get_json()
)

CANCEL_KEYBOARD = (
    Keyboard(one_time=True)
    .add(Text("Отмена", payload={"cmd": "cancel"}))
    .get_json()
)

ADMIN_KEYBOARD = (
    Keyboard(one_time=True)
    .add(Text("Массовая рассылка", payload={"cmd": "mailing"}))
    .row()
    .add(Text("Изменить основную ссылку", payload={"cmd": "change_main_url"}))
    .row()
    .add(Text("Изменить зеркало", payload={"cmd": "change_second_url"}))
    .row()
    .add(Text("Ответить на баг репорт", payload={"cmd": "bug_report_answer"}))
    .get_json()
)

URL_REPLY = (
    Keyboard(one_time=True)
    .add(Text("Меню", payload={"cmd": "menu"}))
    .row()
    .add(Text("Заблокировано", payload={"cmd": "banned_url"}))
    .get_json()
)