# Create your tasks here

from celery import shared_task


@shared_task
def checkplayers():
    from .models import Player
    # from otree.models import Participant
    # print(Participant.objects.all().values('code'))
    print(Player.objects.all())
