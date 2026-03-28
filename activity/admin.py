from django.contrib import admin
from .models import ActivityLog, Notification


admin.site.register(ActivityLog)
admin.site.register(Notification)
