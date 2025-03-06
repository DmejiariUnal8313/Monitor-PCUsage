import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from hello.forms import LogMessageForm
from hello.models import LogMessage
from django.views.generic import ListView
from hello.monitoring_service import MonitoringService
from ecologits import EcoLogits
from openai import OpenAI
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        """Adds additional context to the home page."""
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context

def about(request):
    """Renders the about page."""
    return render(request, "hello/about.html")

def monitor(request):
    """Renders the monitor page with system resource usage."""
    service = MonitoringService()
    analysis = service.analyze_usage(duration=60, interval=5)
    
    context = {
        'cpu_usage': f"{analysis['avg_cpu_usage']:.2f}",
        'memory_usage': f"{analysis['avg_memory_usage']:.2f}",
        'energy_usage': f"{analysis['avg_energy_usage']:.2f}",
        'max_cpu_usage': f"{analysis['max_cpu_usage']:.2f}",
        'max_memory_usage': f"{analysis['max_memory_usage']:.2f}",
        'max_energy_usage': f"{analysis['max_energy_usage']:.2f}",
        'min_cpu_usage': f"{analysis['min_cpu_usage']:.2f}",
        'min_memory_usage': f"{analysis['min_memory_usage']:.2f}",
        'min_energy_usage': f"{analysis['min_energy_usage']:.2f}",
        'execution_time': f"{analysis['execution_time']:.2f}",
    }
    
    return render(request, 'hello/monitor.html', context)

def log_message(request):
    """Handles the log message form submission."""
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "hello/log_message.html", {"form": form})

def ecologits_integration(request):
    """Handles the Ecologits integration form submission and displays the results."""
    EcoLogits.init()
    api_key = os.getenv("OPENAI_API_KEY")

    # Verificar si la clave API se ha cargado correctamente
    if not api_key:
        return HttpResponse("Error: No se ha proporcionado una clave API válida.", status=500)

    # Inicializar la lista de resultados en la sesión si no existe
    if 'results' not in request.session:
        request.session['results'] = []

    if request.method == "POST":
        if 'clear' in request.POST:
            # Limpiar los resultados anteriores
            request.session['results'] = []
        else:
            query = request.POST.get("query")
            response = perform_query(api_key, "gpt-4o-mini", [{"role": "user", "content": query}])
            result = {
                "query": query,
                "response": response.choices[0].message.content,
                "energy_consumption": f"{response.impacts.energy.value:.6f} kWh",
                "ghg_emissions": f"{response.impacts.gwp.value:.6f} kgCO2eq",
                "warnings": [str(w) for w in response.impacts.warnings] if response.impacts.has_warnings else [],
                "errors": [str(e) for e in response.impacts.errors] if response.impacts.has_errors else [],
            }
            # Añadir el nuevo resultado a la lista de resultados en la sesión
            request.session['results'].append(result)
            request.session.modified = True

    context = {
        'results': request.session['results']
    }

    return render(request, 'hello/ecologits_integration.html', context)

def perform_query(api_key, model, messages):
    """Performs a query to OpenAI and returns the response."""
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response
