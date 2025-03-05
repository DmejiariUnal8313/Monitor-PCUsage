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
    monitoring_service = MonitoringService()
    cpu_usage = monitoring_service.get_cpu_usage()
    memory_usage = monitoring_service.get_memory_usage()
    energy_usage = monitoring_service.get_energy_usage()

    context = {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'energy_usage': energy_usage,
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
