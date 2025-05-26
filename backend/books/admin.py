from django.contrib import admin
from .models import Category, Book

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category')
    list_filter = ('category', 'author')
    search_fields = ('title', 'author')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'category', 'author', 'cover_image')
        }),
    )
