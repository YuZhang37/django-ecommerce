from django.contrib import admin

from tags.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['label']
    search_fields = ['label']



# admin.site.register(Tag)
