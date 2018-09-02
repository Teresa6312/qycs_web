from django.core.mail import send_mail
from django.utils.translation import gettext as _

def send_contact_email(subject, message, cc, user_email ):
    subject = _('Contact us - ') + subject
    message = _('From ') + user_email + '\n' + message
    to_email = ['myqycs.001@gmail.com',]
    if cc:
        to_email += user_email
    send_mail(
        subject,
        message,
        to_email,
        fail_silently=False,
    )
    email.send()
