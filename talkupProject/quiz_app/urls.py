# quiz/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('quizzes/', views.quiz_list, name='quiz_list'),  # Define the URL pattern
    path('quiz/<int:quiz_id>/', views.quiz_view, name='quiz_view'),
    path('quiz/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),

    # urls for admin
     path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_quiz/', views.add_quiz, name='add_quiz'),
    path('update_quiz/<int:quiz_id>/', views.update_quiz, name='update_quiz'),
    path('delete_quiz/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),

    # paths for question
    path('quiz/<int:quiz_id>/add_question/', views.add_question, name='add_question'),
    path('question/<int:question_id>/update/', views.update_question, name='update_question'),
    path('question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
]