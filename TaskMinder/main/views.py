from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from datetime import datetime, timedelta , date
from .models import Task , Comment 
from django.db.models import Q
from django.core.mail import send_mail
from django.http import JsonResponse

# Create your views here.



# Home page
def home_page(request:HttpRequest):

    tasks = Task.objects.all()
    # projects = Project.objects.all()
    comments = Comment.objects.all().order_by('-created_at')[:5]
    # important_events = Event.objects.filter(is_important=True)
    
    return render(request, "main/home_page.html", {
        "tasks": tasks,
        # "projects": projects,
        "comments": comments,
        # "important_events": important_events
    })



# View tasks
def tasks(request:HttpRequest):

    tasks = Task.objects.all()
    return render(request, 'home_page.html', {'tasks': tasks})



# Add task 
def task_list(request:HttpRequest):

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        task = Task(title=title, description=description, priority=priority)
        task.save()
        return redirect('main:tasks')
    # return render(request, 'home_page.html')
    return render(request, 'main/task_list.html', {'tasks': tasks})


# def task_list(request):
#     tasks = Task.objects.all()  
#     return render(request, 'task_list.html', {'tasks': tasks})



def create_task(request:HttpRequest):
    if request.method == 'POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due_date')
        description = request.POST.get('description')

        # Create a new task object
        task = Task(title=title, due_date=due_date, description=description)
        task.save() 

        return redirect('dashboard')  
    
    return render(request, 'task_list.html', {'task': task})


# Task search 
# def task_search(request: HttpRequest):
#     tasks = Task.objects.all()

#     if "search" in request.GET:
#         search_query = request.GET["search"]
#         tasks = tasks.filter(
#             Q(title__contains=search_query) |
#             Q(priority__name__contains=search_query) |
#             Q(status__contains=search_query)
#         )

#     if "due_date" in request.GET and len(request.GET["due_date"]) > 4:
#         due_date_str = request.GET["due_date"]
#         due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
#         tasks = tasks.filter(due_date=due_date)

#     return render(request, "main/search.html", {"tasks": tasks})



# Add comment 
def add_comment(request:HttpRequest, task_id):

    if not request.user.is_authenticated:
        return redirect("accounts:sign_in")

    if request.method == "POST":
        task_object = Task.objects.get(pk=task_id)
        new_comment = Comment(task=task_object,user=request.user, content=request.POST["content"])
        new_comment.save()

    return redirect("main:task_detail", task_id=task_id)




# Task detail 
def task_detail(request:HttpRequest, task_id):

    try:
        task = Task.objects.get(pk=task_id)
        comments = Comment.objects.filter(task =task) 

    except Task.DoesNotExist:
        return render(request, "main/not_found.html")
    except Exception as e:
        print(e)


    return render(request, "main/task_detail.html", {"task" : task, "comments" : comments })



# Dashboard
def dashboard(request:HttpRequest):
    comments = Comment.objects.all()[0:3]

    return render(request, "main/dashboard.html", {"comments":comments})



# Journal 

def journal(request:HttpRequest):
    comments = Comment.objects.all()[0:3]

    return render(request, "main/journal.html", {"comments":comments})



# Reading list

def reading_list(request:HttpRequest):

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        task = Task(title=title, description=description, priority=priority)
        task.save()
        return redirect('main:tasks')
    # return render(request, 'home_page.html')
    return render(request, 'main/reading_list.html', {'tasks': tasks})


# Note 

def notes(request:HttpRequest, task_id):

    if not request.user.is_authenticated:
        return redirect("accounts:sign_in")

    if request.method == "POST":
        task_object = Task.objects.get(pk=task_id)
        new_comment = Comment(task=task_object,user=request.user, content=request.POST["content"])
        new_comment.save()

    return redirect("main:notes", task_id=task_id)

# Yearly Goals 



def yearly_goals(request:HttpRequest):

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        task = Task(title=title, description=description, priority=priority)
        task.save()
        return redirect('main:tasks')
    # return render(request, 'home_page.html')
    return render(request, 'main/reading_list.html', {'tasks': tasks})






# Send email 
# def send_email(request:HttpRequest):
    
#     if request.method == 'POST':
#         recipient_email = request.POST.get('recipient_email')
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')
#         send_mail(subject, message, 'your-email@example.com', [recipient_email])
#         return JsonResponse({'success': True})

#     return render(request, 'dashboard.html')