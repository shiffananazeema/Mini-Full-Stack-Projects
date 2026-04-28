from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ExpenseForm, RegisterForm
from .models import Expense


def build_dashboard_context(user, form=None, edit_form=None, editing_expense=None):
    expenses = Expense.objects.filter(user=user)
    total_spent = expenses.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    latest_expense = expenses.order_by("-expense_date", "-created_at").first()

    current_month = timezone.localdate().replace(day=1)
    monthly_total = (
        expenses.filter(expense_date__gte=current_month).aggregate(total=Sum("amount"))["total"]
        or Decimal("0.00")
    )

    category_totals = list(
        expenses.values("category")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    category_breakdown = []
    # Build a small list the template can render directly.
    for item in category_totals:
        percentage = 0
        if total_spent > 0:
            percentage = round((item["total"] / total_spent) * 100, 1)
        category_breakdown.append(
            {
                "category": item["category"],
                "total": item["total"],
                "percentage": percentage,
            }
        )

    monthly_expenses = list(
        expenses.annotate(month=TruncMonth("expense_date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    for row in monthly_expenses:
        row["label"] = row["month"].strftime("%b %Y") if row["month"] else ""

    return {
        "expenses": expenses,
        "form": form or ExpenseForm(),
        "edit_form": edit_form or ExpenseForm(prefix="edit"),
        "editing_expense": editing_expense,
        "total_spent": total_spent,
        "monthly_total": monthly_total,
        "latest_expense": latest_expense,
        "category_breakdown": category_breakdown,
        "category_labels": [item["category"] for item in category_breakdown],
        "category_values": [float(item["total"]) for item in category_breakdown],
        "monthly_expenses": monthly_expenses,
    }


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "expenses/home.html", build_dashboard_context(request.user))


@login_required
def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, "Expense added successfully.")
        else:
            messages.error(request, "Please fix the form errors and try again.")
            return render(request, "expenses/home.html", build_dashboard_context(request.user, form=form))
    return redirect("home")


@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense, prefix="edit")
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully.")
            return redirect("home")

        messages.error(request, "Please fix the form errors and try again.")
        return render(
            request,
            "expenses/home.html",
            build_dashboard_context(
                request.user,
                edit_form=form,
                editing_expense=expense,
            ),
        )
    return redirect("home")


@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "Expense deleted.")
    return redirect("home")


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(
        request,
        "expenses/auth_form.html",
        {"form": form, "title": "Create account", "button_text": "Register"},
    )
