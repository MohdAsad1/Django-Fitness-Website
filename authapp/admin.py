from django.contrib import admin
from authapp.models import *


admin.site.register(Contact)
admin.site.register(Enrollment)
admin.site.register(Trainer)
admin.site.register(Gallery)
admin.site.register(ExerciseType)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'exercise_type')
    search_fields = ('name',)


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ('plan', 'price')
    search_fields = ('price',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'login_time', 'user', 'logout_time', 'work_out', 'trainer',)
    search_fields = ('date_time', 'workout')


