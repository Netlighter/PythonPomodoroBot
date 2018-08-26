import mongoengine.errors

from users.schemas import User
import app.interfaces


class SendChooseActionMsg(app.interfaces.RegexHandler):
    reply_text = 'Выберите действие:'

    def callback(self, bot, update):
        pass


class SendReturnToMainMenuBtn(SendChooseActionMsg):
    RETURN_TO_MENU_BTN = 'Вернуться в меню'

    def get_markup_keyboard(self):
        return [
            [self.RETURN_TO_MENU_BTN],
        ]


class NotImplemented(SendReturnToMainMenuBtn):
    reply_text = 'Ого! Кажется эта функция еще в разработке!'


class Menu(SendChooseActionMsg):
    TIMERS_BTN = 'Таймеры'
    RUN_LAST_TIMER_BTN = 'Запустить последний таймер'

    def get_markup_keyboard(self):
        return [
            [self.TIMERS_BTN],
            [self.RUN_LAST_TIMER_BTN],
        ]


class Start(Menu):
    def callback(self, bot, update):
        try:
            User.objects.create(telegram_id=self.user.id)
        except mongoengine.errors.NotUniqueError:
            pass

    def get_reply_text(self):
        return f'Привет, {self.user.username}!\nДавай сразу приступим.'


class WrongInput(app.interfaces.RegexHandler):
    reply_text = 'Я ничего не понимаю.'

    def callback(self, bot, update):
        pass
