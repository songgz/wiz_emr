#!/usr/bin/python3
# -*- coding: utf-8 -*-
from peewee import *
db = SqliteDatabase('../wizemr.db')


class BaseModel(Model):
    class Meta:
        database = db


class Drug(BaseModel):
    id = IntegerField()
    name = CharField()
    pinyin = CharField()


if __name__ == '__main__':
    print(db.connect())
    d = Drug.select()[0]
    print(getattr(d, 'name'))

