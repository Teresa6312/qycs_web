from .models import Address, Service, UserProfile


def checkAddressWithService(add):
    return Service.objects.filter(ship_to_add=add).count()>=1

# check every time when a user want to update his/her first_name, last_name, and phone
def checkAddress(add):
    profile = UserProfile.objects.get(user = add.user)

    if add.follow_user_infor and checkAddressWithService(add):
        newadd = Address(user=add.user,
                        follow_user_infor =True,
                        address= add.address,
                        apt = add.apt,
                        city = add.city,
                        state = add.state,
                        country = add.country,
                        zipcode = add.zipcode,
                        location_name = add.location_name)
        newadd.save()
        add.follow_user_infor = False
        add.first_name = add.user.first_name
        add.last_name = add.user.last_name
        add.email = add.user.email
        add.phone = profile.phone
        add.user = None
        add.save()

        if add == profile.default_address:
            profile.default_address = newadd
            profile.save()

# def updateAddress(add):
#     if checkAddressWithService(add):
