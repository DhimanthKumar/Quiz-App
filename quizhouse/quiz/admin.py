from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Quiz)
admin.site.register(models.questions)
admin.site.register(models.options)
admin.site.register(models.userquizdata)
admin.site.register(models.quiztime)