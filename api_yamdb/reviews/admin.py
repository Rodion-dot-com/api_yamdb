from django.contrib import admin

from reviews.models import Review, Comment, User


admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comment)
