from django.contrib import admin

from . import models


admin.site.register(models.Profile)
admin.site.register(models.Composition)
admin.site.register(models.ChatMessage)
admin.site.register(models.Comment)
admin.site.register(models.Notification)
