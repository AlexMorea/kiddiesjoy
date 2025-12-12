from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from core.api.serializers import *
from core.models import *

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        profile, _ = ParentProfile.objects.get_or_create(user=request.user)
        return Response(ParentProfileSerializer(profile).data)

class EnrollmentListCreateView(generics.ListCreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self): return Enrollment.objects.filter(parent=self.request.user)
    def perform_create(self, serializer): serializer.save(parent=self.request.user)

class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self): return Enrollment.objects.filter(parent=self.request.user)

class AnnouncementListView(generics.ListCreateAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self): return Announcement.objects.all().order_by('-created_at')
    def perform_create(self, serializer): serializer.save(posted_by=self.request.user)

class AttendanceListCreateView(generics.ListCreateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self): return Attendance.objects.filter(child__parent=self.request.user)
    def perform_create(self, serializer):
        child = get_object_or_404(Enrollment, pk=self.request.data.get('child_id'), parent=self.request.user)
        serializer.save(child=child)

class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self): return Payment.objects.filter(parent=self.request.user)

class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        child = get_object_or_404(Enrollment, pk=self.request.data.get('child_id'), parent=self.request.user)
        serializer.save(parent=self.request.user, child=child)

@api_view(['GET'])
def api_info(request):
    return Response({
        "name": "Love & Joy Kiddie’s Day Care API",
        "version": "v1.0",
        "description": "Official API for Love & Joy Kiddie’s Day Care Parent Portal",
    })
