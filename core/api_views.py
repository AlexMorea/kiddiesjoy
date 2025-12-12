from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import Enrollment, Announcement, Payment, Attendance, ParentProfile
from .serializers import (
    EnrollmentSerializer,
    EnrollmentCreateSerializer,
    AnnouncementSerializer,
    PaymentSerializer,
    AttendanceSerializer,
    ParentProfileSerializer,
)
from django.shortcuts import get_object_or_404


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ParentProfile.objects.select_related("user").all()
    serializer_class = ParentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related("parent__user").all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return EnrollmentCreateSerializer
        return EnrollmentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Enrollment.objects.all()
        try:
            profile = user.parentprofile
            return Enrollment.objects.filter(parent=profile)
        except ParentProfile.DoesNotExist:
            return Enrollment.objects.none()

    def perform_create(self, serializer):
        profile = self.request.user.parentprofile
        serializer.save(parent=profile)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def toggle_approve(self, request, pk=None):
        enrollment = self.get_object()
        enrollment.approved = not enrollment.approved
        enrollment.save()
        return Response({"approved": enrollment.approved})


class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Announcement.objects.order_by("-created_at")
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        try:
            profile = user.parentprofile
            return Payment.objects.filter(parent=profile)
        except ParentProfile.DoesNotExist:
            return Payment.objects.none()


class AttendanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            profile = user.parentprofile
            return Attendance.objects.filter(child__parent=profile)
        except ParentProfile.DoesNotExist:
            return Attendance.objects.none()


from rest_framework import generics
from .serializers import PushTokenSerializer


class PushTokenCreateView(generics.CreateAPIView):
    serializer_class = PushTokenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        profile = self.request.user.parentprofile
        serializer.save(parent=profile)
