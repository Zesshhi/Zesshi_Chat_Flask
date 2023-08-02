import os

from decouple import config

current_path = os.path.dirname(os.path.realpath(__file__))

# DB Mock
rooms = {}


class Config:
    DEBUG = True
    SECRET_KEY = config('SECRET_KEY')
