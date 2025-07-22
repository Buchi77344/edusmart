

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# ---------- AUTH & USER ROLES ----------
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    INSTITUTION_TYPE_CHOICES = [
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary'),
        ('University', 'University'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    school_name = models.CharField(max_length=255, null=True)
    institution_type = models.JSONField(default=list)  # For storing multiple selections like ["Primary", "Secondary"]

    def __str__(self):
        return f"{self.username} ({self.role})"


# ---------- CLASSES & SUBJECTS ----------
class ClassRoom(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'teacher'})

    def __str__(self):
        return f"{self.name} ({self.code})"

# ---------- STUDENT & TEACHER PROFILES ----------
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=100)
    subject_specialization = models.ManyToManyField(Subject, blank=True)

    def __str__(self):
        return self.user.get_full_name()

# ---------- ATTENDANCE ----------
class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'teacher'})

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"

# ---------- RESULTS ----------
class Result(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.CharField(max_length=20)
    score = models.FloatField()
    total = models.FloatField(default=100)

    def get_grade(self):
        percent = (self.score / self.total) * 100
        if percent >= 70:
            return "A"
        elif percent >= 60:
            return "B"
        elif percent >= 50:
            return "C"
        elif percent >= 40:
            return "D"
        else:
            return "F"

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.term}"

# ---------- FEES & PAYMENTS ----------
class FeePlan(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.classroom.name} - {self.term} - ₦{self.amount}"

class Payment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    fee_plan = models.ForeignKey(FeePlan, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)
    receipt_number = models.CharField(max_length=50, unique=True)

    def balance(self):
        return self.fee_plan.amount - self.amount_paid

    def __str__(self):
        return f"{self.student} - ₦{self.amount_paid} - {self.date_paid}"

# ---------- TIMETABLE ----------
class TimeTable(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=[
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'), ('Friday', 'Friday')
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('classroom', 'subject', 'day', 'start_time')

    def __str__(self):
        return f"{self.classroom} - {self.subject} - {self.day}"

# ---------- MESSAGING & NOTIFICATIONS ----------
class Announcement(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"
