from django.urls import path

from . import views


app_name = "registration"

urlpatterns = [
    path("", views.student_list, name="home"),
    path("students/", views.student_list, name="student_list"),
    path("students/add/", views.student_create, name="student_create"),
    path("students/<str:student_id>/", views.student_detail, name="student_detail"),
    path("students/<str:student_id>/edit/", views.student_update, name="student_update"),
    path("students/<str:student_id>/delete/", views.student_delete, name="student_delete"),
]
