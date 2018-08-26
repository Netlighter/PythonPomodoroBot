import mongoengine.errors

from schemas.users import User
import app.interfaces


class NotImplemented(app.interfaces.RegexHandler):
    reply_text = 'Ого! Кажется эта функция еще в разработке!'

    def callback(self, bot, update):
        pass

    def get_markup_keyboard(self):
        return [
            [Menu.RETURN_TO_MENU_BTN],
        ]


class Menu(app.interfaces.RegexHandler):
    TIMERS_BTN = 'Таймеры'
    START_LAST_TIMER_BTN = 'Запустить последний таймер'
    RETURN_TO_MENU_BTN = 'Вернуться в меню'

    reply_text = 'Выберите действие'

    def callback(self, bot, update):
        pass

    def get_markup_keyboard(self):
        return [
            [self.TIMERS_BTN],
            [self.START_LAST_TIMER_BTN],
        ]


class Start(Menu):
    def callback(self, bot, update):
        try:
            User.objects.create(telegram_id=self.user.id)
        except mongoengine.errors.NotUniqueError:
            pass

    def get_reply_text(self):
        return f'Привет, {self.user.username}!\nДавай сразу приступим.'


class RunLastTimer(NotImplemented):
    pass


class Timers(NotImplemented):
    pass


class WrongInput(app.interfaces.RegexHandler):
    reply_text = 'Я ничего не понимаю.'

    def callback(self, bot, update):
        pass
