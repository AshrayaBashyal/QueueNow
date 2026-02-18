from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import OrganizationCreateSerializer, OrganizationSerializer
from ..models import Organization
from ..services.organization_service import OrganizationService
from .permissions import IsOrgAdminOrReadOnly


class OrganizationViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Organization.objects.all()
    permission_classes = [IsAuthenticated, IsOrgAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "create":
            return OrganizationCreateSerializer
        return OrganizationSerializer    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = OrganizationService.create_organization(
            creator=request.user,
            **serializer.validated_data
        )

        output_serializer = OrganizationSerializer(organization, context={'request': request})
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"], url_path="my") #detail=False --> /organizations/my/ (it acts on the whole collection).If detail=True --> /organizations/{slug}/my/ (acting on one specific org).
    def my_organizations(self, request):
        """
        Returns only organizations where the current user is a member.
        """
        user_orgs = Organization.objects.filter(memberships__user = request.user)
        serializer = self.get_serializer(user_orgs, many=True)
        return Response(serializer.data)
