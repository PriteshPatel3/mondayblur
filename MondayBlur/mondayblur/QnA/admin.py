from django.contrib import admin
from .models import question,category,comment

class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("category",)}


admin.site.register(question,QuestionAdmin)
admin.site.register(category,CategoryAdmin)
admin.site.register(comment)


