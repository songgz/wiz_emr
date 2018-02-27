#!/usr/bin/python3
# -*- coding: utf-8 -*-
from peewee import *
db = SqliteDatabase('../wizemr.db')


class BaseModel(Model):
    class Meta:
        database = db


if __name__ == '__main__':
    print(db.connect())
