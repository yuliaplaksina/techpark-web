from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from WebProject import models
from WebProject.forms import RegisterForm, QuestionForm
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.


def register(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                auth.login(request, user)
                return redirect(to=request.GET.get('next', 'main'))
    else:
        form = RegisterForm()

    return render(request, 'registration/registration.html', {'form': form})


@login_required
def add_question(request):
    if request.POST:
        form = QuestionForm(request.user, request.POST)
        if form.is_valid():
            question = form.save()
            if question is not None:
                return redirect(to='question', qid=question.id)
    else:
        form = QuestionForm(request.user)

    return render(request, 'add_question.html', {'form': form})


def pagination(request, model, count):
    paginator = Paginator(model, count)

    page = request.GET.get('page', 1)
    try:
        # Если существует, то выбираем эту страницу
        model = paginator.page(page)
    except PageNotAnInteger:
        # Если None, то выбираем первую страницу
        model = paginator.page(1)
    except EmptyPage:
        # Если вышли за последнюю страницу, то возвращаем последнюю
        model = paginator.page(paginator.num_pages)

    return model


def home(request):
    questions = models.Question.objects.new()
    questions = pagination(request, questions, 20)

    return render(request, 'home.html', {'questions': questions, 'fil': 'home'})


def best(request):
    questions = models.Question.objects.best()
    questions = pagination(request, questions, 20)

    return render(request, 'home.html', {'questions': questions, 'fil': 'best'})


def profile(request):

    return render(request, 'settings_profile.html')


def question_page(request, qid):

    question = models.Question.objects.add_fields().get(pk=qid)

    answers = models.Answer.objects.filter(question=question)
    answers = pagination(request, answers, 10)

    return render(request, 'question.html', {'question': question, 'answers': answers})
