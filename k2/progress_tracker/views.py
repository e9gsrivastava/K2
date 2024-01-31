"""This is the view for progress_report app"""

from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, TemplateView
from django.http import Http404

from .models import Trainee, ProgressReport
from .forms import ProgressReportForm


class LoginView(LoginView):
    template_name = "progress_tracker/login.html"

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(reverse_lazy("progress_tracker:overall_progress"))


class LogoutView(LogoutView):
    next_page = reverse_lazy("progress_tracker:login")


class StudentListView(LoginRequiredMixin, ListView):
    model = ProgressReport
    template_name = "progress_tracker/student_list.html"
    context_object_name = "progress_reports"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("trainee")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["trainees"] = Trainee.objects.all()
        return context


class UpdateProgressReportView(UpdateView):
    model = ProgressReport
    form_class = ProgressReportForm
    template_name = "progress_tracker/update_progress_report.html"
    success_url = reverse_lazy("progress_tracker:student_list")

    # def form_valid(self, form):
    #     form.instance.week_number = 1
    #     return super().form_valid(form)


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Trainee
    template_name = "progress_tracker/student_detail.html"
    context_object_name = "trainee"

    def get_object(self, queryset=None):
        username = self.kwargs.get("username", None)
        trainees = Trainee.objects.filter(username=username)

        if not trainees.exists():
            raise Http404("Trainee not found")

        return trainees.first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["progress_reports"] = ProgressReport.objects.filter(trainee=self.object)
        return context


class ProgressGraphView(LoginRequiredMixin, TemplateView):
    template_name = "progress_tracker/progress_graph.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_trainees = Trainee.objects.all()
        context["attendance_data"] = {
            trainee.username: trainee.progress for trainee in all_trainees
        }
        return context


class MarksheetView(LoginRequiredMixin, TemplateView):
    template_name = "progress_tracker/marksheet.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_trainees = Trainee.objects.all()
        context["mark_data"] = {
            trainee.username: trainee.get_marks for trainee in all_trainees
        }
        return context


class AssignmentReportView(LoginRequiredMixin, TemplateView):
    template_name = "progress_tracker/assignmnet_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_trainees = Trainee.objects.all()
        context["assignment_data"] = {
            trainee.username: trainee.get_assignment for trainee in all_trainees
        }
        return context


class OverallProgressView(LoginRequiredMixin, TemplateView):
    template_name = "progress_tracker/overall_progress.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_trainees = Trainee.objects.all()
        context["overall_data"] = {
            trainee.username: trainee.get_progress for trainee in all_trainees
        }
        return context
