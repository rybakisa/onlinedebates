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


def chat_view(request):
    return render(request, 'chat/index.html')


class MainPage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        pass
        # find current tournament
        # find all rounds
        # find current round
        # find room and results for every round to print tabs and tab
        # find logged in user
        # find command for than user
        # find all chat messages
        # find all feedbacks
        #













