import app.handlers
import timers.handlers


handlers = [
    app.handlers.Start(r'/start'),
    app.handlers.Menu(app.handlers.SendReturnToMainMenuBtn.RETURN_TO_MENU_BTN),
    timers.handlers.RunLastTimer(app.handlers.Start.RUN_LAST_TIMER_BTN),
    timers.handlers.Schedules(app.handlers.Start.TIMERS_BTN),
    timers.handlers.SendAddScheduleMsg(
        timers.handlers.ScheduleMenu.ADD_TIMER_BTN),
    timers.handlers.AddSchedule(r'.*', pass_user_data=True),
    timers.handlers.AddInterval(r'.*', pass_user_data=True),
    # All handlers below following will be ignored.
    app.handlers.WrongInput(r'.*'),
]
