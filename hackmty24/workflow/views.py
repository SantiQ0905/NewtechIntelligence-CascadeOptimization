from django.views.generic import CreateView, View, DetailView
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Task, Worker, RealTimeWork
import datetime
from io import StringIO
import pandas as pd
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import matplotlib.pyplot as plt
from fpdf import FPDF
import math
from django.http import FileResponse

class CreateTask(CreateView):
    model = Task
    template_name: str = "workflow/create_task.html"
    fields = ['title', 'hours', 'description', 'worker']
    
    def get_success_url(self):
        print("workflow:list")
        return reverse("workflow:list")


class ListTasks(View):
    def get(self, request):
        ctx = {"users" : []}
        workers = Worker.objects.all()
        for worker in workers:
            ctx["users"].append(
                {"name" : worker.name, "pk" : worker.pk,
                "tasks" : Task.objects.filter(worker=worker)})
        return render(request, "workflow/listview.html", ctx)


class DetailWorker(DetailView):
    model = Worker
    template_name = "workflow/detailview.html"
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = Task.objects.filter(worker=context["object"])
        return context
    
    def post(self, *args, **kwargs):
        for k, _ in self.request.POST.items():
            try:
                k = int(k)
            except: continue
            obj = Task.objects.get(pk=k)
            obj.completed = True
            obj.register_time = datetime.datetime.now()
            obj.save()
        return redirect(self.request.path)

@method_decorator(csrf_exempt, name='dispatch')
class UploadRealTime(View):
    def post(self, request):
        txt = request.POST['csv']
        pk = int(request.POST['pk'])
        data = StringIO(txt)
        df = pd.read_csv(data, delimiter=';')
        for dat1, dat2, tim in zip(df["initial datetime"], df["final datetime"], df["time_worked(hr)"]):
            print(df)
            RealTimeWork.objects.create(
                start_date = datetime.datetime.strptime(dat1, "%Y-%m-%d %H:%M:%S"),
                finalized_date = datetime.datetime.strptime(dat2, "%Y-%m-%d %H:%M:%S"),
                hours_worked=tim, worker=Worker.objects.get(pk=pk))
        return redirect("/")

def create_plot(p_lst):

    plt.figure(figsize=(5, 5))

    # Plot data
    plt.bar([i for i in range(len(p_lst))], p_lst, label='Productivity')

    # Add titles and labels
    plt.title("Simple Plot Example")
    plt.xlabel("Hours")
    plt.ylabel("Percentage")

    # Add a legend
    plt.legend()

    # Save the plot as an image
    plt.savefig("plot.png")
    plt.close()

def reports(tasks, p_lst, name, work_time):
    # Create an instance of Tasks and add some tasks

    pdf = FPDF()
    pdf.add_page()

    # Add title
    pdf.set_font('times', 'B', size=20)
    pdf.cell(200, 10, txt="Employee Productivity Report" + name, ln=True, align='C')

    pdf.ln(15)

    # Add regular text and bold text in the same line
    pdf.set_font('times', size=16)
    pdf.cell(0, 10, "Real time working: " + str(work_time) + " hours", border=0, ln=True, align='L')

    pdf.ln(10)

    pdf.cell(0, 10, "Completed tasks: ", border=0, ln=True, align='L')

    real_total_time = sum(tasks.values())

    for key, values in tasks.items():
        pdf.cell(0, 10, "Task " + f"{key} - " + f"{values} hours", border=0, ln=0, align='C')
        pdf.ln(10)

    pdf.set_font('times', 'B', size=16)
    pdf.cell(0, 10, "Total: " + str(real_total_time), border=0, ln=True, align='R')


    create_plot(p_lst)

    pdf.image('plot.png', x=50, y=175, w=120)

    pdf.output("report.pdf")


class CreateReport(View):
    def get_info(self, pk):
        n = 3
        self.worker= Worker.objects.get(pk=pk)
        lastn = [i for i in RealTimeWork.objects.filter(worker=self.worker).order_by("-finalized_date")[:n]]
        lastn.reverse()
        p_values = [i.hours_worked for i in reversed(lastn)]
        chamba_periods = [(i.start_date, i.finalized_date) for i in lastn]
        tasks = {}
        for values in chamba_periods:
            for task in Task.objects.filter(worker=self.worker):
                if values[0] <= task.register_time - datetime.timedelta(hours=6) <= values[1]:
                    tasks[task.title] = task.hours
                    break
        return p_values, tasks

    def get(self, request, pk):
        p_values, tasks = self.get_info(pk)
        reports(tasks, p_values, self.worker.name, (30/3600) *sum(p_values)/len(p_values))
        return FileResponse(open("/home/pyskewb/Documents/programming/hackmty24/hackmty24/report.pdf", 'rb'), content_type='application/pdf')