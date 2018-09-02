import re
import datetime

import app.handlers
import app.mixins
import app.interfaces

from timers.schemas import Schedule


# Run last schedule


# TODO: Rename all 'Timers' to 'Schedulers' or 'Intervals'
class RunLastTimer(app.handlers.NotImplemented):
    pass


# Schedules menu


class ScheduleMenu(app.handlers.SendReturnToMainMenuBtn):
    ADD_TIMER_BTN = 'Добавить таймер'

    reply_text = '...или выберите действие:'

    def get_markup_keyboard(self):
        return [
            [self.ADD_TIMER_BTN],
            [self.RETURN_TO_MENU_BTN],
        ]


class Schedules(app.handlers.NotImplemented):
    reply_text = 'Выберите таймер который хотите запустить:'
    markup_type = app.interfaces.RegexHandler.MarkupType.INLINE

    chained_handler = ScheduleMenu()

    def get_markup_keyboard(self):
        schedule_objects = Schedule.objects.filter(user=self.user.id)
        schedules = list(
            dict(text=o.name, callback_data=f'{o.pk}')
            for o in schedule_objects)

        return [[s] for s in schedules]


class SendAddScheduleMsg(app.handlers.SendReturnToMainMenuBtn):
    STATE = 'SendAddScheduleMsg'
    reply_text = 'Введите название помидора:'

    def callback(self, *args, **kwargs):
        return self.STATE


class AddSchedule(
    app.mixins.RequiredStateMixin,
    app.handlers.SendReturnToMainMenuBtn,
):
    REQUIRED_STATE = SendAddScheduleMsg.STATE

    def get_reply_text(self):
        return AddInterval.reply_text

    def callback(self, *args, user_data, **kwargs):
        user_data['schedule'] = Schedule.objects.create(
            name=self.message.text,
            user=self.user.id)
        return AddInterval.STATE


class AddInterval(
    app.mixins.RequiredStateMixin,
    app.handlers.SendReturnToMainMenuBtn,
):
    STATE = 'AddInterval'
    REQUIRED_STATE = STATE

    TIME_UNITS = {
        'm': 'minutes',
        'h': 'hours'
    }

    WRONG_INPUT_MSG = (
        'Вы ввели не правильное значение! Интервал должен быть представлен в '
        'виде челого числа и символа единицы измерения, например: 15m, 30m')

    reply_text = 'Введите интервал:'

    def parse_user_input_to_timedelta(self):
        time_unit_shortcuts = self.TIME_UNITS.keys()
        msg_text = self.message.text

        if ' ' in msg_text:
            number_str, unit = msg_text.split(' ')
        else:
            # re.split have special logic for capture groups:
            # https://stackoverflow.com/a/2136580
            number_str, unit, *garbage = re.split(r'(\D+)', msg_text)

        if unit not in time_unit_shortcuts:
            raise ValueError('Wrong unit format')

        number = int(number_str)

        interval_timedelta = datetime.timedelta(
            **{self.TIME_UNITS[unit]: number})

        return interval_timedelta

    def callback(self, *args, user_data, **kwargs):
        try:
            interval = self.parse_user_input_to_timedelta()
            user_data['schedule'].add_interval(value=interval)
        except ValueError:
            pass

        return self.KEEP_CURRENT_STATE

    def get_reply_text(self):
        try:
            # Too lazy to create input validation.
            self.parse_user_input_to_timedelta()
            return self.reply_text
        except ValueError:
            return self.WRONG_INPUT_MSG
