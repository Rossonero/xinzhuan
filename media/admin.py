from django.contrib import admin
from .models import *

class MediumAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'english_name', 'sponsor', 'introduction')
    search_fields = ['name']
admin.site.register(Medium, MediumAdmin)
