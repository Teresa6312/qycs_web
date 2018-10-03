from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token

from django.utils.translation import gettext as _

def send_confirmation_email(request, user):
		mail_subject = _('Activate your Qycs Website account.')
		message = render_to_string('email/acc_active_email.html', {
			'user': user,
			'domain': get_current_site(request).domain,
			'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
			'token':account_activation_token.make_token(user),
		})
		email = EmailMessage(mail_subject, message, to=[user.email])
		email.send()
