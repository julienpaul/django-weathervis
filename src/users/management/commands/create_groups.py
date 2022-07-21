"""
Create permission groups
Create permissions to models for a set of groups

based on https://stackoverflow.com/a/58231725
"""
from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from src.domains.models import Domain
from src.margins.models import Margin
from src.organisations.models import Organisation
from src.stations.models import Station
from src.users.models import User

GROUPS_PERMISSIONS = {
    "Editor": {
        Station: ["add", "change", "view"],
        Domain: ["add", "change", "view"],
    },
    "Staff": {
        Margin: ["add", "change", "delete", "view"],
        Organisation: ["add", "change", "delete", "view"],
        Station: ["add", "change", "delete", "view"],
        Domain: ["add", "change", "delete", "view"],
        User: ["change", "view"],
    },
}


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = "Create default groups"

    def handle(self, *args, **options):
        # Loop groups
        for group_name in GROUPS_PERMISSIONS:

            # Get or create group
            group, created = Group.objects.get_or_create(name=group_name)

            # Loop models in group
            for model_cls in GROUPS_PERMISSIONS[group_name]:

                # Loop permissions in group/model
                for perm_index, perm_name in enumerate(
                    GROUPS_PERMISSIONS[group_name][model_cls]
                ):

                    # Generate permission name as Django would generate it
                    codename = perm_name + "_" + model_cls._meta.model_name

                    try:
                        # Find permission object and add to group
                        perm = Permission.objects.get(codename=codename)
                        group.permissions.add(perm)
                        self.stdout.write(
                            "Adding " + codename + " to group " + group.__str__()
                        )
                    except Permission.DoesNotExist:
                        self.stdout.write(codename + " not found")
