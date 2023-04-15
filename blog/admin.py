from django.contrib import admin

from .models import Album, Spotlight
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
