import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from hello.forms import LogMessageForm
from hello.models import LogMessage
from django.views.generic import ListView
from hello.monitoring_service import MonitoringService

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def about(request):
    return render(request, "hello/about.html")

def monitor(request):
    service = MonitoringService()
    analysis = service.analyze_usage(duration=60, interval=5)
    
    context = {
        'cpu_usage': analysis['avg_cpu_usage'],
        'memory_usage': analysis['avg_memory_usage'],
        'energy_usage': analysis['avg_energy_usage'],
        'max_cpu_usage': analysis['max_cpu_usage'],
        'max_memory_usage': analysis['max_memory_usage'],
        'max_energy_usage': analysis['max_energy_usage'],
        'min_cpu_usage': analysis['min_cpu_usage'],
        'min_memory_usage': analysis['min_memory_usage'],
        'min_energy_usage': analysis['min_energy_usage'],
        'execution_time': analysis['execution_time'],
    }
    
    return render(request, 'hello/monitor.html', context)

# Add this code elsewhere in the file:
def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "hello/log_message.html", {"form": form})
