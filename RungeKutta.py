import numpy as np

import RungeKutta


# Constantes
G = 6.67430e-11  # Constante gravitacional (m^3 kg^-1 s^-2)
M = 5.972e24  # Masa de la Tierra (kg)
posicion_radial_asteroide = 850750000  # Posición radial del asteroide (m)
posicion_angular_asteroide = 1.884955592  # Posición angular del asteroide (rad)

#r?s 1e7
#posic asteroide 2e7
#v0 7e3
#v1 8e3
#

def sistema_ecuaciones(t, estado):
    r, theta, vr, vtheta = estado
    drdt = vr
    dthetadt = vtheta / r
    dvrdt = -G * M / r ** 2 + (vtheta ** 2) / r
    dvthetadt = -vr * vtheta / r
    return np.array([drdt, dthetadt, dvrdt, dvthetadt])


def simular_trayectoria(velocidad_inicial, h=50, num_steps=10000):
    # Condiciones iniciales
    r0 = 415000000  # Posición radial inicial del satélite (m)
    theta0 = 0  # Posición angular inicial del satélite
    vr0 = velocidad_inicial  # Velocidad radial inicial (velocidad de lanzamiento)
    vtheta0 = 0  # Velocidad angular inicial
    estado_inicial = np.array([r0, theta0, vr0, vtheta0])

    # Ejecutar la simulación hasta la posición angular del asteroide
    estado_final = RungeKutta.runge_kutta_4(sistema_ecuaciones, 0, estado_inicial, h, num_steps)
    return estado_final

def verificar_impacto(estado_final, tolerancia_radial=10000):  # tolerancia de 10 km
    r_final = estado_final[0]

    # Calcular la diferencia radial
    diferencia_radial = abs(r_final - posicion_radial_asteroide)

    # Verificar si estamos dentro de la tolerancia
    impacto = diferencia_radial < tolerancia_radial
    return impacto, diferencia_radial / 1000  # Convertimos a km

# Ejecutar la simulación con una velocidad específica
velocidad_inicial = 1196.71   # m/s
estado_final = simular_trayectoria(velocidad_inicial)

# Verificar impacto y mostrar resultados
impacto, diferencia_radial_km = verificar_impacto(estado_final)

print(f"\nResultados de la simulación:")
print(f"Velocidad inicial: {velocidad_inicial:.2f} m/s")
print(f"Posición radial final: {estado_final[0] / 1000:.2f} km")
print(f"Posición angular final: {estado_final[1]:.6f} rad")
print(f"Velocidad radial final: {estado_final[2]:.2f} m/s")
print(f"Velocidad angular final: {estado_final[3]:.2f} m/s")

print(f"\nAnálisis de impacto:")
if impacto:
    print(f"¡IMPACTO EXITOSO!")
    print(f"Diferencia con el objetivo radial: {diferencia_radial_km:.2f} km")
else:
    print(f"NO HAY IMPACTO")
    print(f"Diferencia con el objetivo radial: {diferencia_radial_km:.2f} km")
    #distintos delta
    # #rb posicion asteoride a punto de sisparart
