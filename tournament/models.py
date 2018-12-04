import json
from django.db import models
from django.utils.six import python_2_unicode_compatible
from django.contrib.auth.models import User
from channels import Group

USERTYPE_CHOICES = ((1, 'player'),
                    (2, 'judge'),
                    (3, 'admin'))

ROUNDTYPE_CHOICES = ((1, 'preliminary'),
                     (2, 'semifinal'),
                     (3, 'final'))

POSITION_CHOICES = ((1, 'OG'),
                    (2, 'OO'),
                    (3, 'CG'),
                    (4, 'CO'))


@python_2_unicode_compatible
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    tabmaker_link = models.URLField()
    translation_link = models.URLField()
    current = models.BooleanField(default=False)

    @property
    def current_round(self):
        try:
            self.rounds.get(current=True)
        except self.DoesNotExist:
            # TODO: logging
            return None
        except self.MultipleObjectsReturned:
            # TODO: logging
            return None

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Team(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=255)
    hangout_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


# TODO: 1-1 link on django accounts
@python_2_unicode_compatible
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='players', blank=True)
    name = models.CharField(max_length=255)
    type = models.IntegerField(choices=USERTYPE_CHOICES)
    vk = models.URLField(blank=True)
    feedbacks = models.ManyToManyField('Player', through='Feedback')

    def __str__(self):
        return self.name


# TODO: create choises for round type
# TODO: handle current round
@python_2_unicode_compatible
class Round(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='rounds')
    type = models.IntegerField(choices=ROUNDTYPE_CHOICES)
    start_time = models.DateTimeField()
    number = models.IntegerField()
    resolution = models.TextField()
    infoslide = models.TextField(blank=True)
    current = models.BooleanField(default=False)

    def __str__(self):
        return self.get_type_display() + ' ' + str(self.number)


@python_2_unicode_compatible
class Room(models.Model):
    # Room title
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='rooms')
    title = models.CharField(max_length=255)
    chair = models.ForeignKey(Player, on_delete=models.CASCADE)
    hangout_link = models.URLField()

    def __str__(self):
        return self.title + ' | ' + str(self.round)


# TODO: logic for team speaks
@python_2_unicode_compatible
class Result(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    position = models.IntegerField(default=0, choices=POSITION_CHOICES)
    score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.room) + ' | ' + str(self.team) + ' | ' + str(self.score)


@python_2_unicode_compatible
class Feedback(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='fb_rooms')
    judge = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='fb_judges')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='fb_players')
    # TODO: feedback structure


@python_2_unicode_compatible
class ChatMessage(models.Model):
    msg_from = models.ForeignKey(Player, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    text = models.TextField()


@python_2_unicode_compatible
class Kurilka(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField()

    def __str__(self):
        return self.name


def send_start_round_notification(sender, instance, created, **kwargs):
    if instance.current_round:
        # send event to websocket
        data = {'text': json.dumps({'event': 'start_round'})}
        Group('chat-1').send(data)


models.signals.post_save.connect(send_start_round_notification, sender=Tournament)
