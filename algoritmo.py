import time
from multiprocessing import Pool, cpu_count

# Función ineficiente para verificar si un número es primo
def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Función que busca primos en un rango dado
def buscar_primos(rango):
    return [n for n in rango if es_primo(n)]

if __name__ == "__main__":
    num_procesos = cpu_count()  # Usa todos los núcleos disponibles
    print(f"Usando {num_procesos} procesos...")

    rango_maximo = 10**6  # Incrementa esto para mayor consumo
    inicio = time.time()

    # Dividir el rango entre los núcleos disponibles
    rangos = [range(i, rango_maximo, num_procesos) for i in range(num_procesos)]
    
    with Pool(num_procesos) as pool:
        resultados = pool.map(buscar_primos, rangos)

    # Aplanar la lista de resultados
    primos = [p for sublist in resultados for p in sublist]

    fin = time.time()
    print(f"Se encontraron {len(primos)} números primos en {fin - inicio:.2f} segundos.")
