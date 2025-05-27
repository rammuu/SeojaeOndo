from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    nickname = models.CharField(max_length=50, unique=True, null=True, blank=True)
    favorite_categories = models.JSONField(default=list)
    bookshelf = models.ManyToManyField('books.Book', blank=True, related_name='saved_by_users')
    following = models.ManyToManyField(
        'self', 
        through='Follow',
        symmetrical=False, 
        related_name='followers_set'
    )

    REQUIRED_FIELDS = ['email', 'name', 'phone_number', 'nickname']

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
