from django.db import transaction
from ..models import Organization, Membership

class OrganizationService:
    @staticmethod
    @transaction.atomic
    def create_organization(*, name, creator, **extra_fields):
        """
        Creates an organization and assigns the creator as the first ADMIN.
        Atomic transaction ensures we don't get an Org without an Admin.
        """
        organization = Organization.objects.create(
            name = name,
            created_by = creator,
            **extra_fields
        )        

        Membership.objects.create(
            user = creator,
            organization = organization,
            role = Membership.Role.ADMIN
        )

        return organization