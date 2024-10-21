from django.contrib import admin
from .models import Department, Employee  # Импортируем модели

# Регистрируем модель Department
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')  # Показать эти поля в списке
    search_fields = ('name',)  # Поля для поиска

# Регистрируем модель Employee
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'hire_date', 'salary', 'department')
    search_fields = ('full_name', 'position', 'department__name')  # Поиск по полям