from django.contrib import admin
from . models import MemberShip, UserMemberShip, Subscription

admin.site.register(MemberShip)
admin.site.register(UserMemberShip)
admin.site.register(Subscription)
