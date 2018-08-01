from django.contrib import admin

# Register your models here.
from .models import Tweet, Tag

admin.site.register(Tweet)
admin.site.register(Tag)
