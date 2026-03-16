from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Question, Choice

def home(request):
    questions = Question.objects.all().order_by('-created_date')
    return render(request, 'index.html', {'questions': questions})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def create_poll(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        choices = request.POST.getlist('choices')
        question = Question.objects.create(title=title, description=description, author=request.user)
        for text in choices:
            if text.strip(): Choice.objects.create(question=question, choice_text=text)
        return redirect('home')
    return render(request, 'create_poll.html')

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('results', question_id=question.id)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html', {'question': question, 'error_message': "Seçim yapmadınız!"})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question': question})