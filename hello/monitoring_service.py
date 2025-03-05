import psutil
import time

class MonitoringService:
    def get_cpu_usage(self):
        return psutil.cpu_percent(interval=1)

    def get_memory_usage(self):
        memory_info = psutil.virtual_memory()
        return memory_info.percent

    def get_energy_usage(self):
        # Simulación de uso de energía
        return 50  # Valor simulado

    def analyze_usage(self, duration=60, interval=5):
        start_time = time.time()  # Registrar el tiempo de inicio

        cpu_usages = []
        memory_usages = []
        energy_usages = []

        for _ in range(duration // interval):
            cpu_usages.append(self.get_cpu_usage())
            memory_usages.append(self.get_memory_usage())
            energy_usages.append(self.get_energy_usage())
            time.sleep(interval)

        avg_cpu_usage = sum(cpu_usages) / len(cpu_usages)
        avg_memory_usage = sum(memory_usages) / len(memory_usages)
        avg_energy_usage = sum(energy_usages) / len(energy_usages)

        analysis = {
            'avg_cpu_usage': avg_cpu_usage,
            'avg_memory_usage': avg_memory_usage,
            'avg_energy_usage': avg_energy_usage,
            'max_cpu_usage': max(cpu_usages),
            'max_memory_usage': max(memory_usages),
            'max_energy_usage': max(energy_usages),
            'min_cpu_usage': min(cpu_usages),
            'min_memory_usage': min(memory_usages),
            'min_energy_usage': min(energy_usages),
        }

        end_time = time.time()
        execution_time = end_time - start_time  # Calcular el tiempo de ejecución

        analysis['execution_time'] = execution_time
        
        return analysis