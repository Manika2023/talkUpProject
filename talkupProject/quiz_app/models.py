# quiz/models.py

from django.db import models
from django.contrib.auth.models import User

# Model to represent a Quiz
class Quiz(models.Model):
    title = models.CharField(max_length=255)  # Title of the quiz
    subject = models.CharField(max_length=255)  # Subject the quiz belongs to
    start_time = models.DateTimeField()  # Start time of the quiz
    end_time = models.DateTimeField()  # End time of the quiz

    def __str__(self):
        return self.title  # Returns the title of the quiz as its string representation

# Model to represent a Question associated with a Quiz
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')  # Foreign key linking to the Quiz
    text = models.TextField()  # Text of the question

    def __str__(self):
        return self.text  # Returns the question text as its string representation

# Model to represent a Choice for a Question
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')  # Foreign key linking to the Question
    text = models.CharField(max_length=255)  # Text of the choice
    is_correct = models.BooleanField(default=False)  # Indicates whether this choice is the correct answer

    def __str__(self):
        return self.text  # Returns the choice text as its string representation

# Model to store Student's answers to Questions
class StudentAnswer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key linking to the User (student)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Foreign key linking to the Question
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)  # Foreign key linking to the Choice selected by the student

    def __str__(self):
        # Returns a string representation of the StudentAnswer, including the student's name, question text, and selected choice
        return f"{self.student} - {self.question.text[:30]} - {self.choice.text}"
