from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .student_forms import StudentForm
from .models import Student


def student_list(request):
    """Display the student table. Used by / and /students/."""
    query = request.GET.get("q", "").strip()
    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(student_id__icontains=query)
            | Q(name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone__icontains=query)
        )

    context = {
        "students": students,
        "query": query,
        "total_students": Student.objects.count(),
        "active_menu": "students",
    }
    return render(request, "registration/student_list.html", context)


def student_detail(request, student_id):
    """Display one student profile. Used by /students/<student_id>/."""
    student = get_object_or_404(Student, student_id=student_id)

    return render(
        request,
        "registration/student_detail.html",
        {
            "student": student,
            "active_menu": "students",
        },
    )


def student_create(request):
    """Create a new student record. Used by /students/add/."""
    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            student = form.save()
            messages.success(request, f"{student.name} was added successfully.")
            return redirect("registration:student_detail", student_id=student.student_id)
    else:
        form = StudentForm()

    return render(
        request,
        "registration/student_form.html",
        {
            "form": form,
            "page_title": "Add Student",
            "submit_label": "Create Student",
            "active_menu": "students",
        },
    )


def student_update(request, student_id):
    """Edit an existing student record. Used by /students/<student_id>/edit/."""
    student = get_object_or_404(Student, student_id=student_id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            student = form.save()
            messages.success(request, f"{student.name} was updated successfully.")
            return redirect("registration:student_detail", student_id=student.student_id)
    else:
        form = StudentForm(instance=student)

    return render(
        request,
        "registration/student_form.html",
        {
            "form": form,
            "student": student,
            "page_title": "Edit Student",
            "submit_label": "Save Changes",
            "active_menu": "students",
        },
    )


def student_delete(request, student_id):
    """Confirm and delete a student record. Used by /students/<student_id>/delete/."""
    student = get_object_or_404(Student, student_id=student_id)

    if request.method == "POST":
        student_name = student.name
        student.delete()
        messages.success(request, f"{student_name} was deleted successfully.")
        return redirect("registration:student_list")

    return render(
        request,
        "registration/student_confirm_delete.html",
        {
            "student": student,
            "active_menu": "students",
        },
    )
