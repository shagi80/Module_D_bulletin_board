""" конфигурация адмиистрирования моделей приложения Объявления """
from django.contrib import admin
from .models import Advert, Comment


class AdvertAdmin(admin.ModelAdmin):
    """ класс администрирования Объявлеий """
    list_display = ('id', 'category', 'title')
    list_display_links = ('id', 'title')
    list_filter = ('category', )
    search_fields = ('title', )


class CommentAdmin(admin.ModelAdmin):
    """ класс администрирования Комментариев """
    list_display = ('id', 'author', 'advert', 'accepted')
    list_display_links = ('id', 'advert')
    list_filter = ('author', )
    search_fields = ('text', 'advert')


admin.site.register(Advert, AdvertAdmin)
admin.site.register(Comment, CommentAdmin)