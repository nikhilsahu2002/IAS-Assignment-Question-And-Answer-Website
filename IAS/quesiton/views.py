from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from quesiton.models import Question
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.models import  User
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        question_text = request.POST.get('question')
        answer = request.POST.get('answer')
        image = request.FILES.get('image')
        url = request.POST.get('url')
        submit_time = request.POST.get('submit-time')
        subject = request.POST.get('subject')
        topic = request.POST.get('topic')

        # Create and save a new instance of the Question model
        Question.objects.create(
            title=title,
            question=question_text,
            answer=answer,
            image=image,
            url=url,
            submit_time=submit_time,
            subject=subject,
            topic=topic
        )

        return redirect("question") 

    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('')  # Redirect to your home page or wherever you want
        else:
            # Passwords don't match, handle accordingly (you may want to display an error)
            pass

    return render(request, 'Registration.html')

def user_login(request):
    error = None  # Default value for error

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to your home page or wherever you want
        else:
            error = "Login error"

    return render(request, 'login.html', {'error': error})

def user_logout(request):
    logout(request)
    return redirect('question')

def question(request):
    # Number of questions to display per page
    questions_per_page = 1

    # Get all questions from the database
    all_questions = Question.objects.all()

    # Create a Paginator instance
    paginator = Paginator(all_questions, questions_per_page)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    try:
        # Get the questions for the requested page
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page
        questions = paginator.page(paginator.num_pages)

    return render(request, "Home.html", {"questions": questions})