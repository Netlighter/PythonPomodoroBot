from datetime import datetime

import mongoengine

import schemas.users


class Timer(mongoengine.Document):
    created_at = mongoengine.fields.DateTimeField(default=datetime.utcnow)
    user = mongoengine.fields.LazyReferenceField(schemas.users.User)
    interval = mongoengine.fields.IntField(min_value=0)
    next_timer = mongoengine.fields.ReferenceField('self', null=True)
