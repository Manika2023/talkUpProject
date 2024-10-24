# quiz/admin.py

from django.contrib import admin
from .models import Quiz, Question, Choice

# Inline class to manage choices related to a question within the admin interface
class ChoiceInline(admin.TabularInline):
    model = Choice  # Specify the model to use for the inline
    extra = 3  # Provide 3 empty choice forms by default

# Admin configuration for the Question model
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]  # Include the ChoiceInline class to manage choices for questions

# Register the Quiz model with the default admin interface
admin.site.register(Quiz)

# Register the Question model with the custom QuestionAdmin configuration
admin.site.register(Question, QuestionAdmin)
