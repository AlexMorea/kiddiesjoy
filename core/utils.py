from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(user):
    subject = "Welcome to Love & Joy Kiddie’s Day Care!"
    message = f"""
    Hi {user.first_name},

    Thank you for joining Love & Joy Kiddie’s Day Care.
    You can now manage your child’s enrollment and updates from your parent portal.

    With love & care,  
    The Love & Joy Team
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
