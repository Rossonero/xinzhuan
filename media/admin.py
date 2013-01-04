from django.contrib import admin
from .models import *

class MediumAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'sponsor')
    search_fields = ['name']
admin.site.register(Medium, MediumAdmin)
