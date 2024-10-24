# forms.py
from django import forms
from .models import Quiz
from .models import Question

from django.forms import inlineformset_factory
from .models import Question, Choice

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'subject', 'start_time', 'end_time']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Formset for handling multiple Choices related to a Question
# Set extra=2 to always display 2 options for each question
ChoiceFormSet = inlineformset_factory(
    Question, 
    Choice, 
    fields=('text', 'is_correct'), 
    extra=2,  # Always display 3 choice forms
    can_delete=True  # Allow deleting choices if necessary
)
