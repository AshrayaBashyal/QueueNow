from rest_framework import serializers
from ..models import Organization
from core.utils.text_cleaners import collapse_spaces
from django.utils.text import slugify


class OrganizationCreateSerializer(serializers.ModelSerializer):
    """Used for input validation only"""
    class Meta:
        model = Organization
        fields = ['name', 'description', 'address', 'phone_number']

    def validate(self, data):
        for field in ['name', 'description', 'address', 'phone_number']:
            if data.get(field):
                data[field] = collapse_spaces(data[field])
                
        return data


class OrganizationSerializer(serializers.ModelSerializer):
    """Used for returning the full organization data"""
    user_role = serializers.SerializerMethodField()
    class Meta:
        model = Organization
        fields = ['id', 'name', 'slug', 'description', 'address', 'phone_number', 'created_at', 'user_role']
        read_only_fields = ['id', 'slug', 'created_at']

    def get_user_role(self, obj):
        # This is how you "grab" the request inside a serializer
        request = self.context.get('request') 
        
        if request and request.user.is_authenticated:
            # Now you can use request.user just like in a view
            membership = obj.memberships.filter(user=request.user).first()
            return membership.role if membership else None
        return None

