from django.shortcuts import render

# Create your views here.
# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm
from .models import CustomUser

def home(request):
    return render(request,'users/home.html')
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'users/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

# def user_list(request):
#     users = CustomUser.objects.all()
#     return render(request, 'users/user_list.html', {'users': users})
from django.shortcuts import render
from .models import CustomUser
from django.db.models import Q  # Add this line

def user_list(request):
    query = request.GET.get('q', '')  # Get the search term
    category = request.GET.get('category', '')  # Get the selected category (CSE, ECE, etc.)

    users = CustomUser.objects.all()

    # Apply search filtering
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(bio__icontains=query) |
            Q(location__icontains=query) |
            Q(education__icontains=query) |
            Q(experience__icontains=query) |
            Q(skills__icontains=query)
        )

    # Apply category filtering
    if category:
        users = users.filter(
            Q(bio__icontains=category) |
            Q(education__icontains=category) |
            Q(skills__icontains=category)
        )

    return render(request, 'users/user_list.html', {'users': users, 'query': query, 'category': category})

def user_detail(request, pk):
    user = CustomUser.objects.get(id=pk)
    return render(request, 'users/user_detail.html', {'user': user})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import CustomUser, Message
from .forms import MessageForm

@login_required
def chat_page(request, username):
    user = get_object_or_404(CustomUser, username=username)
    
    # Ensure the group exists for the user
    group_name = f"group_{user.username}"
    group, created = Group.objects.get_or_create(name=group_name)
    
    # Fetch messages for this group
    messages = Message.objects.filter(group=group).order_by('timestamp')

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.group = group
            message.save()
            return redirect('chat_page', username=user.username)
    else:
        form = MessageForm()

    return render(request, 'users/chat_page.html', {'user': user, 'messages': messages, 'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import JobPosting
from django.utils.timezone import now

@login_required
def job_posting(request):
    if request.method == "POST":
        title = request.POST.get("title")
        company = request.POST.get("company")
        location = request.POST.get("location")
        description = request.POST.get("description")
        apply_link = request.POST.get("apply_link")

        if title and company and location and description and apply_link:
            JobPosting.objects.create(
                user=request.user,
                title=title,
                company=company,
                location=location,
                description=description,
                apply_link=apply_link,
                posted_at=now()
            )
            return redirect("job_list")  # Redirect to job listing page

    return render(request, "users/job_posting.html")

from django.shortcuts import render
from django.db.models import Q
from .models import JobPosting

def job_list(request):
    query = request.GET.get('q', '')  # Get search input

    jobs = JobPosting.objects.all().order_by("-posted_at")  # Get latest jobs first

    # Apply search filtering
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | 
            Q(company__icontains=query) | 
            Q(location__icontains=query)
        )

    return render(request, "users/job_list.html", {"jobs": jobs, "query": query})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

# def question_list(request):
#     questions = Question.objects.all().order_by('-created_at')  # Fetch all questions
#     return render(request, 'users/questions_list.html', {'questions': questions})
from django.shortcuts import render
from .models import Question

from django.shortcuts import render
from django.db.models import Q
from .models import Question

def question_list(request):
    query = request.GET.get('q', '')  # Get search input
    category = request.GET.get('category', '')  # Get selected category

    questions = Question.objects.all()

    # Apply search filtering
    if query:
        questions = questions.filter(
            Q(question_text__icontains=query) |
            Q(tags__icontains=query) |
            Q(source__icontains=query)  # Searching in book/exam source as well
        )

    # Apply category filtering (subject-wise)
    if category:
        questions = questions.filter(category__iexact=category)

    return render(request, 'users/questions_list.html', {'questions': questions, 'query': query, 'category': category})
@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question).order_by('-upvotes') 

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question  # Link answer to the question
            answer.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = AnswerForm()

    return render(request, 'users/question_detail.html', {'question': question, 'answers': answers, 'form': form})
@login_required
def ask_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('question_list')
    else:
        form = QuestionForm()

    return render(request, 'users/ask_question.html', {'form': form})
# View to handle upvoting an answer
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Answer, UserUpvote

@login_required
def upvote_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    user = request.user

    # Check if user has already upvoted this specific answer
    existing_upvote = UserUpvote.objects.filter(user=user, answer=answer).first()

    if existing_upvote:
        return JsonResponse({'message': 'You have already upvoted this answer.'}, status=400)

    # Add upvote
    answer.upvotes += 1
    answer.upvoted_by.add(user)
    answer.save()

    # Track the upvote
    UserUpvote.objects.create(user=user, answer=answer)

    return JsonResponse({'upvotes': answer.upvotes})
