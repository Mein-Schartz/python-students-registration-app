from django.contrib import admin

from .models import Course, Lecturer, Student


@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    list_display = (
        "lecturer_id",
        "full_name",
        "email",
        "phone",
        "department",
        "specialization",
        "is_active",
    )
    list_filter = ("is_active", "department")
    search_fields = ("lecturer_id", "full_name", "email", "phone")
    ordering = ("full_name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "fee", "duration", "lecturer", "capacity", "is_active")
    list_filter = ("is_active", "lecturer")
    search_fields = ("code", "name", "lecturer__full_name", "lecturer__lecturer_id")
    ordering = ("code",)
    autocomplete_fields = ("lecturer",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "name", "age", "phone", "email", "date_registered")
    search_fields = ("student_id", "name", "email", "phone")
    ordering = ("name",)
    readonly_fields = ("date_registered",)
