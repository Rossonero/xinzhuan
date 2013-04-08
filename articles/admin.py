from django.contrib import admin
from .models import *

class HotWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'english', 'monthly_frequency')
    search_fields = ['word']

admin.site.register(HotWord, HotWordAdmin)
