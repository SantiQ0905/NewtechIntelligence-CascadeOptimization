from django.db import models


class Worker(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=150, unique=True)


class RealTimeWork(models.Model):
    start_date =  models.DateTimeField(null=True)
    finalized_date = models.DateTimeField()
    hours_worked = models.FloatField()
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True)


class Task(models.Model):
    def __str__(self):
        return f"{self.hours}hrs - {self.title}"

    title = models.CharField(verbose_name="Task title", max_length=150)
    hours = models.FloatField(verbose_name="Estimated working hours")
    description = models.TextField(verbose_name="Task description")
    completed = models.BooleanField(default=False)
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, verbose_name="Asigned worker")
    register_time = models.DateTimeField(null=True, blank=True)
    