__author__ = 'muqeetmughal786@gmail.com'

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from client import models as client_models

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.init_super_admin()
        self.assign_permissions_to_group()
        self.create_public_tenant()
        # self.create_units()

    def create_public_tenant(self):
        call_command("createpublictenant")


    def assign_permissions_to_group(self):
        print("Initializing Group Permissions")
        group, created = Group.objects.get_or_create(name="Client")
        client_app_permissions = Permission.objects.filter(
            content_type__app_label='client')
        group.permissions.add(*client_app_permissions)

    def init_super_admin(self):
        print("Initializing Super Admin")
        email = "admin@gmail.com"
        password = 'admin'
        user =  User.objects.filter(email=email).first()
        if not user:
            # for user in settings.ADMINS:
                
            print('Creating account for (%s)' % email)
            admin = User.objects.create_superuser(email=email, password=password)
            admin.is_active = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
        
        