import mongoengine.errors

from schemas.users import User


def start(bot, update):
    user_id = update.effective_message.from_user.id
    try:
        User.objects.create(telegram_id=user_id)
    except mongoengine.errors.NotUniqueError:
        pass
