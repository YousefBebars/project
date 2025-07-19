from django.contrib import admin
from .models import Post, Comment
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)            
from .models import Like, Notification
admin.site.register(Like)              
admin.site.register(Notification)