from main.models import OrderSet

def paid(order_set_id, amount, currency):

	try:
		print('---------------------------0---------------')
		order = OrderSet.objects.get(id=order_set_id)
		need_pay = float(order.total_amount) + float(order.insurance)-order.get_total()[1]
		print(need_pay)
		print(float(amount))
		print(need_pay == float(amount))
		print(currency == order.currency)
		if need_pay == float(amount) and currency == order.currency:
			no_rush_amount = 0
# for sub packages
			print('---------------------------2---------------')

			if order.service_set.all().count()>0:
				print('---------------------------3---------------')
				user = order.service_set.first().user
				if order.coupon:
					print('---------------------------4---------------')
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
				else:
					for pack in order.service_set.all():
						package = Service.objects.get(id = pack.id)
						package.paid_amount = package.get_total()
						package.save()
						if package.no_rush_request:
							no_rush_amount = no_rush_amount + package.paid_amount

# for parent_package
			count = order.parentpackage_set.all().count()
			print('---------------------------5---------------')
			if count > 0:
				print('---------------------------6--------------')
				user = order.parentpackage_set.first().service_set.first().user
				if order.coupon:
					for parent_pack in order.parentpackage_set.all():
						p = ParentPackage.objects.get(id = parent_pack.id)
						p.paid_amount = float(p.package_amount)*(1-order.coupon.discount/100)
						p.save()
				else:
					for parent_pack in order.parentpackage_set.all():
						p = ParentPackage.objects.get(id = parent_pack.id)
						p.paid_amount = parent_pack.package_amount
						p.save()

			print('---------------------------7---------------')
			paid_user = User.objects.get(id = user.id)
			if order.currency == 'USD':
				paid_user.reward = math.floor(no_rush_amount) + math.floor(need_pay)
			else:
				paid_user.reward = math.floor(no_rush_amount/7)+ math.floor(need_pay/7)
			paid_user.save()
			print('---------------------------8---------------')
			if order.coupon:
				coup = Coupon.objects.get(id = order.coupon.id)
				coup.used_times = coup.used_times+1
				coup.save()

	except:
		return
