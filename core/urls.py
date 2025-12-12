from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views, api_views

router = DefaultRouter()
router.register(r"profile", api_views.ProfileViewSet, basename="profile")
router.register(r"enrollments", api_views.EnrollmentViewSet, basename="enrollments")
router.register(
    r"announcements", api_views.AnnouncementViewSet, basename="announcements"
)
router.register(r"payments", api_views.PaymentViewSet, basename="payments")
router.register(r"attendance", api_views.AttendanceViewSet, basename="attendance")

urlpatterns = [
    path("", views.home, name="home"),
    # Auth
    path("login/", views.ParentLoginView.as_view(), name="login"),
    path("signup/", views.ParentRegisterView.as_view(), name="signup"),
    path("logout/", views.logout_view, name="logout"),
    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    # Enrollment
    path("add_child/", views.add_child, name="add_child"),
    path("enrollment/<int:pk>/", views.enrollment_detail, name="enrollment_detail"),
    path("enrollment/<int:pk>/edit/", views.edit_enrollment, name="edit_enrollment"),
    path("toggle_approve/<int:pk>/", views.toggle_approve, name="toggle_approve"),
    # API
    path("api/info/", views.api_info, name="api_info"),
    path("api/", include(router.urls)),
    # Dashboard sub-pages
    path("announcements/", views.announcements_view, name="announcements"),
    path("payments/", views.payments_view, name="payments"),
    path("attendance/", views.attendance_view, name="attendance"),
]
