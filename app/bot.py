from telegram.ext import Updater, CommandHandler

import app.settings


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def run():
    bot_proxy_kwargs = {}
    if app.settings.PROXY_URL != '':
        bot_proxy_kwargs = {'proxy_url': app.settings.PROXY_URL}

    request_kwargs = {'connect_timeout': 60, 'read_timeout': 60}
    request_kwargs.update(bot_proxy_kwargs)
    updater = Updater(app.settings.TOKEN, request_kwargs=request_kwargs)

    updater.dispatcher.add_handler(CommandHandler('hello', hello))

    updater.start_polling()
    updater.idle()
