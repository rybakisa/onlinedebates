from django.contrib import admin
from .models import *

admin.site.register(Tournament)
admin.site.register(Round)
admin.site.register(Room)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(ChatMessage)
admin.site.register(Result)
admin.site.register(Feedback)