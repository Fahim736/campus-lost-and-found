from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Report, Project
from .forms import ReportForm


def home(request):
    return render(request, 'home.html')

def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'projects_list.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project_detail.html', {'project': project})

def about(request):
    return render(request, 'about.html')



def reports_list(request):
    reports = Report.objects.all().order_by('-created_at')

    item_name = request.GET.get('item_name', '')
    category = request.GET.get('category', '')
    report_type = request.GET.get('type', '')
    status = request.GET.get('status', '')

    if item_name:
        reports = reports.filter(item_name__icontains=item_name)

    if category:
        reports = reports.filter(category__icontains=category)

    if report_type:
        reports = reports.filter(type=report_type)

    if status:
        reports = reports.filter(status=status)

    context = {
        'reports': reports,
        'item_name': item_name,
        'category': category,
        'selected_type': report_type,
        'selected_status': status,
    }

    return render(request, 'reports.html', context)


def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)
    return render(request, 'report_detail.html', {'report': report})


@login_required
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, 'Report created successfully!')
            return redirect('reports')
    else:
        form = ReportForm()

    return render(request, 'report_form.html', {'form': form, 'title': 'Create Report'})


@login_required
def update_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if report.user != request.user:
        messages.error(request, 'You cannot edit another user\'s report.')
        return redirect('report_detail', pk=pk)

    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report updated successfully!')
            return redirect('report_detail', pk=pk)
    else:
        form = ReportForm(instance=report)

    return render(request, 'report_form.html', {'form': form, 'title': 'Update Report'})


@login_required
def delete_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if report.user != request.user:
        messages.error(request, 'You cannot delete another user\'s report.')
        return redirect('report_detail', pk=pk)

    if request.method == 'POST':
        report.delete()
        messages.success(request, 'Report deleted successfully!')
        return redirect('reports')

    return redirect('report_detail', pk=pk)


@login_required
def resolve_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if report.user != request.user:
        messages.error(request, 'You cannot resolve another user\'s report.')
        return redirect('report_detail', pk=pk)

    report.status = 'Resolved'
    report.save()
    messages.success(request, 'Report marked as resolved!')
    return redirect('report_detail', pk=pk)


@login_required
def my_reports(request):
    reports = Report.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_reports.html', {'reports': reports})


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')