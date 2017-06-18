from django.conf.urls import url
from tournament.views import index

urlpatterns = [
    url(r'^$', index, name='homepage'),
]