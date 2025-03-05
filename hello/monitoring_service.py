import psutil

class MonitoringService:
    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)

    def get_memory_usage(self):
        memory_info = psutil.virtual_memory()
        return memory_info.percent

    def get_energy_usage(self):
        # Simulación de uso de energía
        return 50  # Valor simulado