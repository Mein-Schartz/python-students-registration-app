from django.urls import path

from . import views
app_name = "registration"

# Each path connects a browser URL to a view function in registration/views.py.
urlpatterns = [
    # The dashboard currently starts on the student list.
    path("", views.student_list, name="home"),

    # Student CRUD routes.
    path("students/", views.student_list, name="student_list"),
    path("students/add/", views.student_create, name="student_create"),
    path("students/<str:student_id>/", views.student_detail, name="student_detail"),
    path("students/<str:student_id>/edit/", views.student_update, name="student_update"),
    path("students/<str:student_id>/delete/", views.student_delete, name="student_delete"),
]
