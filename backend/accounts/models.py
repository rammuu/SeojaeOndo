from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50) # Consider blank=True, null=True if can be initially empty
    phone_number = models.CharField(max_length=20) # Consider blank=True, null=True
    nickname = models.CharField(max_length=50, unique=True, null=True, blank=True) # Allow null/blank initially
    favorite_categories = models.JSONField(default=list)
    following = models.ManyToManyField(
        'self', 
        through='Follow',  # Explicit intermediary table
        symmetrical=False, 
        related_name='followers_set' # Changed from 'followers' to avoid conflict if we add a followers property
    )

    # REQUIRED_FIELDS is for createsuperuser. For social, allauth handles it.
    # If nickname can be blank/null initially, it shouldn't be in REQUIRED_FIELDS
    # if that list is strictly enforced for all user creation paths.
    # Let's adjust REQUIRED_FIELDS if nickname can now be initially blank.
    # However, allauth's signup form might still require it if listed here.
    # For now, let's assume allauth's social signup bypasses direct use of REQUIRED_FIELDS for missing fields.
    REQUIRED_FIELDS = ['email', 'name', 'phone_number'] # Nickname can be set later

class Follow(models.Model):
    from_user = models.ForeignKey(User, related_name='following_relations', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='follower_relations', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['from_user', 'to_user'], name='unique_follow')
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_user} follows {self.to_user}"
