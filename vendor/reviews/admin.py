from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')

admin.site.register(Review, ReviewAdmin)
