from django.contrib import admin
from .models import ParentProfile, Enrollment, Announcement, Attendance, Payment

@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user','phone_number','occupation','profile_created')
    search_fields = ('user__username','phone_number','occupation')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('child_name','parent','class_group','approved','date_enrolled')
    list_editable = ('approved',)
    list_filter = ('approved','class_group')
    search_fields = ('child_name','parent__username')
    date_hierarchy = 'date_enrolled'

    def approve_enrollments(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f"{updated} enrollments approved.")
    approve_enrollments.short_description = "Mark selected enrollments as approved"

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title','posted_by','created_at')
    search_fields = ('title','message')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('child','date','present')
    list_filter = ('present',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reference','parent','child','amount','verified','date_paid')
    list_filter = ('verified',)

admin.site.site_header = "Love & Joy Kiddie’s Day Care Admin"
admin.site.site_title = "Love & Joy Kiddie’s Portal"
admin.site.index_title = "Welcome to Love & Joy Kiddie’s Day Care Management System"