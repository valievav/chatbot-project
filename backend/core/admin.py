from django.contrib import admin
from core import models

admin.site.register(models.Recipe)
admin.site.register(models.AiChatSession)
admin.site.register(models.AiRequest)
