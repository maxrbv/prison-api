from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=64, null=True)
    cigarettes = fields.BigIntField(default=0)
    next_usage = fields.DatetimeField(null=True)
