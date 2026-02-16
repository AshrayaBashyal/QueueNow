import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from core.utils.text_cleaners import collapse_spaces

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=255, unique=False)         #unique=True??
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT,
        related_name="owned_organizations"
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = collapse_spaces(self.name)
        if self.description:
            self.description = collapse_spaces(self.description)
        if self.address:
            self.address = collapse_spaces(self.address)
        if self.phone_number: 
            self.phone_number = collapse_spaces(self.phone_number)
        
        if not self.slug:
            self.slug = slugify(self.name)
        else:
            self.slug = slugify(self.slug)
            
        super().save(*args, **kwargs)
