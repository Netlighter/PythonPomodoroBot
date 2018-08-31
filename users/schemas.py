import mongoengine


class User(mongoengine.Document):
    telegram_id = mongoengine.IntField(
        primary_key=True,
        required=True)
