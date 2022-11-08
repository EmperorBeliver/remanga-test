from django.contrib import admin
from .models import *
# Register your models here.

class TitleAdmin(admin.ModelAdmin):
    search_fields = ['rus_name', 'eng_name', 'other_name']

class VolumeAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register([TagModel, ChapterModel])
admin.site.register(TitleModel, TitleAdmin)
admin.site.register(VolumeModel, VolumeAdmin)