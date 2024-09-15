from django.contrib import admin
from .models import Worker, Task, RealTimeWork

# Register your models here.
class WorkerAdmin(admin.ModelAdmin):
    pass

class TaskAdmin(admin.ModelAdmin):
    pass

class WorkTimeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Worker, WorkerAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(RealTimeWork, WorkTimeAdmin)