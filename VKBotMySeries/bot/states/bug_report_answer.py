from vkbottle import BaseStateGroup

class BugReportAnswer(BaseStateGroup):
    WAITING_FOR_USER_URL = 0
    WAITING_FOR_ANSWER_MESSAGE = 1