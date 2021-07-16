from django.contrib import admin

from apis.models.Word import *
from apis.models.Voice import *
from apis.models.Category import *


class ForId(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Word, ForId)
admin.site.register(Voice, ForId)
admin.site.register(Category, ForId)