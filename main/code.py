# from .models import Address, Service, UserProfile
# from django.core.mail import send_mail
#
# def checkAddressWithService(add):
#     return Service.objects.filter(ship_to_add=add).count()>=1
#
# # check every time when a user want to update his/her first_name, last_name, and phone
# def checkAddress(add):
#     profile = UserProfile.objects.get(user = add.user)
#
#     if add.follow_user_infor and checkAddressWithService(add):
#         newadd = Address(user=add.user,
#                         follow_user_infor =True,
#                         address= add.address,
#                         apt = add.apt,
#                         city = add.city,
#                         state = add.state,
#                         country = add.country,
#                         zipcode = add.zipcode,
#                         location_name = add.location_name)
#         newadd.save()
#         add.follow_user_infor = False
#         add.first_name = add.user.first_name
#         add.last_name = add.user.last_name
#         add.email = add.user.email
#         add.phone = profile.phone
#         add.user = None
#         add.save()
#
#         if add == profile.default_address:
#             profile.default_address = newadd
#             profile.save()
#
# def boundEmail(user):
#     message = render_to_string('email/acc_active_email.html', {
#                 'user': user,
#                 'domain': 'myqycs.com',
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token':account_activation_token.make_token(user),
#             })
#     to_email = user.email
#     email = EmailMessage(
#                 mail_subject, message, to=[to_email]
#     )
#     email.send()
#
#     subject = "Confirm your email address"
#     message = "Confirm your email address by click the following link"
#     sender = "myqycs@gmail.com"
#
#     recipients = [recipient, sender]
#
#
#     send_mail(subject, message, sender, recipients)
# #     if checkAddressWithService(add):
