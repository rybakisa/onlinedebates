from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .models import *


@login_required
def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")

    # Render that in the index template
    return render(request, "index.html", {
        "rooms": rooms,
    })


class MainPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):

        context = super(MainPage, self).get_context_data(**kwargs)

        tournament = None   #просто текущий турнир
        current_user = None
        current_team = None
        rounds = None       #выбрать все и отсортировать по номеру, ставить последний акетивным
        current_round_number = None #как вариант, в темплейте сравнивать каждый с текущим
        messages = None     #выбрать сообщения судей и сообщения участников в один запрос и отсортировать по времени
        tab = None          #сформировать QuerySet с тэбом

        tournament = Tournament.objects.get(current=True)
        #
        #
        rounds = Round.objects.all().order_by('number')
        current_round_number = rounds[-1].number
        messages = ChatMessage.objects.all().order_by('time')
        #

        context['tournament'] = tournament
        context['current_user'] = current_user
        context['current_team'] = current_team
        context['rounds'] = rounds
        context['current_round_number'] = current_round_number
        context['messages'] = messages
        context['tab'] = tab












