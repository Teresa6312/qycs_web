from main.models import OrderSet

def paid(order_set_id, amount, currency, tx = None, confirmed = False):

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
				print('--------------user---------------------------')
				if order.coupon:
					print('---------------------------7--------------')
					for parent_pack in order.parentpackage_set.all():
						print('---------------------------8--------------')
						p = ParentPackage.objects.get(id = parent_pack.id)
						p.paid_amount = float(p.package_amount)*(1-order.coupon.discount/100)
						p.save()
				else:
					print('---------------------------9--------------')
					for parent_pack in order.parentpackage_set.all():
						print('---------------------------10--------------')
						p = ParentPackage.objects.get(id = parent_pack.id)
						p.paid_amount = parent_pack.package_amount
						p.save()

			print('---------------------------11---------------')
			paid_user = User.objects.get(id = user.id)
			if order.currency == 'USD':
				paid_user.reward = math.floor(no_rush_amount) + math.floor(need_pay)
			else:
				paid_user.reward = math.floor(no_rush_amount/7)+ math.floor(need_pay/7)
			paid_user.save()
			print('---------------------------12---------------')
			if order.coupon:
				coup = Coupon.objects.get(id = order.coupon.id)
				coup.used_times = coup.used_times+1
				coup.save()

			print('---------------------------13---------------')
			if confirmed:
				order.payment_confirmed = True
			if tx != None:
				order.tx = tx
			order.save()
	except:
		return
