from django.db import models

# Create your models here.
import mongoengine


class User(mongoengine.Document):
    v_type = mongoengine.StringField(max_length=30)
    v_times = mongoengine.IntField(default=1, null=True)
    end_time = mongoengine.DateTimeField(null=True)

