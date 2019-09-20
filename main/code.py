from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from .models import Service, ParentPackage, Coupon

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

def send_copackage_ready_to_pay_email(pack_id):
		try:
			coup = Coupon.objects.get(code="WELCOME")
			if not coup.check_coupon(user=None):
				coup = None
		except:
			coup = None
		package = Service.objects.get(id=pack_id)
		mail_subject = "%s - %s"%(package.get_cust_carrier_display(), package.cust_tracking_num)+_(' is ready to pay')
		message = render_to_string('email/copackage_ready_to_pay.html', {
			'username':package.user.username,
			'carrier':package.get_cust_carrier_display(),
			'tracking_num':package.cust_tracking_num,
			'coupon':coup,
		})
		email = EmailMessage(mail_subject, message, to=[package.user.email])
		email.send()

def send_package_ready_to_pay_email(pack_id):
		try:
			coup = Coupon.objects.get(code="WELCOME")
			if not coup.check_coupon(user=None):
				coup = None
		except:
			coup = None
		package = ParentPackage.objects.get(id=pack_id)
		mail_subject = _('Your direct shipping package is ready to pay')
		message = render_to_string('email/package_ready_to_pay.html', {
			'username':package.service_set.first().user.username,
			'parent_pack': package,
			'coupon':coup,
		})
		email = EmailMessage(mail_subject, message, to=[package.service_set.first().user.email])
		email.send()
