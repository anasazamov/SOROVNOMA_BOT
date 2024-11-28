from django.contrib import admin
from .models import BotAdmin, Bot, REQUIRED_CHANNELS, Question, Options, Voter

# Register your models here.

admin.site.register(BotAdmin)
admin.site.register(Bot)
admin.site.register(REQUIRED_CHANNELS)
admin.site.register(Question)
admin.site.register(Options)
admin.site.register(Voter)