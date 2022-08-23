from vkbottle import BaseStateGroup

class SubscribeState(BaseStateGroup):
    WAITING_FOR_SERIES_NAME = 0
    WAITING_FOR_SERIES_NUM = 1