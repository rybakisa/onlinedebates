from django.conf.urls import url
from tournament.views import MainPage

urlpatterns = [
    url(r'^$', MainPage.as_view(), name='mainpage'),
]