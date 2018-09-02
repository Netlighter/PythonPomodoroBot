from datetime import datetime

import mongoengine

import users.schemas


class Timer(mongoengine.Document):
    created_at = mongoengine.fields.DateTimeField(default=datetime.utcnow)
    user = mongoengine.fields.LazyReferenceField(users.schemas.User)
    interval = mongoengine.fields.IntField(min_value=0)
    next_timer = mongoengine.fields.ReferenceField('self', null=True)
