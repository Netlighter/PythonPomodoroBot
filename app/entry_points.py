from telegram import ext

import app.handlers


handlers = [
    ext.RegexHandler(r'/start', app.handlers.start),
]
