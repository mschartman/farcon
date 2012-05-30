from session_manager.models import Session
from django.contrib import admin

class SessionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['label']}),
        (None, {'fields': ['owner']}),
        (None, {'fields': ['hostname']}),
        ('Authentication', {'fields': ['username', 'password']}),
    ]

admin.site.register(Session, SessionAdmin)
