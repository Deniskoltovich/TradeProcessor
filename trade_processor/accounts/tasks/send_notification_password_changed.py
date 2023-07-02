from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from config import celery_app, settings


@celery_app.task
def send_notification_about_changed_password(user_id):

    user = get_user_model().objects.get(pk=user_id)
    send_mail(
        subject='Changing password',
        message="Your trading bot account's password was changed",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
    )
