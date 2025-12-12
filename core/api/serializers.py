from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import ParentProfile, Enrollment, Announcement, Attendance, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class ParentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ParentProfile
        fields = ("user", "phone_number", "address", "occupation", "profile_created")


class EnrollmentSerializer(serializers.ModelSerializer):
    parent = UserSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = "__all__"
        read_only_fields = ("parent", "date_enrolled")


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        exclude = ()


class AnnouncementSerializer(serializers.ModelSerializer):
    posted_by = UserSerializer(read_only=True)

    class Meta:
        model = Announcement
        fields = ("id", "title", "message", "created_at", "posted_by")


class AttendanceSerializer(serializers.ModelSerializer):
    child = EnrollmentSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ("id", "child", "date", "present", "notes")


class PaymentSerializer(serializers.ModelSerializer):
    parent = UserSerializer(read_only=True)
    child = EnrollmentSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "reference",
            "parent",
            "child",
            "amount",
            "date_paid",
            "verified",
        )
