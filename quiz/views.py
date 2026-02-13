
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import UserRegisterForm
from .models import Quiz, Question, Choice, StudentAnswer

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.user_type = form.cleaned_data['user_type']
            user.profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'quiz/register.html', {'form': form})

def home(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/home.html', {'quizzes': quizzes})

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()
    if request.method == 'POST':
        score = 0
        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected:
                choice = Choice.objects.get(id=int(selected))
                StudentAnswer.objects.create(student=request.user, question=question, selected_choice=choice)
                if choice.is_correct:
                    score += 1
        return render(request, 'quiz/result.html', {'score': score, 'total': questions.count(), 'quiz': quiz})
    return render(request, 'quiz/take_quiz.html', {'quiz': quiz, 'questions': questions})

