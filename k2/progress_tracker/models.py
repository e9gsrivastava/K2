# progress_report/models.py

from django.db import models
from django.db.models import Avg


class Trainee(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    @property
    def get_progress(self):
        progress_reports = ProgressReport.objects.filter(trainee=self)

        attendance_percentage = (
            progress_reports.aggregate(average=Avg("attendance"))["average"] / 100.0
            if progress_reports
            else 0
        )
        marks_percentage = (
            progress_reports.aggregate(average=Avg("marks"))["average"] / 100.0
            if progress_reports
            else 0
        )
        assignment_percentage = (
            progress_reports.aggregate(average=Avg("assignment"))["average"] / 100.0
            if progress_reports
            else 0
        )

        return (
            attendance_percentage + marks_percentage + assignment_percentage
        ) / 3
    
    @property
    def progress(self):

        progress_reports = ProgressReport.objects.filter(trainee=self)
        percentages = [report.attendance / 100.0 for report in progress_reports]

        return percentages
    
    @property
    def get_marks(self):
        progress_reports = ProgressReport.objects.filter(trainee=self)
        marks = [report.marks / 100.0 for report in progress_reports]
        return marks
    
    @property
    def get_assignment(self):
        progress_reports = ProgressReport.objects.filter(trainee=self)
        assignments = [report.assignment / 100.0 for report in progress_reports]
        return assignments
    

class ProgressReport(models.Model):
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    week_number = models.PositiveIntegerField()
    attendance = models.PositiveIntegerField()
    assignment = models.PositiveIntegerField()
    marks = models.PositiveIntegerField()
    comments = models.TextField()
