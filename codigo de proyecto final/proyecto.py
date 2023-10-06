import csv
import time
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

def convertirCSV_lista(filename):
    lista = []
    with open(filename, 'r', encoding="utf-8") as archivo_csv:
        lectura_csv = csv.reader(archivo_csv)
        for fila_num, fila in enumerate(lectura_csv, start=1):
            lista.append((fila_num, fila))  # Guardar número de posición y fila
    return lista

def convertirCSV_lista2(filename):
    lista = []
    with open(filename, 'r', encoding="utf-8") as archivo_csv:
        lectura_csv = csv.reader(archivo_csv)
        for fila_num, fila in enumerate(lectura_csv, start=1):
            lista.append((fila_num, fila[1], fila[2]))  # Guardamos el número de fila, la profesión y el nombre
    return lista
#'''''''''''''''''''''''''''''''''''''
def insertion_sort_descendente(lista):
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        while j >= 0 and actual[0] > lista[j][0]:
            lista[j+1] = lista[j]
            j -= 1
        lista[j+1] = actual


def merge_sort_descendente(lista):
    if len(lista) > 1:
        medio = len(lista) // 2
        mitad_izq = lista[:medio]
        mitad_der = lista[medio:]

        merge_sort_descendente(mitad_izq)
        merge_sort_descendente(mitad_der)

        i = j = k = 0

        while i < len(mitad_izq) and j < len(mitad_der):
            if mitad_izq[i][0] > mitad_der[j][0]:
                lista[k] = mitad_izq[i]
                i += 1
            else:
                lista[k] = mitad_der[j]
                j += 1
            k += 1

        while i < len(mitad_izq):
            lista[k] = mitad_izq[i]
            i += 1
            k += 1

        while j < len(mitad_der):
            lista[k] = mitad_der[j]
            j += 1
            k += 1



#'''''''''''''''''''''''''''''''
def busqueda_binaria_iterativa(lista, carrera):
    resultados = []
    inicio = 0
    fin = len(lista) - 1
    start_time = time.time()

    while inicio <= fin:
        medio = (inicio + fin) // 2
        if carrera.upper() in lista[medio][1].upper():
            resultados.append((lista[medio][0], lista[medio][1], lista[medio][2]))
            # Buscar más ocurrencias hacia la izquierda
            izquierda = medio - 1
            while izquierda >= inicio and lista[izquierda][1].upper() == carrera.upper():
                resultados.append((lista[izquierda][0], lista[izquierda][1], lista[izquierda][2]))
                izquierda -= 1
            # Buscar más ocurrencias hacia la derecha
            derecha = medio + 1
            while derecha <= fin and lista[derecha][1].upper() == carrera.upper():
                resultados.append((lista[derecha][0], lista[derecha][1], lista[derecha][2]))
                derecha += 1
            break
        elif carrera.upper() < lista[medio][1].upper():
            fin = medio - 1
        else:
            inicio = medio + 1

    end_time = time.time()
    return resultados, end_time - start_time

def busqueda_binaria_recursiva(lista, carrera, inicio, fin):
    resultados = []
    if inicio > fin:
        return resultados

    medio = (inicio + fin) // 2
    if carrera.upper() in lista[medio][1].upper():
        resultados.append((lista[medio][0], lista[medio][1], lista[medio][2]))
        # Buscar más ocurrencias hacia la izquierda
        izquierda = medio - 1
        while izquierda >= inicio and lista[izquierda][1].upper() == carrera.upper():
            resultados.append((lista[izquierda][0], lista[izquierda][1], lista[izquierda][2]))
            izquierda -= 1
        # Buscar más ocurrencias hacia la derecha
        derecha = medio + 1
        while derecha <= fin and lista[derecha][1].upper() == carrera.upper():
            resultados.append((lista[derecha][0], lista[derecha][1], lista[derecha][2]))
            derecha += 1
        return resultados
    else:
        if carrera.upper() < lista[medio][1].upper():
            return busqueda_binaria_recursiva(lista, carrera, inicio, medio - 1)
        else:
            return busqueda_binaria_recursiva(lista, carrera, medio + 1, fin)


# Convertir el archivo CSV en una lista de listas
archivo_csv = 'datos.csv'
lista = convertirCSV_lista(archivo_csv)



def ordenar_insertion_sort():
    global lista
    inicio_tiempo = time.time()
    insertion_sort_descendente(lista)
    fin_tiempo = time.time()
    mostrar_resultados("Ordenamiento (Insertion Sort)", inicio_tiempo, fin_tiempo)

def ordenar_merge_sort():
    global lista
    lista = convertirCSV_lista(archivo_csv)
    inicio_tiempo = time.time()
    merge_sort_descendente(lista)
    fin_tiempo = time.time()
    mostrar_resultados("Ordenamiento (Merge Sort)", inicio_tiempo, fin_tiempo)

def buscar_iterativa():
    global lista
    archivo_csv = 'datos.csv'
    lista = convertirCSV_lista2(archivo_csv)
    lista.sort(key=lambda x: x[1])
    carrera_buscar = input_entry.get()
    inicio_tiempo = time.time()
    resultados, tiempo = busqueda_binaria_iterativa(lista, carrera_buscar)
    fin_tiempo = time.time()
    mostrar_resultados_busqueda(resultados, carrera_buscar, tiempo, inicio_tiempo, fin_tiempo)

