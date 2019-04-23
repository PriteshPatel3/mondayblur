from django.contrib import admin
from .models import question,category,comment

class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(question,QuestionAdmin)
admin.site.register(category)
admin.site.register(comment)


