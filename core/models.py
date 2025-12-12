from django.db import models
from django.contrib.auth.models import User


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    profile_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Profile"


class Enrollment(models.Model):
    CLASS_GROUPS = [
        ("Infants", "Infants (6–12 months)"),
        ("Toddlers", "Toddlers (1–3 years)"),
        ("Preschool", "Preschool (3–5 years)"),
    ]
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    child_name = models.CharField(max_length=100)
    child_age = models.PositiveIntegerField()
    parent_contact = models.CharField(max_length=20)
    address = models.TextField()
    medical_info = models.TextField(blank=True, null=True)
    class_group = models.CharField(max_length=20, choices=CLASS_GROUPS)
    date_enrolled = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.child_name} ({self.parent.username})"


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Attendance(models.Model):
    child = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE, related_name="attendances"
    )
    date = models.DateField(auto_now_add=True)
    present = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("child", "date")

    def __str__(self):
        return f"{self.child.child_name} - {'Present' if self.present else 'Absent'} on {self.date}"


class Payment(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    child = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=100, unique=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.reference} by {self.parent.username}"

    def __str__(self):
        return self.title


class PushToken(models.Model):
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
