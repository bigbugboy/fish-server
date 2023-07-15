import time

from tortoise import fields
from tortoise.models import Model


class BaseModel(Model):
    class Meta:
        abstract = True

    def to_dict(self):
        return {
            field: getattr(self, field)
            for field in self._meta.fields
            if hasattr(self, field)
        }


class SingleChoice(BaseModel):
    help_text = "单选题"

    id = fields.IntField(pk=True)
    question = fields.CharField(max_length=1000, description="题目")
    choice_a = fields.CharField(max_length=256, description="A选项")
    choice_b = fields.CharField(max_length=256, description="B选项")
    choice_c = fields.CharField(max_length=256, description="C选项")
    choice_d = fields.CharField(max_length=256, description="D选项")
    choice_right = fields.CharField(max_length=1, description="正确选项")
    desc = fields.TextField(description="解析")
    created_at = fields.IntField(default=time.time)
    updated_at = fields.IntField(default=time.time)
    status = fields.BooleanField(default=1, description="0表示删除")
    level_id = fields.SmallIntField(null=True, description="难度等级id")
    category_id = fields.IntField(null=True, description="知识点类型id")


class Level(BaseModel):
    help_text = "难度等级"

    id = fields.IntField(pk=True)
    name = fields.SmallIntField(unique=True)


class Category(BaseModel):
    help_text = "知识点类型"

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=20, unique=True)


class AdminUser(BaseModel):
    help_text = "后台用户表"

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    password = fields.CharField(max_length=20)
