from django.contrib import admin
from .models import *

class JournalistAdmin(admin.ModelAdmin):
    list_display = ('name', 'newspaper_name')
    search_fields = ['name', 'medium__name']

admin.site.register(Journalist, JournalistAdmin)
