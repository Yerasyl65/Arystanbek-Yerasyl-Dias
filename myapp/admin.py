from django.contrib import admin
from .models import CustomUser, Subject, Grade, Homework, Schedule
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (_('Дополнительно'), {'fields': ('role',)}),
    )
    list_display = ['username', 'email', 'role', 'is_staff']

class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('subject', 'due_date')
    fields = ('subject', 'description', 'due_date')
    def save_model(self, request, obj, form, change):
        if not change:
            obj.teacher = request.user
        super().save_model(request, obj, form, change)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'teacher':
            return qs.filter(teacher=request.user)
        return qs
    def has_change_permission(self, request, obj=None):
        if obj and obj.teacher != request.user:
            return False
        return super().has_change_permission(request, obj)

class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'value', 'date')
    fields = ('student', 'subject', 'value')
    # При необходимости добавьте аналогичные фильтры для учителя

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subject)
admin.site.register(Homework, HomeworkAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Schedule)
