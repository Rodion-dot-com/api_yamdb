from django.contrib import admin

from reviews.models import Review, Comment, User, Title, Genre, Category, TitleGenre


admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(TitleGenre)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
