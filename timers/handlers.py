import app.handlers
import app.interfaces


class RunLastTimer(app.handlers.NotImplemented):
    pass


class Timers(app.handlers.NotImplemented):
    reply_text = 'Выберите таймер который хотите запустить:'
    markup_type = app.interfaces.RegexHandler.MarkupType.INLINE

    chained_handler = app.handlers.SendReturnToMainMenuBtn()

    def get_markup_keyboard(self):
        return [
            [dict(text='Таймер 1', callback_data='1')],
            [dict(text='Таймер 2', callback_data='2')],
            [dict(text='Таймер 3', callback_data='3')],
        ]
