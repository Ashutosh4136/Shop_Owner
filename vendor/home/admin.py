from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Banner, StaticPage

admin.site.register(Banner)
admin.site.register(StaticPage)
