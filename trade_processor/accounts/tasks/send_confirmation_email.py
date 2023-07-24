from celery.utils.log import get_task_logger
from django.core.mail import send_mail

from accounts.services.auth_service import AuthService
from config import celery_app, settings

logger = get_task_logger(__name__)


@celery_app.task
def send_confirmation_email(user_id):

    """
    The send_confirmation_email function sends an email to the user
    with a link that they can click on to activate their account.

    :param user_id: Get the user from the database
    :return: None
    """
    activation_link, user = AuthService.generate_activation_link(user_id)

    send_mail(
        subject='Account confirmation',
        message=f'Confirmation link: {activation_link}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
    )
    logger.info('Email is send')
