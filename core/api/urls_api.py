from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.ProfileView.as_view()),
    path('enrollments/', views.EnrollmentListCreateView.as_view()),
    path('enrollments/<int:pk>/', views.EnrollmentDetailView.as_view()),
    path('announcements/', views.AnnouncementListView.as_view()),
    path('attendance/', views.AttendanceListCreateView.as_view()),
    path('payments/', views.PaymentListView.as_view()),
    path('payments/create/', views.PaymentCreateView.as_view()),
    path("children/", views.EnrollmentListCreateView.as_view(), name="children_list"),
    path("children/<int:pk>/", views.EnrollmentDetailView.as_view(), name="children_detail"),
]
