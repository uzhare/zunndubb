from django.contrib import admin
from .models import Group, GroupUser, GroupOwner

admin.site.register(Group)
admin.site.register(GroupUser)
admin.site.register(GroupOwner)
