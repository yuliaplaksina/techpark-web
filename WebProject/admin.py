from django.contrib import admin
from WebProject import models

# Register your models here.

admin.site.register(models.Question)
admin.site.register(models.Profile)
admin.site.register(models.Answer)
admin.site.register(models.Tag)
