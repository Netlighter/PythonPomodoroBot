from telegram import ext

import app.settings
import app.entry_points


def run():
    bot_proxy_kwargs = {}
    if app.settings.PROXY_URL != '':
        bot_proxy_kwargs = {'proxy_url': app.settings.PROXY_URL}

    request_kwargs = {'connect_timeout': 60, 'read_timeout': 60}
    request_kwargs.update(bot_proxy_kwargs)
    updater = ext.Updater(app.settings.TOKEN, request_kwargs=request_kwargs)

    for handler in app.entry_points.handlers:
        updater.dispatcher.add_handler(handler)

    updater.start_polling()
    updater.idle()
