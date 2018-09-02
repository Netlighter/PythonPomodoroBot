import app.handlers
import timers.handlers


handlers = [
    app.handlers.Start(r'/start'),
    app.handlers.Menu(app.handlers.SendReturnToMainMenuBtn.RETURN_TO_MENU_BTN),
    timers.handlers.RunLastTimer(app.handlers.Start.RUN_LAST_TIMER_BTN),
    timers.handlers.Timers(app.handlers.Start.TIMERS_BTN),
    # All handlers below following will be ignored.
    app.handlers.WrongInput(r'.*'),
]
