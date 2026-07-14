import csv
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from registration.models import Course, Lecturer


class Command(BaseCommand):
    help = "Seed lecturers and default courses from the existing CSV files."

    def handle(self, *args, **options):
        lecturers_path = settings.BASE_DIR / "lecturers.csv"
        courses_path = settings.BASE_DIR / "courses.csv"

        if not lecturers_path.exists():
            raise CommandError(f"Could not find {lecturers_path}")

        if not courses_path.exists():
            raise CommandError(f"Could not find {courses_path}")

        lecturer_count = self.seed_lecturers(lecturers_path)
        course_count = self.seed_courses(courses_path)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {lecturer_count} lecturers and {course_count} courses."
            )
        )

    def seed_lecturers(self, lecturers_path):
        count = 0

        with lecturers_path.open(newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                lecturer_id = row["Lecturer_id"].strip()

                if not lecturer_id:
                    continue

                Lecturer.objects.update_or_create(
                    lecturer_id=lecturer_id,
                    defaults={
                        "full_name": row["Lecturer_name"].strip(),
                        "email": row["Email"].strip(),
                        "phone": row.get("Phone", "").strip(),
                    },
                )
                count += 1

        return count

    def seed_courses(self, courses_path):
        count = 0

        with courses_path.open(newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                course_code = row["code"].strip()

                if not course_code:
                    continue

                lecturer = self.get_lecturer(row.get("lecturer_id", ""))

                Course.objects.update_or_create(
                    code=course_code,
                    defaults={
                        "name": row["name"].strip(),
                        "fee": self.parse_fee(row["fee"]),
                        "duration": row["duration"].strip(),
                        "lecturer": lecturer,
                    },
                )
                count += 1

        return count

    def get_lecturer(self, lecturer_id):
        lecturer_id = lecturer_id.strip()

        if lecturer_id == "":
            return None

        try:
            return Lecturer.objects.get(lecturer_id=lecturer_id)
        except Lecturer.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(
                    f"Course references missing lecturer '{lecturer_id}'. Leaving it unassigned."
                )
            )
            return None

    def parse_fee(self, fee):
        try:
            return Decimal(fee)
        except InvalidOperation as error:
            raise CommandError(f"Invalid course fee: {fee}") from error
