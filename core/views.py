from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User

from .forms import (
    SignUpForm,
    ParentProfileForm,
    EnrollmentForm,
    ParentLoginForm,
)
from .models import ParentProfile, Enrollment


def home(request):
    return render(request, "home.html")


class ParentRegisterView(View):
    template_name = "signup.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {"form": SignUpForm(), "profile_form": ParentProfileForm()},
        )

    def post(self, request):
        form = SignUpForm(request.POST)
        profile_form = ParentProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(
                request, "Account created successfully! You can now log in."
            )
            return redirect("login")

        messages.error(request, "Please correct the errors below.")
        return render(
            request, self.template_name, {"form": form, "profile_form": profile_form}
        )


class ParentLoginView(View):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name, {"form": ParentLoginForm()})

    def post(self, request):
        form = ParentLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Allow login by email: find matching user and authenticate by username
            try:
                user_obj = User.objects.get(email__iexact=email)
                user = authenticate(
                    request, username=user_obj.username, password=password
                )
            except User.DoesNotExist:
                user = None

            if user is not None:
                auth_login(request, user)
                return redirect("dashboard")

        messages.error(request, "Invalid email or password.")
        return redirect("login")


@login_required
def dashboard(request):
    # Parent sees only THEIR children (admins see all)
    if request.user.is_staff:
        children = Enrollment.objects.all().order_by("-date_enrolled")
    else:
        children = Enrollment.objects.filter(parent=request.user).order_by(
            "-date_enrolled"
        )

    # Example placeholders for cards (you can wire to models / API later)
    announcements = []  # replace with Announcement.objects.all() or api call
    attendance_records = []  # replace with real records
    payments = []  # replace with real payments

    return render(
        request,
        "dashboard.html",
        {
            "children": children,
            "announcements": announcements,
            "attendance": attendance_records,
            "payments": payments,
        },
    )


@login_required
def add_child(request):
    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enroll = form.save(commit=False)
            enroll.parent = request.user
            enroll.save()
            messages.success(request, "Child enrollment submitted.")
            return redirect("dashboard")
    else:
        form = EnrollmentForm()

    return render(request, "add_child.html", {"form": form})


@login_required
def enrollment_detail(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)

    # parents can ONLY view their children unless admin
    if request.user != enrollment.parent and not request.user.is_staff:
        return redirect("dashboard")

    return render(request, "enrollment_detail.html", {"enrollment": enrollment})


@login_required
def edit_enrollment(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)

    if request.user != enrollment.parent and not request.user.is_staff:
        return redirect("dashboard")

    if request.method == "POST":
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            messages.success(request, "Enrollment updated successfully.")
            return redirect("enrollment_detail", pk=enrollment.pk)
    else:
        form = EnrollmentForm(instance=enrollment)

    return render(
        request, "enrollment_edit.html", {"form": form, "enrollment": enrollment}
    )


def api_info(request):
    return JsonResponse(
        {
            "service": "Love & Joy Kiddie’s Day Care API",
            "version": "1.0",
            "status": "running",
            "endpoints": {
                "profile": "/api/profile/",
                "enrollments": "/api/enrollments/",
                "announcements": "/api/announcements/",
                "attendance": "/api/attendance/",
                "payments": "/api/payments/",
            },
        }
    )


@login_required
def toggle_approve(request, pk):
    if not request.user.is_staff:
        return redirect("dashboard")

    enrollment = get_object_or_404(Enrollment, pk=pk)
    enrollment.approved = not enrollment.approved
    enrollment.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", reverse("dashboard")))


def logout_view(request):
    auth_logout(request)
    return redirect("login")


@login_required
def announcements_view(request):
    announcements = []  # replace with actual model query later
    return render(request, "announcements.html", {"announcements": announcements})


@login_required
def payments_view(request):
    payments = []  # replace with actual Payment model query later
    return render(request, "payments.html", {"payments": payments})


@login_required
def attendance_view(request):
    attendance = []  # replace with actual Attendance model query later
    return render(request, "attendance.html", {"attendance": attendance})
