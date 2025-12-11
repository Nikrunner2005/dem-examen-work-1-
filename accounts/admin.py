from django.contrib import admin
from .models import CourseRequest

@admin.register(CourseRequest)
class CourseRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "date_start", "status", "created_at")
    list_filter = ("status", "course")
    search_fields = ("user__username",)
    list_editable = ("status",)  # позволяет менять статус прямо из списка
