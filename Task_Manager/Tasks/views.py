from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "Tasks/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(request, "Tasks/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def home(request):
    query = request.GET.get("q", "").strip()
    filter_type = request.GET.get("filter", "all")

    tasks = Task.objects.filter(user=request.user).order_by("-created_at")

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    if filter_type == "tasks":
        tasks = tasks.filter(item_type="task")
    elif filter_type == "notes":
        tasks = tasks.filter(item_type="note")
    elif filter_type == "completed":
        tasks = tasks.filter(is_completed=True)

    context = {
        "tasks": tasks,
        "query": query,
        "filter_type": filter_type,
    }
    return render(request, "Tasks/home.html", context)


@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        item_type = request.POST.get("item_type", "task")
        priority = request.POST.get("priority", "low")
        due_date = request.POST.get("due_date") or None

        if title:
            Task.objects.create(
                user=request.user,
                title=title,
                content=content,
                item_type=item_type,
                priority=priority if item_type == "task" else "low",
                due_date=due_date if item_type == "task" else None,
            )

    return redirect("home")


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        item_type = request.POST.get("item_type", "task")
        priority = request.POST.get("priority", "low")
        due_date = request.POST.get("due_date") or None

        if title:
            task.title = title
            task.content = content
            task.item_type = item_type
            task.priority = priority if item_type == "task" else "low"
            task.due_date = due_date if item_type == "task" else None
            task.save()

    return redirect("home")


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect("home")


@login_required
def toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if task.item_type == "task":
        task.is_completed = not task.is_completed
        task.save()
    return redirect("home")