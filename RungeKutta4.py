import numpy as np

#Calculamos la velocidad de lanzamiento de un misil desde un satélite que orbita la Tierra para que impacte y desvíe el meteorito.

# Usamos valores de constantes universales y los datos que nos fueron asignados en la consigna
G = 6.67430e-11  # Constante gravitacional (m^3 kg^-1 s^-2)
M = 5.972e24  # Masa de la Tierra (kg)
posicion_radial_asteroide = 850750000  # Posición radial del asteroide (m)
posicion_angular_asteroide = 1.884955592  # Posición angular del asteroide (rad)

#Construímos el sistema de ecuaciones diferenciales para, luego, aplicar Runge-Kutta 4
def sistema_ecuaciones(t, estado):
    r, theta, vr, vtheta = estado
    drdt = vr
    dthetadt = vtheta / r
    dvrdt = -G * M / r ** 2 + (vtheta ** 2) / r
    dvthetadt = -vr * vtheta / r
    return np.array([drdt, dthetadt, dvrdt, dvthetadt])

#Aplicamos Runge-Kutta 4
def runge_kutta_4(f, t0, y0, h, num_steps):
    t = t0
    y = y0

    for _ in range(num_steps):
        k1 = h * f(t, y)
        k2 = h * f(t + h / 2, y + k1 / 2)
        k3 = h * f(t + h / 2, y + k2 / 2)
        k4 = h * f(t + h, y + k3)
        y = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        t += h
    return y


def simular_trayectoria(v0, h, num_steps=10000):
    r0 = 415000000  # Posición radial inicial del satélite (m)
    theta0 = 0  # Posición angular inicial del satélite
    vr0 = v0  # Velocidad radial inicial
    vtheta0 = 0  # Velocidad angular inicial
    estado_inicial = np.array([r0, theta0, vr0, vtheta0])

    # Ejecutamos la simulacion para ver si, para un determinado valor de h, hay impacto con el asteroide
    estado_final = runge_kutta_4(sistema_ecuaciones, 0, estado_inicial, h, num_steps)
    return estado_final

#El método siguiente determina si se produce un impacto entre el misil y el asteroide, o no
def verificar_impacto(estado_final, tolerancia_radial=10000):  # tolerancia de 10 km
    r_final = estado_final[0]

    # Calculamos la diferencia radial
    diferencia_radial = abs(r_final - posicion_radial_asteroide)

    # Verificamos que el valor se encuentre dentro del rango de tolerancia
    impacto = diferencia_radial < tolerancia_radial

    return impacto, diferencia_radial / 1000  # Convertimos a km

    #Para buscar el h (Δt óptimo) iteramos a lo largo de una lista de valores
h = [1000, 900, 800, 700, 600, 500, 400, 300, 200, 100, 50, 40, 30, 20, 10, 1, 0.1, 0.01, 0.001]
for value in h:
    # Ejecutamos la simulación para el valor de v0 encontrado con el método de secantes que nos asegura un impacto
    velocidad_inicial = 1196.71  # m/s
    estado_final = simular_trayectoria(velocidad_inicial, value)

    #Verificamos impacto y mostramos el resultado
    impacto, diferencia_radial_km = verificar_impacto(estado_final)

    print(f"\nResultados de la simulación:")
    print(f"Velocidad inicial: {velocidad_inicial:.2f} m/s")
    print(f"Posición radial final: {estado_final[0] / 1000:.2f} km")
    print(f"Posición angular final: {estado_final[1]:.6f} rad")
    print(f"Velocidad radial final: {estado_final[2]:.2f} m/s")
    print(f"Velocidad angular final: {estado_final[3]:.2f} m/s")

    print(f"\nAnálisis de impacto:")
    print(f"Δt: {value}")
    if impacto:
        print(f"¡IMPACTO EXITOSO!")
        print(f"Diferencia con el objetivo radial: {diferencia_radial_km:.2f} km")
    else:
        print(f"NO HAY IMPACTO")
        print(f"Diferencia con el objetivo radial: {diferencia_radial_km:.2f} km")
