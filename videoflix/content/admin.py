from django.contrib import admin
from .models import Video

# Register your models here.

# class VideoAdmin(admin.ModelAdmin):
#     list_display = ('title', 'id','due_date', 'priority', 'category', 'author', 'token')

#     search_fields = ('title', 'id','description', 'author__username', 'token')

#     list_filter = ('priority', 'id','category', 'due_date', 'author')

#     fields = ()

#     readonly_fields = ('created_at',)

admin.site.register(Video)
