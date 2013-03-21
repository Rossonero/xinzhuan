from django.contrib import admin
from .models import Area
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'en', 'parent_id', 'summary')
    search_fields = ['name']

admin.site.register(Area, AreaAdmin)
