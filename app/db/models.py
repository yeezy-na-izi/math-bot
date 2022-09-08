from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    telegram_id = fields.BigIntField()


class LogRecord(Model):
    id = fields.BigIntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="logs")
    command = fields.TextField()
    date = fields.DatetimeField(auto_now_add=True)
    info = fields.JSONField(null=True)
    fail = fields.BooleanField(default=False)
