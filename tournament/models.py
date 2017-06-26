import json
from django.db import models
from django.utils.six import python_2_unicode_compatible
from channels import Group

# TODO: refactor msg types
from .settings import MSG_TYPE_MESSAGE


@python_2_unicode_compatible
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    tabmaker_link = models.URLField()

    def __str__(self):
        return self.name.encode('utf-8')


@python_2_unicode_compatible
class Team(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name.encode('utf-8')


# TODO: 1-1 link on django accounts
@python_2_unicode_compatible
class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    name = models.CharField(max_length=255)
    # type = models.CharField(max_length=255)
    vk = models.URLField()

    def __str__(self):
        return self.name.encode('utf-8')

# TODO: 1-1 link on django accounts
@python_2_unicode_compatible
class Judge(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='judges')
    name = models.CharField(max_length=255)
    vk = models.URLField()
    feedbacks = models.ManyToManyField(Player, through='Feedback')

    def __str__(self):
        return self.name.encode('utf-8')


# TODO: create choises for round type
# TODO: handle current round
@python_2_unicode_compatible
class Round(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='rounds')
    type = models.CharField(max_length=10)
    number = models.IntegerField()
    resolution = models.TextField()
    infoslide = models.TextField(blank=True)


    def __str__(self):
        return self.type.encode('utf-8')


# TODO: change sent message logic
@python_2_unicode_compatible
class Room(models.Model):
    # Room title
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='rooms')
    title = models.CharField(max_length=255)
    chair = models.ForeignKey(Judge, on_delete=models.CASCADE)
    hangout_link = models.URLField()
    results = models.ManyToManyField(Player, through='Result')

    def __str__(self):
        return self.title.encode('utf-8')

    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get sent
        messages as they are generated
        """
        return Group("room-%s" % self.id)

    def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
        """
        Called to send a message to the room on behalf of a user.
        """
        final_msg = {'event': 'start_round', 'room': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type}

        # Send out the message to everyone in the room
        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )


# TODO: choises for place
# TODO: logic for team speaks
@python_2_unicode_compatible
class Result(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='players')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rooms')
    place = models.IntegerField()
    # score = models.IntegerField()


@python_2_unicode_compatible
class Feedback(models.Model):
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE, related_name='judges')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='players')
    # TODO: feedback structure




























