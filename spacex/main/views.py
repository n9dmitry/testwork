from django.shortcuts import render
from .models import Employee


def home(request):
    employee = Employee.objects.all()
    return render(request, 'index.html', {'employee': employee,})