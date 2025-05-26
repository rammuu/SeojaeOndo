from django.contrib import admin
from .models import Category, Book

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'category', 'pub_date', 'customer_review_rank')
    list_filter = ('category', 'publisher', 'author')
    search_fields = ('title', 'isbn', 'author', 'publisher')
    date_hierarchy = 'pub_date'
    fieldsets = (
        (None, {
            'fields': ('title', 'subTitle', 'isbn', 'category')
        }),
        ('Author & Publisher', {
            'fields': ('author', 'author_info', 'author_photo', 'publisher', 'pub_date')
        }),
        ('Details', {
            'fields': ('description', 'cover', 'customer_review_rank')
        }),
    )
