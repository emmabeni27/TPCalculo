import numpy as np
import matplotlib.pyplot as plt

import RungeKutta

# Usamos valores de constantes universales y los datos que nos fueron asignados en la consigna
G = 6.67430e-11  # Constante gravitacional (m^3 kg^-1 s^-2)
M = 5.972e24  # Masa de la Tierra (kg)
posicion_radial_asteroide = 850750000  # Posición radial del asteroide (m)
posicion_angular_asteroide = 1.884955592  # Posición angular del asteroide (rad)

# Construímos el sistema de ecuaciones diferenciales para, luego, aplicar Runge-Kutta 4

def graficar_trayectoria(trayectoria, posicion_radial_asteroide, posicion_angular_asteroide):
    # Extraemos r y theta de la trayectoria calculada
    r = trayectoria[:,0]
    theta = trayectoria[:,1]

    # Convertimos las coordenadas polares (r, theta) a coordenadas cartesianas (x, y)
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Convertimos la posición del asteroide a coordenadas cartesianas
    x_asteroide = posicion_radial_asteroide * np.cos(posicion_angular_asteroide)
    y_asteroide = posicion_radial_asteroide * np.sin(posicion_angular_asteroide)

    # Graficamos la trayectoria del misil y la posición del asteroide
    plt.figure(figsize=(10, 10))
    plt.plot(x, y, label='Trayectoria del misil', color='blue')
    plt.scatter(x_asteroide, y_asteroide, color='red', marker='x', s=100, label='Asteroide')
    plt.xlabel('Posición X (m)')
    plt.ylabel('Posición Y (m)')
    plt.title('Trayectoria del misil hacia el asteroide')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')  # Asegura proporciones correctas en el gráfico
    plt.show()

print(f"\nAnálisis de impacto:")

# Para buscar el h (Δt óptimo) iteramos a lo largo de una lista de valores
h = [400, 300, 200, 100, 50, 40, 30, 20, 10]
velocidad_inicial = 1196.71  # m/s

for value in h:
    trayectoria = RungeKutta.simular_trayectoria(velocidad_inicial, value)
    estado_final = trayectoria[-1]

    # Verificamos impacto y mostramos el resultado
    impacto, diferencia_radial_km = RungeKutta.verificar_impacto(estado_final)

    print(f"Δt: {value}")
    if impacto:
        print("--------------------------------------------------------------------------------\n")
        print(f"¡IMPACTO EXITOSO!")
        print(f"\nResultados de la simulación:")
        print(f"Velocidad inicial: {velocidad_inicial:.2f} m/s")
        print(f"Posición radial final: {estado_final[0] / 1000:.2f} km")
        print(f"Posición angular final: {estado_final[1]:.6f} rad")
        print(f"Velocidad radial final: {estado_final[2]:.2f} m/s")
        print(f"Velocidad angular final: {estado_final[3]:.2f} m/s")
        print(f"Diferencia con el objetivo radial: {diferencia_radial_km:.2f} km\n")
        print("--------------------------------------------------------------------------------\n")
        graficar_trayectoria(trayectoria, posicion_radial_asteroide, posicion_angular_asteroide)
    else:
        print(f"NO HAY IMPACTO")
        print(f"Diferencia con el objetivo radial: {diferencia_radial_km:.2f} km \n")
