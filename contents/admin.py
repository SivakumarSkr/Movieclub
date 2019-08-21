from django.contrib import admin
from .models import *
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.

admin.site.register(Blog, MarkdownxModelAdmin)
admin.site.register(Answer, MarkdownxModelAdmin)
admin.site.register(Review, MarkdownxModelAdmin)
admin.site.register(Status)
