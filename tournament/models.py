import json
from django.db import models
from django.utils.six import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.dispatch import receiver

from channels import Group

# TODO: refactor msg types
from .settings import MSG_TYPE_MESSAGE

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
    current_round = models.ForeignKey('Round', on_delete=models.DO_NOTHING, default=None, blank=True)
    current = models.BooleanField(default=False)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Team(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# TODO: 1-1 link on django accounts
@python_2_unicode_compatible
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='players', blank=True)
    name = models.CharField(max_length=255)
    type = models.IntegerField(choices=USERTYPE_CHOICES)   # judje or player or admin
    vk = models.URLField(blank=True)
    feedbacks = models.ManyToManyField('Player', through='Feedback')

    def __str__(self):
        return self.name


# @python_2_unicode_compatible
# class Judge(models.Model):
#     tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='judges')
#     name = models.CharField(max_length=255)
#     vk = models.URLField()
#
#
#     def __str__(self):
#         return self.name.encode('utf-8')


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

    def __str__(self):
        return str(ROUNDTYPE_CHOICES[self.type-1][1]) + ' ' + str(self.number)

    #TODO: переопределить save, чтобы проверял (если изменение начала раунда произошло и это текущий раунд, то кидать событыие в веб-сокет)
    #TODO: при создании раунда автоматически делать его текущим

# TODO: change sent message logic
@python_2_unicode_compatible
class Room(models.Model):
    # Room title
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='rooms')
    title = models.CharField(max_length=255)
    chair = models.ForeignKey(Player, on_delete=models.CASCADE)
    hangout_link = models.URLField()
    # OG = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='OGs')
    # OG_place = models.IntegerField(default=0)
    # OO = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='OOs')
    # OO_place = models.IntegerField(default=0)
    # CG = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='CGs')
    # CG_place = models.IntegerField(default=0)
    # CO = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='COs')
    # CO_place = models.IntegerField(default=0)

    def __str__(self):
        return self.title + ' | ' + str(self.round)

    # @property
    # def websocket_group(self):
    #     """
    #     Returns the Channels Group that sockets should subscribe to to get sent
    #     messages as they are generated
    #     """
    #     return Group("room-%s" % self.id)
    #
    # def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
    #     """
    #     Called to send a message to the room on behalf of a user.
    #     """
    #     final_msg = {'event': 'start_round', 'room': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type}
    #
    #     # Send out the message to everyone in the room
    #     self.websocket_group.send(
    #         {"text": json.dumps(final_msg)}
    #     )


# TODO: logic for team speaks
@python_2_unicode_compatible
class Result(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    position = models.IntegerField(default=0, choices=POSITION_CHOICES)
    score = models.IntegerField(default=-1)

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
    msg_from = models.ForeignKey(Player)
    time = models.DateTimeField(auto_now=True)
    text = models.TextField()


@python_2_unicode_compatible
class Kurilka(models.Model):
    name = models.CharField(max_length=100)
    link = models.URLField()

    def __str__(self):
        return self.name































