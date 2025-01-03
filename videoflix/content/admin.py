from django.contrib import admin
from .models import Video, VideoProgress
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.



class VideoResource(resources.ModelResource):

    class Meta:
        model = Video

class VideoAdmin(ImportExportModelAdmin):
    resource_classes = [VideoResource]

admin.site.register(Video, VideoAdmin)

class VideoProgressAdmin(admin.ModelAdmin):
    class Meta:
        model = VideoProgress

admin.site.register(VideoProgress, VideoProgressAdmin)
