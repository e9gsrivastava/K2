
'''This is the view for progress_report app'''

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Trainee, ProgressReport
from .forms import ProgressReportForm
from django.db.models import Avg


def login_view(request):
    '''this function creates login view'''
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("progress_tracker:student_list")
    else:
        form = AuthenticationForm()
    return render(request, "progress_tracker/login.html", {"form": form})


def logout_view(request):
    '''this function creates logout view'''
    logout(request)
    return redirect("progress_tracker:login")


@login_required(login_url="progress_tracker:login")
def student_list(request):
    '''this function shows all the data of trainee'''
    progress_reports = ProgressReport.objects.select_related("trainee").all()

    items_per_page = 6
    paginator = Paginator(progress_reports, items_per_page)

    page = request.GET.get("page")
    try:
        progress_reports = paginator.page(page)
    except PageNotAnInteger:
        progress_reports = paginator.page(1)
    except EmptyPage:
        progress_reports = paginator.page(paginator.num_pages)

    return render(
        request,
        "progress_tracker/student_list.html",
        {"progress_reports": progress_reports},
    )


@login_required
def update_progress_report(request, pk):
    ''''this function updates marks and comments'''
    progress_report = get_object_or_404(ProgressReport, pk=pk)

    if request.method == "POST":
        form = ProgressReportForm(request.POST, instance=progress_report)
        if form.is_valid():
            form.instance.week_number = 1
            form.save()
            return redirect("progress_tracker:student_list")
    else:
        form = ProgressReportForm()

    return render(
        request,
        "progress_tracker/update_progress_report.html",
        {"form": form, "pk": pk},
    )


@login_required
def progress_graph(request):
    '''this function creates attendance % view'''
    all_trainees = Trainee.objects.all()
    attendance_data = {}
    for trainee in all_trainees:
        attendance_data[trainee.username] = trainee.progress

    return render(
        request,
        "progress_tracker/progress_graph.html",
        {"attendance_data": attendance_data},
    )


@login_required
def marksheet(request):
    '''this function crates marks given by mentor in % '''
    all_trainees = Trainee.objects.all()
    mark_data = {}
    for trainee in all_trainees:
        mark_data[trainee.username] = trainee.get_marks

    return render(request, "progress_tracker/marksheet.html", {"mark_data": mark_data})


@login_required
def assignmnet_report(request):
    '''this function crates marks given by mentor in % '''
    all_trainees = Trainee.objects.all()
    assignment_data = {}
    for trainee in all_trainees:
        assignment_data[trainee.username] = trainee.get_assignment

    return render(
        request,
        "progress_tracker/assignmnet_report.html",
        {"assignment_data": assignment_data},
    )


@login_required
def overall_progress(request):
    '''this function shows overall progress of tainee  '''
    all_trainees = Trainee.objects.all()
    overall_data = {}

    for trainee in all_trainees:
        overall_data[trainee.username] = trainee.get_progress

    return render(
        request,
        "progress_tracker/overall_progress.html",
        {"overall_data": overall_data},
    )
