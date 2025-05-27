from django.db import models
from django.conf import settings
import datetime

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    isbn = models.CharField(max_length=20, unique=True, help_text="ISBN number")
    cover = models.URLField(max_length=1024, blank=True, null=True, help_text="URL for the book cover image")
    publisher = models.CharField(max_length=100, blank=True, null=True)
    pub_date = models.DateField(blank=True, null=True, help_text="Publication date")
    author = models.CharField(max_length=255, blank=True, null=True)
    author_info = models.TextField(blank=True, null=True)
    author_photo = models.URLField(max_length=1024, blank=True, null=True, help_text="URL for the author's photo")
    customer_review_rank = models.IntegerField(blank=True, null=True, help_text="Customer review rank or rating")
    subTitle = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class OpenEnding(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='open_endings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.nickname or self.user.username} - {self.book.title} 열린 결말"
    

class OpenEndingLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    open_ending = models.ForeignKey('OpenEnding', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'open_ending'], name='unique_open_ending_like')
        ]

    def __str__(self):
        return f"{self.user.username} likes 결말 {self.open_ending.id}"

class OpenEndingComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    open_ending = models.ForeignKey('OpenEnding', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on 결말 {self.open_ending.id}"




class Thread(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    reading_date = models.DateField(default=datetime.date.today)
    cover_img = models.ImageField(upload_to="thread_cover_img/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_threads", blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.CharField(max_length=100)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)

    def __str__(self):
        return self.content