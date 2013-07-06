#!/usr/bin/env python
# coding: utf-8

from mongoengine import *

class Weather(Document):
    point = StringField()
    date = DateTimeField()
    temperature = FloatField()
    humidity = FloatField()
    pressure = FloatField()
    wind_direction = StringField()
    wind_speed = FloatField()
    rainfall = FloatField()

