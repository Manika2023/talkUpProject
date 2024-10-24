# quiz/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Quiz, StudentAnswer
from .forms import QuestionForm,QuizForm



def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_app/quiz_list.html', {'quizzes': quizzes})

@login_required
def quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    current_time = timezone.now()

    # Check if the user has already submitted answers for this quiz
    if StudentAnswer.objects.filter(student=request.user, question__quiz=quiz).exists():
        return redirect('quiz_results', quiz_id=quiz.id)  # Redirect to results if already attempted

    # Check quiz timing
    if current_time < quiz.start_time:
        message = f"The quiz will start at {quiz.start_time}."
        quiz_active = False
    elif current_time > quiz.end_time:
        message = "The quiz has ended. Please wait for the next one."
        quiz_active = False
    else:
        quiz_active = True
        message = None

    # If quiz is active and form is submitted
    if request.method == 'POST' and quiz_active:
        for question in quiz.questions.all():
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:
                StudentAnswer.objects.create(
                    student=request.user,
                    question=question,
                    choice_id=selected_choice_id
                )
        return redirect('quiz_results', quiz_id=quiz.id)

    return render(request, 'quiz_app/quiz.html', {'quiz': quiz, 'quiz_active': quiz_active, 'message': message})

def quiz_results(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    answers = StudentAnswer.objects.filter(student=request.user, question__quiz=quiz)

    score = sum(1 for answer in answers if answer.choice.is_correct)  # Assuming `is_correct` attribute in Choice model
    total_questions = quiz.questions.count()
    passing_score = total_questions / 2  # Calculate passing score

    return render(request, 'quiz_app/results.html', {
        'quiz': quiz,
        'score': score,
        'total_questions': total_questions,
        'passing_score': passing_score,  # Pass the passing score to the template
    })


# all views for admin 
@login_required
def admin_dashboard(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_app/admin_dashboard.html', {'quizzes': quizzes})

@login_required
def add_quiz(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = QuizForm()
    return render(request, 'quiz_app/add_quiz.html', {'form': form})

@login_required
def update_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        quiz.title = request.POST['title']
        quiz.subject = request.POST['subject']
        quiz.start_time = request.POST['start_time']
        quiz.end_time = request.POST['end_time']
        quiz.save()
        return redirect('admin_dashboard')
    return render(request, 'quiz_app/update_quiz.html', {'quiz': quiz})

@login_required
# quiz/views.py
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        quiz.delete()
        return redirect('quiz_list')
    return render(request, 'quiz/delete_quiz.html', {'quiz': quiz})


# views for adding , updating and deleting questions
# your_app/views.py
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Question, Choice
from .forms import QuestionForm, ChoiceFormSet

def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            formset.instance = question
            formset.save()
            return redirect('admin_dashboard')  # Redirect to the dashboard after saving
    else:
        form = QuestionForm()
        formset = ChoiceFormSet()
    
    return render(request, 'quiz_app/add_questions.html', {'form': form, 'formset': formset, 'quiz': quiz})
def update_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = ChoiceFormSet(request.POST, instance=question)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('admin_dashboard')  # Redirect to the dashboard after saving
    else:
        form = QuestionForm(instance=question)
        formset = ChoiceFormSet(instance=question)
    
    return render(request, 'quiz_app/update_question.html', {
        'form': form,
        'formset': formset,
        'question': question
    })

def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        question.delete()
        return redirect('admin_dashboard')  # Redirect to the admin dashboard after deleting
    return render(request, 'quiz_app/delete_question.html', {'question': question})
