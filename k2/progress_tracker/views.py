
'''This is the view for progress_report app'''

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Trainee, ProgressReport
from .forms import ProgressReportForm
from django.db.models import Avg
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from .models import ProgressReport
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import ProgressReportForm
from .models import ProgressReport
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator

class LoginView(LoginView):
    template_name = 'progress_tracker/login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(reverse_lazy('progress_tracker:overall_progress'))

class LogoutView(LogoutView):
    next_page = reverse_lazy('progress_tracker:login')

class StudentListView(LoginRequiredMixin, ListView):
    model = ProgressReport
    template_name = 'progress_tracker/student_list.html'
    context_object_name = 'progress_reports'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('trainee')


from django.views.generic import DetailView

class StudentDetailView(ListView):
    model = ProgressReport
    template_name = 'progress_tracker/student_detail.html'
    context_object_name = 'progress_report'

    def get_queryset(self):
        return self.model.objects.get(pk = self.kwargs['pk'])
    

method_decorator(login_required, name='dispatch')
class UpdateProgressReportView(UpdateView):
    model = ProgressReport
    form_class = ProgressReportForm
    template_name = "progress_tracker/update_progress_report.html"
    
    def form_valid(self, form):
        form.instance.week_number = 1
        return super().form_valid(form)





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
