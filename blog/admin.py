from django.contrib import admin
from .models import ContactMessage, Post, Comment

admin.site.register(ContactMessage)
admin.site.register(Post)
admin.site.register(Comment)
