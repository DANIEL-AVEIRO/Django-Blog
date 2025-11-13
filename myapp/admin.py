from django.contrib import admin
from myapp import models

# Register your models here.

admin.site.register(models.PostModel)
admin.site.register(models.CommentModel)
admin.site.register(models.CategoryModel)
