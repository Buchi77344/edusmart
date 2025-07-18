from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(ClassRoom)
admin.site.register(Subject)
admin.site.register(Attendance)
admin.site.register(Result)
admin.site.register(FeePlan)
admin.site.register(Payment)
admin.site.register(TimeTable)
admin.site.register(Announcement)
admin.site.register(Message)