def buscar_recursiva():
    global lista
    archivo_csv = 'datos.csv'
    lista = convertirCSV_lista2(archivo_csv)
    lista.sort(key=lambda x: x[1])
    carrera_buscar = input_entry.get()
    inicio_tiempo = time.time()
    resultados = busqueda_binaria_recursiva(lista, carrera_buscar, 0, len(lista) - 1)
    fin_tiempo = time.time()
    mostrar_resultados_busqueda(resultados, carrera_buscar, None, inicio_tiempo, fin_tiempo)

def mostrar_resultados(tipo, inicio_tiempo, fin_tiempo):
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Resultados del {tipo}:\n\n")
    for fila_num, fila in lista:
        output_text.insert(tk.END, f"Fila {fila_num}: {fila}\n")
    tiempo_milisegundos = (fin_tiempo - inicio_tiempo) * 1000
    output_text.insert(tk.END, f"\nTiempo de {tipo}: {tiempo_milisegundos:.6f} milisegundos")
    output_text.config(state=tk.DISABLED)

def mostrar_resultados_busqueda(resultados, carrera_buscar, tiempo, inicio_tiempo, fin_tiempo):
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    if resultados:
        output_text.insert(tk.END, f"Resultados de búsqueda para '{carrera_buscar}':\n\n")
        for fila_num, profesion, nombre in resultados:
            output_text.insert(tk.END, f"Fila {fila_num}: Profesión: {profesion}, Nombre: {nombre}\n")
        if tiempo is not None:
            tiempo_milisegundos = tiempo * 1000
            output_text.insert(tk.END, f"\nTiempo de búsqueda iterativa: {tiempo_milisegundos:.6f} milisegundos")
    else:
        output_text.insert(tk.END, f"No se encontraron resultados para la profesión: {carrera_buscar}")
    tiempo_milisegundos_total = (fin_tiempo - inicio_tiempo) * 1000
    output_text.insert(tk.END, f"\nTiempo de búsqueda: {tiempo_milisegundos_total:.6f} milisegundos")
    output_text.config(state=tk.DISABLED)

# Crear la ventana
window = tk.Tk()
window.title("Programa de Búsqueda y Ordenamiento")
window.geometry("800x600")

# Componentes de la GUI
input_label = tk.Label(window, text="Profesión a buscar:")
input_label.pack(pady=10)

input_entry = tk.Entry(window)
input_entry.pack()

search_button = tk.Button(window, text="Buscar (Iterativa)", command=buscar_iterativa)
search_button.pack(pady=5)

search_recursive_button = tk.Button(window, text="Buscar (Recursiva)", command=buscar_recursiva)
search_recursive_button.pack(pady=5)

sort_insertion_button = tk.Button(window, text="Ordenar (Insertion Sort)", command=ordenar_insertion_sort)
sort_insertion_button.pack(pady=5)

sort_merge_button = tk.Button(window, text="Ordenar (Merge Sort)", command=ordenar_merge_sort)
sort_merge_button.pack(pady=5)

output_text = tk.Text(window, state=tk.DISABLED)
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

exit_button = tk.Button(window, text="Salir", command=window.quit)
exit_button.pack(pady=10)

# Iniciar la ventana principal
window.mainloop()

# Tamaños del conjunto de datos
tamanio_datos = [100, 500, 1000, 5000, 10000, 22000]

# Datos de tiempos para cada algoritmo (en segundos)
tiempo_insertion_sort = [0.5, 10, 40, 2500, 10000, 48400]
tiempo_merge_sort = [0.02, 0.2, 0.5, 5.0, 10.0, 15.0]
tiempo_busqueda_iterativa = [0.001, 0.002, 0.003, 0.01, 0.02, 0.03]
tiempo_busqueda_recursiva = [0.002, 0.003, 0.005, 0.02, 0.04, 0.06]

# Configuración de la gráfica
x = np.arange(len(tamanio_datos))
width = 0.2

fig, ax = plt.subplots(figsize=(10, 6))

# Dibujar líneas para cada conjunto de datos
ax.plot(x, tiempo_insertion_sort, label='Insertion Sort', marker='o', linestyle='-', color='b')
ax.plot(x, tiempo_merge_sort, label='Merge Sort', marker='o', linestyle='-', color='g')
ax.plot(x, tiempo_busqueda_iterativa, label='Búsqueda Iterativa', marker='o', linestyle='-', color='r')
ax.plot(x, tiempo_busqueda_recursiva, label='Búsqueda Recursiva', marker='o', linestyle='-', color='c')

# Usar escala logarítmica en el eje y
ax.set_yscale('log')

# Formatear el eje y para mostrar segundos con un decimal
def tiempo_formatter(x, pos):
    if x < 1:
        return f'{x:.1f} s'
    else:
        return f'{x:.0f} s'

formatter = FuncFormatter(tiempo_formatter)
ax.yaxis.set_major_formatter(formatter)

# Etiquetas y leyendas
ax.set_xlabel('Tamaño del Conjunto de Datos')
ax.set_ylabel('Tiempo (segundos)')
ax.set_title('Tiempos de Ejecución por Tamaño de Conjunto de Datos con Líneas (Segundos)')
ax.set_xticks(x)
ax.set_xticklabels(tamanio_datos)
ax.legend()

# Mostrar la gráfica
plt.grid()
plt.tight_layout()
plt.show()