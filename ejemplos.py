"""
Ejemplos Adicionales de Uso del Árbol de Segmentos de Varianzas
================================================================

Este archivo contiene ejemplos más avanzados y casos de uso específicos
del árbol de segmentos que mantiene varianzas.
"""

from segment_tree_variance import SegmentTreeVariance
import random


def ejemplo_datos_sensores():
    """
    Ejemplo: Análisis de datos de sensores de temperatura.

    Contexto: Tenemos lecturas de temperatura de un sensor a lo largo del día
    y queremos consultar la variabilidad (varianza) en diferentes períodos.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO: Análisis de Datos de Sensores de Temperatura")
    print("=" * 70)

    # Temperaturas por hora (24 lecturas)
    temperaturas = [18, 17, 16, 15, 16, 18, 20, 22, 25, 27, 29, 30,
                    31, 32, 31, 30, 28, 26, 24, 22, 21, 20, 19, 18]

    st = SegmentTreeVariance(temperaturas)

    print(f"\nTemperaturas registradas: {temperaturas}")
    print("\nAnálisis por períodos del día:")

    periodos = [
        ("Madrugada (0-5h)", 0, 5),
        ("Mañana (6-11h)", 6, 11),
        ("Tarde (12-17h)", 12, 17),
        ("Noche (18-23h)", 18, 23),
    ]

    for nombre, inicio, fin in periodos:
        media = st.query_mean(inicio, fin)
        varianza = st.query_variance(inicio, fin)
        desv_std = varianza ** 0.5

        print(f"\n{nombre}:")
        print(f"  Temperatura media: {media:.2f}°C")
        print(f"  Varianza: {varianza:.4f}")
        print(f"  Desviación estándar: {desv_std:.2f}°C")

    # Simular un error en el sensor y corregirlo
    print("\n\nSimulación de corrección de error:")
    print(f"Temperatura en hora 15 (índice 15): {temperaturas[15]}°C")
    print("Se detecta que el sensor tuvo un error y la temperatura real era 33°C")

    var_antes = st.query_variance(12, 17)
    st.update(15, 33)
    var_despues = st.query_variance(12, 17)

    print(f"Varianza de la tarde antes de corrección: {var_antes:.4f}")
    print(f"Varianza de la tarde después de corrección: {var_despues:.4f}")


def ejemplo_calificaciones():
    """
    Ejemplo: Sistema de análisis de calificaciones de estudiantes.

    Contexto: Análisis de la dispersión de calificaciones en diferentes
    secciones de un examen.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO: Análisis de Calificaciones")
    print("=" * 70)

    # Calificaciones de 20 estudiantes
    calificaciones = [85, 90, 78, 92, 88, 76, 95, 89, 91, 87,
                     82, 94, 88, 90, 86, 93, 79, 91, 88, 84]

    st = SegmentTreeVariance(calificaciones)

    print(f"\nCalificaciones: {calificaciones}")
    print(f"Número de estudiantes: {len(calificaciones)}")

    # Análisis general
    media_total = st.query_mean(0, len(calificaciones) - 1)
    var_total = st.query_variance(0, len(calificaciones) - 1)
    desv_std_total = var_total ** 0.5

    print(f"\nEstadísticas generales:")
    print(f"  Media: {media_total:.2f}")
    print(f"  Varianza: {var_total:.4f}")
    print(f"  Desviación estándar: {desv_std_total:.2f}")

    # Dividir en grupos
    print(f"\nAnálisis por grupos de 5 estudiantes:")
    for i in range(0, len(calificaciones), 5):
        fin = min(i + 4, len(calificaciones) - 1)
        media = st.query_mean(i, fin)
        varianza = st.query_variance(i, fin)
        print(f"  Grupo {i//5 + 1} (estudiantes {i+1}-{fin+1}): Media={media:.2f}, Varianza={varianza:.4f}")


