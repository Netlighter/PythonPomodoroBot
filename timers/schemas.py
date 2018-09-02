from datetime import datetime, timedelta

import mongoengine

import users.schemas


class Interval(mongoengine.Document):
    created_at = mongoengine.fields.DateTimeField(default=datetime.utcnow)
    value = mongoengine.fields.IntField(required=True, min_value=0)
    position = mongoengine.fields.IntField(required=True, min_value=0)

    def run(self):
        raise NotImplementedError

    def as_timedelta(self):
        return timedelta(minutes=self.interval)


class Schedule(mongoengine.Document):
    created_at = mongoengine.fields.DateTimeField(default=datetime.utcnow)
    name = mongoengine.StringField(default='-')
    user = mongoengine.fields.LazyReferenceField(users.schemas.User)
    intervals = mongoengine.fields.ListField(
        field=mongoengine.fields.LazyReferenceField(Interval))
    last_interval = mongoengine.fields.ReferenceField(Interval)

    def get_interval_next_position(self):
        if self.last_interval is None:
            return 0
        else:
            return self.last_interval.position + 1

    def add_interval(self, value: timedelta):
        interval = Interval(
            value=value.seconds // 3600,
            position=self.get_interval_next_position())
        interval.save()

        Schedule.objects(pk=self.pk).update_one(push__intervals=interval)
        self.last_interval = interval
        self.save()

    def run_last_interval(self):
        self.last_interval.run()
