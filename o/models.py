from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
from .tasks import checkplayers

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'o'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        print('BEFORE RUNNING TASK')
        checkplayers.delay()
        print('AFTER RUNNING TASK')


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