def ejemplo_finanzas():
    """
    Ejemplo: Análisis de volatilidad de precios de acciones.

    Contexto: La varianza es una medida de volatilidad en finanzas.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO: Análisis de Volatilidad Financiera")
    print("=" * 70)

    # Precios de cierre diarios de una acción (30 días)
    precios = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109,
              111, 110, 112, 115, 114, 116, 115, 117, 119, 118,
              120, 122, 121, 123, 125, 124, 126, 128, 127, 129]

    st = SegmentTreeVariance(precios)

    print(f"\nPrecios de cierre (30 días): {precios}")

    # Análisis de volatilidad por semanas
    print("\nVolatilidad por semana (5 días hábiles):")
    for semana in range(6):
        inicio = semana * 5
        fin = min(inicio + 4, len(precios) - 1)

        if inicio >= len(precios):
            break

        media = st.query_mean(inicio, fin)
        varianza = st.query_variance(inicio, fin)
        volatilidad = (varianza ** 0.5) / media * 100  # Coeficiente de variación

        print(f"  Semana {semana + 1}: Precio promedio=${media:.2f}, "
              f"Varianza={varianza:.2f}, Volatilidad={volatilidad:.2f}%")

    # Comparar primera y última semana
    var_primera = st.query_variance(0, 4)
    var_ultima = st.query_variance(25, 29)

    print(f"\nComparación de volatilidad:")
    print(f"  Primera semana: {var_primera:.4f}")
    print(f"  Última semana: {var_ultima:.4f}")

    if var_ultima > var_primera:
        print(f"  La volatilidad aumentó en {(var_ultima/var_primera - 1) * 100:.2f}%")
    else:
        print(f"  La volatilidad disminuyó en {(1 - var_ultima/var_primera) * 100:.2f}%")


def ejemplo_rendimiento():
    """
    Ejemplo: Demostración del rendimiento del árbol de segmentos.

    Muestra cómo el árbol de segmentos es eficiente para múltiples consultas.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO: Demostración de Rendimiento")
    print("=" * 70)

    # Crear un array grande
    n = 1000
    arr = [random.randint(1, 100) for _ in range(n)]

    print(f"\nCreando árbol con {n} elementos...")
    st = SegmentTreeVariance(arr)
    print("Árbol creado exitosamente.")

    # Realizar múltiples consultas
    print(f"\nRealizando consultas de varianza:")
    consultas = [
        (0, 99, "Primer 10%"),
        (100, 299, "Elementos 100-299"),
        (500, 699, "Elementos 500-699"),
        (0, 999, "Array completo")
    ]

    for inicio, fin, descripcion in consultas:
        var = st.query_variance(inicio, fin)
        media = st.query_mean(inicio, fin)
        print(f"  {descripcion}: Media={media:.2f}, Varianza={var:.4f}")

    # Realizar actualizaciones
    print(f"\nRealizando actualizaciones:")
    actualizaciones = [100, 500, 750]
    for idx in actualizaciones:
        nuevo_valor = random.randint(1, 100)
        st.update(idx, nuevo_valor)
        print(f"  Actualizado índice {idx} a valor {nuevo_valor}")

    # Consulta después de actualizaciones
    var_final = st.query_variance(0, 999)
    print(f"\nVarianza del array completo después de actualizaciones: {var_final:.4f}")


def ejemplo_comparacion_rangos():
    """
    Ejemplo: Comparación de varianzas entre diferentes rangos.

    Útil para encontrar el rango con menor/mayor variabilidad.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO: Comparación de Varianzas entre Rangos")
    print("=" * 70)

    # Datos con diferentes patrones
    datos = [10, 11, 10, 11, 10,  # Baja varianza
             20, 40, 15, 35, 25,  # Alta varianza
             30, 31, 30, 31, 30,  # Baja varianza
             50, 10, 90, 20, 80]  # Muy alta varianza

    st = SegmentTreeVariance(datos)

    print(f"\nDatos: {datos}")

    # Dividir en grupos de 5 y comparar
    grupos = []
    for i in range(0, len(datos), 5):
        fin = min(i + 4, len(datos) - 1)
        varianza = st.query_variance(i, fin)
        media = st.query_mean(i, fin)
        grupos.append((i, fin, media, varianza))

    print("\nAnálisis de grupos:")
    for i, (inicio, fin, media, varianza) in enumerate(grupos, 1):
        elementos = datos[inicio:fin+1]
        print(f"  Grupo {i} [{inicio}-{fin}]: {elementos}")
        print(f"    Media: {media:.2f}, Varianza: {varianza:.2f}")

    # Encontrar grupo más y menos variable
    grupo_min = min(grupos, key=lambda x: x[3])
    grupo_max = max(grupos, key=lambda x: x[3])

    print(f"\nGrupo más estable (menor varianza):")
    print(f"  Rango [{grupo_min[0]}-{grupo_min[1]}]: Varianza={grupo_min[3]:.2f}")

    print(f"\nGrupo más variable (mayor varianza):")
    print(f"  Rango [{grupo_max[0]}-{grupo_max[1]}]: Varianza={grupo_max[3]:.2f}")


if __name__ == "__main__":
    # Ejecutar todos los ejemplos
    ejemplo_datos_sensores()
    ejemplo_calificaciones()
    ejemplo_finanzas()
    ejemplo_rendimiento()
    ejemplo_comparacion_rangos()

    print("\n" + "=" * 70)
    print("FIN DE LOS EJEMPLOS")
    print("=" * 70)
