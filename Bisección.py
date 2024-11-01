import numpy as np

# Constantes
G = 6.67430e-11  # Constante gravitacional (m^3 kg^-1 s^-2)
M = 5.972e24  # Masa de la Tierra (kg)
posicion_radial_asteroide = 850750000  # Posición radial del asteroide (m)
posicion_angular_asteroide = 1.884955592  # Posición angular del asteroide (rad)


def sistema_ecuaciones(t, estado):
    r, theta, vr, vtheta = estado
    drdt = vr
    dthetadt = vtheta / r
    dvrdt = -G * M / r ** 2 + (vtheta ** 2) / r
    dvthetadt = -vr * vtheta / r
    return np.array([drdt, dthetadt, dvrdt, dvthetadt])


def runge_kutta_4(f, t0, y0, h, num_steps):
    t = t0
    y = y0

    for step in range(num_steps):
        k1 = h * f(t, y)
        k2 = h * f(t + h / 2, y + k1 / 2)
        k3 = h * f(t + h / 2, y + k2 / 2)
        k4 = h * f(t + h, y + k3)
        y = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        t += h

        # Verificar si estamos en la posición angular del asteroide
        if abs(y[1] - posicion_angular_asteroide) < 0.001:
            return y

    return y


def simular_trayectoria(velocidad_inicial, h=50, num_steps=10000):
    # Condiciones iniciales
    r0 = 415000000  # Posición radial inicial del satélite (m)
    theta0 = 0  # Posición angular inicial del satélite
    vr0 = velocidad_inicial  # Velocidad radial inicial (velocidad de lanzamiento)
    vtheta0 = 0  # Velocidad angular inicial
    estado_inicial = np.array([r0, theta0, vr0, vtheta0])

    # Ejecutar la simulación hasta la posición angular del asteroide
    estado_final = runge_kutta_4(sistema_ecuaciones, 0, estado_inicial, h, num_steps)
    return estado_final


def encontrar_velocidad_lanzamiento(v_min=0, v_max=15000, tolerancia=0.1):
    iteracion = 1

    while True:
        velocidad_lanzamiento = (v_min + v_max) / 2
        estado_final = simular_trayectoria(velocidad_lanzamiento)
        diferencia = estado_final[0] - posicion_radial_asteroide

        print(f"\nIteración {iteracion}:")
        print(f"Velocidad de lanzamiento: {velocidad_lanzamiento:.2f} m/s")
        print(f"Posición radial alcanzada: {estado_final[0] / 1000:.2f} km")
        print(f"Diferencia con objetivo: {diferencia / 1000:.2f} km")

        # Criterio de convergencia
        if abs(diferencia) < 1000:  # Precisión de 1 km
            return velocidad_lanzamiento, estado_final

        # Ajustar intervalo de búsqueda
        if diferencia > 0:  # El misil se pasa
            v_max = velocidad_lanzamiento
        else:  # El misil se queda corto
            v_min = velocidad_lanzamiento

        # Verificar si hemos alcanzado la precisión deseada en velocidad
        if v_max - v_min < tolerancia:
            return velocidad_lanzamiento, estado_final

        iteracion += 1


# Buscar la velocidad de lanzamiento
print("Buscando velocidad de lanzamiento para impacto...")
velocidad_lanzamiento, estado_final = encontrar_velocidad_lanzamiento()

# Mostrar resultados finales
print("\nRESULTADOS FINALES:")
print(f"Velocidad de lanzamiento necesaria: {velocidad_lanzamiento:.2f} m/s")
print("\nCondiciones en el punto de encuentro:")
print(f"Posición radial: {estado_final[0] / 1000:.2f} km")
print(f"Posición angular: {estado_final[1]:.6f} rad")
print(f"Velocidad radial final: {estado_final[2] / 1000:.2f} km/s")
print(f"Velocidad angular final: {estado_final[3] / 1000:.2f} km/s")

# Calcular error de impacto
error = abs(estado_final[0] - posicion_radial_asteroide) / 1000
print(f"\nPrecisión del impacto: {error:.3f} km")

if error < 1:
    print("\n¡IMPACTO CONFIRMADO!")
    print(f"Con una velocidad inicial de {velocidad_lanzamiento:.2f} m/s el misil impactará el asteroide")
else:
    print("\nNo se logró la precisión deseada")