from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "name", "age", "phone", "email", "date_registered")
    search_fields = ("student_id", "name", "email", "phone")
    ordering = ("name",)
    readonly_fields = ("date_registered",)
