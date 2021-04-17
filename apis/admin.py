from django.contrib import admin
from .models import Word, Voice, Category

class ForId(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Word, ForId)
admin.site.register(Voice, ForId)
admin.site.register(Category, ForId)