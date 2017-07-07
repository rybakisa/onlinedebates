from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView, RedirectView, FormView
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.http import is_safe_url
from django.db import connection
from django.http import Http404, HttpResponseRedirect, HttpResponse

from .queries import TAB_QUERY

from .models import *


class MainPage(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    success_url = '/'
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'index.html'

    def calculate_page_status(self, current_user, current_team, current_round, current_user_rooms):

        status = None
        results = Result.objects.filter(team=current_team, room__round=current_round)
        feedbacks = Feedback.objects.filter(player=current_user, room__round=current_round)

        # если нет ни одного рума -- waiting_for_round
        if len(current_user_rooms) == 0:
            status = 'waiting_for_round'

        # если текущий раунд с результатами и фидбэками -- waiting_for_round
        elif results.count() != 0 and feedbacks.count() != 0:
            status = 'waiting_for_round'

        # если текущий раунд без результатов результатов -- preparing
        elif results.count() == 0:
            status = 'preparing'

        # есть результаты, нет фидбэка -- waiting_for_feedback
        elif results.count() != 0 and feedbacks.count() == 0:
            status = 'waiting_for_feedback'

        return status

    def get_context_data(self, **kwargs):

        context = super(MainPage, self).get_context_data(**kwargs)

        tournament = None   #просто текущий турнир
        current_user = None
        current_team = None
        current_user_rooms = None
        rounds = None       #выбрать все и отсортировать по номеру, ставить последний акетивным
        current_round = None #как вариант, в темплейте сравнивать каждый с текущим
        messages = None     #выбрать сообщения судей и сообщения участников в один запрос и отсортировать по времени
        tab = None          #сформировать QuerySet с тэбом
        kurilki = None
        page_status = None
        next_round_start_time = None

        tournament = Tournament.objects.get(current=True)
        current_round = tournament.current_round
        current_user = Player.objects.get(user=self.request.user)
        current_team = current_user.team
        current_user_rooms = Room.objects.filter(result__team=current_team).order_by('round__number', 'result__position')
        messages = ChatMessage.objects.all().order_by('time')
        kurilki = Kurilka.objects.all()
        page_status = self.calculate_page_status(current_user, current_team, current_round, current_user_rooms)

        # next_round_start_time
        next_round = Round.objects.get(number=current_round.number+1)
        next_round_start_time = next_round.start_time

        # tab
        cursor = connection.cursor()
        cursor.execute(TAB_QUERY)
        tab = cursor.fetchall()

        context['tournament'] = tournament
        context['page_status'] = page_status
        context['next_round_start_time'] = next_round_start_time
        context['current_user'] = current_user
        context['current_team'] = current_team
        context['current_user_rooms'] = current_user_rooms
        # context['rounds'] = rounds
        # context['current_round_number'] = current_round_number
        context['messages'] = messages
        context['kurilki'] = kurilki
        context['tab'] = tab

        return context


class LoginView(FormView):
    success_url = '/'
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'login.html'


    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class LogoutView(RedirectView):
    url = '/login/'
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)











