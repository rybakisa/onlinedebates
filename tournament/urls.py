from django.conf.urls import url
from tournament.views import index, chat_view

urlpatterns = [
    url(r'^$', chat_view, name='homepage'),
]