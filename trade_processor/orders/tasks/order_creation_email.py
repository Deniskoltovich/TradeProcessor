from django.core.mail import send_mail

from config import celery_app, settings
from orders.services.get_order_info_for_email import GetOrderInfoService


@celery_app.task(bind=False)
def send_email_with_order_info(
    order_data, errors: tuple | None = None, auto=False
):
    """
    The send_email_with_order_info function sends an email to the
    user with information about their order.

    :param order_data: Pass the order data to the function
    :param errors: tuple: Pass the errors tuple to the
        send_email_with_order_info function
    :return: None
    """

    message, recipient = GetOrderInfoService.get_info(order_data, errors, auto)
    send_mail(
        subject='Order status',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[
            recipient,
        ],
    )
