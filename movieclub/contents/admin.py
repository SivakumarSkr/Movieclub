from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Blog)
admin.site.register(Answer)
admin.site.register(Review)
admin.site.register(Status)