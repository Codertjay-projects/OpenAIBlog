from django.contrib import admin

from .models import Album, Spotlight, HighLight
from .models import Post


class SpotlightInline(admin.StackedInline):
    model = Spotlight
    extra = 1


class AlbumAdmin(admin.ModelAdmin):
    inlines = [SpotlightInline]


admin.site.register(Album, AlbumAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'timestamp')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Post, PostAdmin)


@admin.register(HighLight)
class HighLightAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('name', 'description')
