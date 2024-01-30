from django.urls import path
from . import views

app_name = "progress_tracker"

urlpatterns = [

    path("", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("students/", views.StudentListView.as_view(), name="student_list"),
    path(
        "update-progress-report/<int:pk>/",
        views.update_progress_report,
        name="update_progress_report",
    ),
    path("progress_graph/", views.progress_graph, name="progress_graph"),
    path("marksheet/", views.marksheet, name="marksheet"),
    path("assignmnet_report/", views.assignmnet_report, name="assignmnet_report"),
    path("overall_progress/", views.overall_progress, name="overall_progress"),
    # checking branch
]
