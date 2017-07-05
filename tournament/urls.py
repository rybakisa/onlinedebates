from django.conf.urls import url
from tournament.views import MainPage, LoginView, LogoutView

urlpatterns = [
    url(r'^$', MainPage.as_view(), name='mainpage'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
]