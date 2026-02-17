from django.db import transaction
from django.utils.text import slugify
from ..models import Organization, Membership


class OrganizationService:

    @staticmethod
    def _generate_unique_slug(name):
        """
        Creates a unique slug. 
        Example: 'My Bank' -> 'my-bank', then 'my-bank-1', 'my-bank-2'...
        """
        base_slug = slugify(name)  
        if not base_slug:
            base_slug = "org"       # Fallback for non-latin characters
        slug = base_slug
        counter = 1

        while Organization.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"  
            counter += 1
        return slug   


    @staticmethod
    @transaction.atomic
    def create_organization(*, name, creator, **extra_fields):
        """
        Creates an organization and assigns the creator as the first ADMIN.
        Atomic transaction ensures we don't get an Org without an Admin.
        """

        unique_slug = OrganizationService._generate_unique_slug(name)
        
        organization = Organization.objects.create(
            name = name,
            slug = unique_slug,
            created_by = creator,
            **extra_fields
        )        

        Membership.objects.create(
            user = creator,
            organization = organization,
            role = Membership.Role.ADMIN
        )

        return organization