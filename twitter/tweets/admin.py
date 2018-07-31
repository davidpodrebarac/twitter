from django.contrib import admin

# Register your models here.
from .models import Tweet, Tag

admin.register(Tweet)
admin.register(Tag)

