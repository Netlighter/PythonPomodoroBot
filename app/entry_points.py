import app.handlers


handlers = [
    app.handlers.Start(r'/start'),
    app.handlers.Menu(app.handlers.Menu.RETURN_TO_MENU_BTN),
    app.handlers.RunLastTimer(app.handlers.Start.START_LAST_TIMER_BTN),
    app.handlers.Timers(app.handlers.Start.TIMERS_BTN),
    # All handlers below following will be ignored.
    app.handlers.WrongInput(r'.*'),
]
