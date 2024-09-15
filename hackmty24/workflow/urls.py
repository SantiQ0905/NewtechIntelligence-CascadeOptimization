from django.urls import path
from .views import CreateTask, ListTasks, DetailWorker, UploadRealTime, CreateReport 


app_name = "workflow"


urlpatterns = [
    path("create/", CreateTask.as_view(), name="create"),
    path("detail/<int:pk>", DetailWorker.as_view(), name="detail"),
    path("list/", ListTasks.as_view(), name="list"),
    path("consume/", UploadRealTime.as_view()),
    path("report/<int:pk>", CreateReport.as_view())
]