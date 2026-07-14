from django import forms

from .models import Student


def generate_student_id():
    student_ids = Student.objects.filter(student_id__startswith="STU").values_list(
        "student_id",
        flat=True,
    )
    numbers = []

    for student_id in student_ids:
        suffix = student_id[3:]

        if suffix.isdigit():
            numbers.append(int(suffix))

    next_number = max(numbers, default=0) + 1
    return f"STU{next_number:03d}"


class StudentForm(forms.ModelForm):
    student_id = forms.CharField(
        label="Student ID",
        required=False,
        help_text="Leave blank to generate the next student ID.",
    )

    class Meta:
        model = Student
        fields = ["student_id", "name", "age", "phone", "email"]
        labels = {
            "name": "Full name",
            "phone": "Phone number",
            "email": "Email address",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        if self.instance and self.instance.pk:
            self.fields["student_id"].disabled = True
            self.fields["student_id"].help_text = "Student ID cannot be changed."

    def clean_student_id(self):
        student_id = self.cleaned_data["student_id"].strip().upper()

        if student_id == "" and not self.instance.pk:
            return generate_student_id()

        if student_id == "":
            raise forms.ValidationError("Student ID is required.")

        return student_id
