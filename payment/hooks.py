from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from django.conf import settings
from main.models import OrderSet, Service, User, Coupon, ParentPackage
from paypal.standard.ipn.models import PayPalIPN

import math

# https://django-paypal.readthedocs.io/en/stable/standard/ipn.html
def payment_paid(sender, **kwargs):
	print('------------ipn_obj.mc_gross_x---------0------------')
	ipn_obj = sender
	if ipn_obj.payment_status == ST_PP_COMPLETED:
		order = OrderSet.objects.get(id = ipn_obj.invoice)
		if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
			return

		print('------------ipn_obj.mc_gross_x---------------------')
		print(ipn_obj.mc_gross)
		print(ipn_obj.mc_gross_x)
		print(order.total_amount-order.get_total()[1])

		if ipn_obj.mc_gross >= order.total_amount + order.insurance and ipn_obj.mc_currency == order.currency:
			no_rush_amount = 0
# for sub packages
			if order.service_set.all().count()>0:
				user = order.service_set.first().user
				print('------------ipn_obj.mc_gross_x------------1---------')
				if order.coupon:
					for pack in order.service_set.all():
						package = Service.objects.get(id = pack.id)
						if package.order and order.coupon.order:
							package.paid_amount = package.get_total()*(1-order.coupon.discount/100)
						elif order.coupon.package and not package.order:
							package.paid_amount = package.get_total()*(1-order.coupon.discount/100)
						else:
							package.paid_amount = package.get_total()
						package.save()
						if package.no_rush_request:
							no_rush_amount = no_rush_amount + package.paid_amount
					print('------------ipn_obj.mc_gross_x------------2---------')
				else:
					for pack in order.service_set.all():
						package = Service.objects.get(id = pack.id)
						package.paid_amount = package.get_total()
						package.save()
						if package.no_rush_request:
							no_rush_amount = no_rush_amount + package.paid_amount
					print('------------ipn_obj.mc_gross_x------------3---------')

# for parent_package
			count = order.parentpackage_set.all().count()
			if count > 0:
				user = order.parentpackage_set.first().service_set.first().user
				print('------------ipn_obj.mc_gross_x------------4---------')
				if order.coupon:
					for parent_pack in order.parentpackage_set.all():
						paid_amount = 0
						print('------------ipn_obj.mc_gross_x------------5---------')
						for pack in parent_pack.service_set.all():
							package = Service.objects.get(id = pack.id)
							if package.order and order.coupon.order:
								package.paid_amount = package.get_total()*(1-order.coupon.discount/100)
							elif order.coupon.package and not package.order:
								package.paid_amount = package.get_total()*(1-order.coupon.discount/100)
							else:
								package.paid_amount = package.get_total()
							package.save()
							if package.no_rush_request:
								no_rush_amount = no_rush_amount + package.paid_amount
							paid_amount = paid_amount+package.paid_amount

						p = ParentPackage.objects.get(id = parent_pack.id)
						p.paid_amount = paid_amount
						p.save()
					print('------------ipn_obj.mc_gross_x------------6---------')
				else:
					for parent_pack in order.parentpackage_set.all():
						for pack in parent_pack.service_set.all():
							package = Service.objects.get(id = pack.id)
							package.paid_amount = parent_pack.package_amount/count
							package.save()
							if package.no_rush_request:
								no_rush_amount = no_rush_amount + package.paid_amount

						p = ParentPackage.objects.get(id = parent_pack.id)
						p.paid_amount = parent_pack.package_amount
						p.save()
						print('------------ipn_obj.mc_gross_x------------7---------')

			paid_user = User.objects.get(id = user.id)
			if order.currency == 'USD':
				paid_user.reward = math.floor(no_rush_amount) + math.floor(p.paid_amount)
			else:
				paid_user.reward = math.floor(no_rush_amount/7)+ math.floor(p.paid_amount/7)
			paid_user.save()

			if order.coupon:
				coup = Coupon.objects.get(id = order.coupon.id)
				coup.used_times = coup.used_times+1
				coup.save()
			print('------------ipn_obj.mc_gross_x------------8---------')
		else:
			print('------------ipn_obj.mc_gross_x------------9---------')
			return
	else:
		print('------------ipn_obj.mc_gross_x------------10---------')
		return

valid_ipn_received.connect(payment_paid)

#
# from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
# from paypal.standard.models import ST_PP_COMPLETED
# from django.conf import settings
# from main.models import OrderSet, Service, User
# from paypal.standard.ipn.models import PayPalIPN
#
#
#
# # https://django-paypal.readthedocs.io/en/stable/standard/ipn.html
# def payment_paid(sender, **kwargs):
# 	ipn_obj = sender
# 	print('------------ipn_obj.mc_gross_x---------0------------')
# 	print(ipn_obj)
# 	if ipn_obj.payment_status == ST_PP_COMPLETED:
# 		order = OrderSet.objects.get(id = ipn_obj.invoice)
# 		if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
# 			return
#
# 		if ipn_obj.mc_gross == order.total_amount and ipn_obj.mc_currency == order.currency:
# 			if order.service_set.all().count()>0:
# 				user = order.service_set.first().user
# 				if order.coupon:
# 					for pack in order.service_set.all():
# 						package = Service.objects.get(id = pack.id)
# 						package.paid_amount = package.get_total()*(1-order.coupon.discount/100)
# 						package.save()
# 				else:
# 					for pack in order.service_set.all():
# 						package = Service.objects.get(id = pack.id)
# 						package.paid_amount = package.get_total()
# 						package.save()
#
#
# # parent_package
# 			count = order.parentpackage_set.all().count()
# 			if count > 0:
# 				user = order.parentpackage_set.first().service_set.first().user
# 				if order.coupon:
# 					for parent_pack in order.parentpackage_set.all():
# 						parent_pack.paid_amount = parent_pack.package_amount*(1-order.coupon.discount/100)
# 						for pack in parent_pack.service_set.all():
# 							package = Service.objects.get(id = pack.id)
# 							package.paid_amount = parent_pack.package_amount*(1-order.coupon.discount/100)/count
# 							package.save()
# 				else:
# 					for parent_pack in order.parentpackage_set.all():
# 						parent_pack.paid_amount = parent_pack.package_amount
# 						for pack in parent_pack.service_set.all():
# 							package = Service.objects.get(id = pack.id)
# 							package.paid_amount = parent_pack.package_amount/count
# 							package.save()
#
# 			paid_user = User.objects.get(id = user.id)
# 			if order.currency == 'USD':
# 				paid_user.reward = int(order.total_amount)
# 			else:
# 				paid_user.reward = int(order.total_amount/7)
# 			paid_user.save()
# 		else:
# 			return
# 	else:
# 		return
#
# valid_ipn_received.connect(payment_paid)
