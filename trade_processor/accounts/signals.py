from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User
from accounts.tasks.send_confirmation_email import (
    send_confirmation_email,
)


@receiver(post_save, sender=User, weak=False)
def confirmation_email_for_changing_password(sender, instance, **kwargs):
    # TODO: email for password valid.
    pass
