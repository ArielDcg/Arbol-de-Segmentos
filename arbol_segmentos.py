"""
Árbol de Segmentos para Mantener Varianzas de Intervalos
=========================================================

Implementación completa de un árbol de segmentos que mantiene y consulta
la varianza de intervalos usando la fórmula compacta: Var(X) = E[X²] - (E[X])²

Incluye:
- Clase Node y SegmentTreeVariance
- Función de visualización gráfica
- Ejemplos prácticos del mundo real

Autor: Estructuras de Datos
"""

import random


class Node:
    """Nodo del árbol de segmentos que almacena información agregada del intervalo."""

    def __init__(self, suma=0, suma_cuadrados=0, count=0):
        self.suma = suma
        self.suma_cuadrados = suma_cuadrados
        self.count = count

    def get_variance(self):
        """Calcula varianza usando fórmula compacta: Var(X) = E[X²] - (E[X])²"""
        if self.count == 0:
            return 0
        media = self.suma / self.count
        media_cuadrados = self.suma_cuadrados / self.count
        varianza = media_cuadrados - (media * media)
        return max(0, varianza)

    def get_mean(self):
        """Calcula la media del intervalo."""
        if self.count == 0:
            return 0
        return self.suma / self.count

    def __repr__(self):
        return f"Node(suma={self.suma}, suma²={self.suma_cuadrados}, n={self.count}, var={self.get_variance():.2f})"


class SegmentTreeVariance:
    """
    Árbol de Segmentos que mantiene varianzas de intervalos.

    Complejidades:
    - Construcción: O(n)
    - Consulta: O(log n)
    - Actualización: O(log n)
    """

    def __init__(self, arr):
        """Inicializa el árbol de segmentos con un array dado."""
        self.arr = arr[:]
        self.n = len(arr)
        self.tree = [Node() for _ in range(4 * self.n)]
        if self.n > 0:
            self._build(0, 0, self.n - 1)

    def _merge(self, left_node, right_node):
        """Combina dos nodos hijos para crear el nodo padre."""
        return Node(
            suma=left_node.suma + right_node.suma,
            suma_cuadrados=left_node.suma_cuadrados + right_node.suma_cuadrados,
            count=left_node.count + right_node.count
        )

    def _build(self, node_idx, left, right):
        """Construye el árbol de segmentos recursivamente."""
        if left == right:
            value = self.arr[left]
            self.tree[node_idx] = Node(suma=value, suma_cuadrados=value * value, count=1)
            return

        mid = (left + right) // 2
        left_child = 2 * node_idx + 1
        right_child = 2 * node_idx + 2

        self._build(left_child, left, mid)
        self._build(right_child, mid + 1, right)
        self.tree[node_idx] = self._merge(self.tree[left_child], self.tree[right_child])

    def update(self, index, new_value):
        """Actualiza el valor en una posición. Complejidad: O(log n)"""
        if index < 0 or index >= self.n:
            raise IndexError(f"Índice {index} fuera de rango [0, {self.n-1}]")
        self.arr[index] = new_value
        self._update_recursive(0, 0, self.n - 1, index, new_value)

    def _update_recursive(self, node_idx, left, right, target_idx, new_value):
        if left == right:
            self.tree[node_idx] = Node(suma=new_value, suma_cuadrados=new_value * new_value, count=1)
            return

        mid = (left + right) // 2
        left_child = 2 * node_idx + 1
        right_child = 2 * node_idx + 2

        if target_idx <= mid:
            self._update_recursive(left_child, left, mid, target_idx, new_value)
        else:
            self._update_recursive(right_child, mid + 1, right, target_idx, new_value)

        self.tree[node_idx] = self._merge(self.tree[left_child], self.tree[right_child])

    def query_variance(self, query_left, query_right):
        """Consulta la varianza de un rango. Complejidad: O(log n)"""
        if query_left < 0 or query_right >= self.n or query_left > query_right:
            raise ValueError(f"Rango inválido [{query_left}, {query_right}]")
        result_node = self._query_recursive(0, 0, self.n - 1, query_left, query_right)
        return result_node.get_variance()

    def query_mean(self, query_left, query_right):
        """Consulta la media de un rango. Complejidad: O(log n)"""
        if query_left < 0 or query_right >= self.n or query_left > query_right:
            raise ValueError(f"Rango inválido [{query_left}, {query_right}]")
        result_node = self._query_recursive(0, 0, self.n - 1, query_left, query_right)
        return result_node.get_mean()

    def query_sum(self, query_left, query_right):
        """Consulta la suma de un rango. Complejidad: O(log n)"""
        if query_left < 0 or query_right >= self.n or query_left > query_right:
            raise ValueError(f"Rango inválido [{query_left}, {query_right}]")
        result_node = self._query_recursive(0, 0, self.n - 1, query_left, query_right)
        return result_node.suma

    def _query_recursive(self, node_idx, left, right, query_left, query_right):
        """Consulta recursiva con tres casos: sin solapamiento, total, parcial."""
        # Sin solapamiento
        if query_right < left or query_left > right:
            return Node()
        # Solapamiento total
        if query_left <= left and right <= query_right:
            return self.tree[node_idx]
        # Solapamiento parcial
        mid = (left + right) // 2
        left_child = 2 * node_idx + 1
        right_child = 2 * node_idx + 2
        left_result = self._query_recursive(left_child, left, mid, query_left, query_right)
        right_result = self._query_recursive(right_child, mid + 1, right, query_left, query_right)
        return self._merge(left_result, right_result)

    def get_array(self):
        """Retorna una copia del array actual."""
        return self.arr[:]

    def print_tree(self, node_idx=0, level=0, left=None, right=None):
        """Imprime el árbol de segmentos de manera visual."""
        if left is None:
            left = 0
        if right is None:
            right = self.n - 1
        if left > right:
            return

        indent = "  " * level
        node = self.tree[node_idx]
        print(f"{indent}[{left},{right}]: {node}")

        if left < right:
            mid = (left + right) // 2
            self.print_tree(2 * node_idx + 1, level + 1, left, mid)
            self.print_tree(2 * node_idx + 2, level + 1, mid + 1, right)


def visualizar_arbol(arr, output_file='arbol_visualizacion.png'):
    """
    Genera una visualización gráfica del árbol de segmentos.

    Requiere matplotlib. Instalar con: pip install matplotlib

    Args:
        arr: Array de datos
        output_file: Nombre del archivo de salida
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        import math
    except ImportError:
        print("Error: matplotlib no está instalado.")
        print("Instala con: pip install matplotlib")
        return

    st = SegmentTreeVariance(arr)
    n = len(arr)
    height = math.ceil(math.log2(n)) + 1 if n > 0 else 1

    fig_width = max(12, n * 1.5)
    fig_height = max(8, height * 2)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    def draw_node(node_idx, left, right, x, y, level):
        if left > right or node_idx >= len(st.tree):
            return

        node = st.tree[node_idx]
        box_width, box_height = 2.5, 1.2
        color = '#FFE8E8' if left == right else '#E8F4F8'

        rect = patches.FancyBboxPatch(
            (x - box_width/2, y - box_height/2), box_width, box_height,
            boxstyle="round,pad=0.1", linewidth=2,
            edgecolor='#2C3E50', facecolor=color
        )
        ax.add_patch(rect)

        info_text = f"[{left},{right}]\\nΣ={node.suma:.0f}\\nΣ²={node.suma_cuadrados:.0f}\\nVar={node.get_variance():.2f}"
        ax.text(x, y, info_text, ha='center', va='center', fontsize=9, fontweight='bold', color='#2C3E50')

        if left < right:
            mid = (left + right) // 2
            horizontal_spacing = fig_width / (2 ** (level + 2))
            vertical_spacing = 2.5
            left_x, right_x = x - horizontal_spacing, x + horizontal_spacing
            child_y = y - vertical_spacing

            ax.plot([x, left_x], [y - box_height/2, child_y + box_height/2], linewidth=2, color='#34495E')
            ax.plot([x, right_x], [y - box_height/2, child_y + box_height/2], linewidth=2, color='#34495E')

            draw_node(2 * node_idx + 1, left, mid, left_x, child_y, level + 1)
            draw_node(2 * node_idx + 2, mid + 1, right, right_x, child_y, level + 1)

    array_y = height * 2.5
    ax.text(fig_width / 2, array_y + 1, f"Array Original: {arr}",
            ha='center', va='center', fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='#FFF9E6', edgecolor='#F39C12', linewidth=2))

    draw_node(0, 0, n - 1, fig_width / 2, array_y - 2, 0)

    ax.text(fig_width / 2, array_y + 2.5, 'Árbol de Segmentos para Varianzas',
            ha='center', va='center', fontsize=16, fontweight='bold', color='#2C3E50')
    ax.text(1, -1, 'Σ = Suma\\nΣ² = Suma de cuadrados\\nVar = Varianza',
            ha='left', va='top', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='#F8F9FA', edgecolor='#95A5A6', linewidth=1))

    ax.set_xlim(0, fig_width)
    ax.set_ylim(-2, array_y + 3)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Visualización guardada: {output_file}")


# ==================== EJEMPLOS ====================

def ejemplo_basico():
    """Ejemplo 1: Construcción y consultas básicas"""
    print("=" * 70)
    print("EJEMPLO 1: Construcción y Consultas Básicas")
    print("=" * 70)

    arr = [4, 8, 6, 2, 10, 12, 14, 16]
    print(f"Array: {arr}")

    st = SegmentTreeVariance(arr)

    print("\\nConsultas de varianza:")
    for l, r in [(0, 3), (2, 5), (0, 7), (4, 7)]:
        var = st.query_variance(l, r)
        mean = st.query_mean(l, r)
        print(f"  [{l},{r}]: elementos={arr[l:r+1]} -> Media={mean:.2f}, Var={var:.4f}")


def ejemplo_sensores():
    """Ejemplo 2: Análisis de datos de sensores de temperatura"""
    print("\\n" + "=" * 70)
    print("EJEMPLO 2: Análisis de Sensores de Temperatura")
    print("=" * 70)

    temperaturas = [18, 17, 16, 15, 16, 18, 20, 22, 25, 27, 29, 30,
                    31, 32, 31, 30, 28, 26, 24, 22, 21, 20, 19, 18]
    st = SegmentTreeVariance(temperaturas)

    print(f"Temperaturas (24h): {temperaturas}")
    print("\\nAnálisis por períodos:")

    periodos = [("Madrugada", 0, 5), ("Mañana", 6, 11), ("Tarde", 12, 17), ("Noche", 18, 23)]
    for nombre, inicio, fin in periodos:
        media = st.query_mean(inicio, fin)
        var = st.query_variance(inicio, fin)
        print(f"  {nombre:12s}: Media={media:5.2f}°C, Varianza={var:6.4f}, Desv.Est={var**0.5:5.2f}°C")


def ejemplo_calificaciones():
    """Ejemplo 3: Análisis de calificaciones"""
    print("\\n" + "=" * 70)
    print("EJEMPLO 3: Análisis de Calificaciones")
    print("=" * 70)

    calif = [85, 90, 78, 92, 88, 76, 95, 89, 91, 87, 82, 94, 88, 90, 86, 93, 79, 91, 88, 84]
    st = SegmentTreeVariance(calif)

    media = st.query_mean(0, len(calif) - 1)
    var = st.query_variance(0, len(calif) - 1)
    print(f"Calificaciones: {calif}")
    print(f"Estadísticas: Media={media:.2f}, Varianza={var:.4f}, Desv.Est={var**0.5:.2f}")

    print("\\nPor grupos de 5:")
    for i in range(0, len(calif), 5):
        fin = min(i + 4, len(calif) - 1)
        print(f"  Grupo {i//5 + 1}: Media={st.query_mean(i, fin):.2f}, Var={st.query_variance(i, fin):.4f}")


def ejemplo_finanzas():
    """Ejemplo 4: Análisis de volatilidad financiera"""
    print("\\n" + "=" * 70)
    print("EJEMPLO 4: Volatilidad Financiera")
    print("=" * 70)

    precios = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109,
               111, 110, 112, 115, 114, 116, 115, 117, 119, 118,
               120, 122, 121, 123, 125, 124, 126, 128, 127, 129]
    st = SegmentTreeVariance(precios)

    print("Volatilidad por semana (5 días):")
    for sem in range(6):
        inicio = sem * 5
        fin = min(inicio + 4, len(precios) - 1)
        if inicio >= len(precios):
            break
        media = st.query_mean(inicio, fin)
        var = st.query_variance(inicio, fin)
        volatilidad = (var ** 0.5) / media * 100
        print(f"  Semana {sem + 1}: Precio=${media:.2f}, Var={var:.2f}, Volatilidad={volatilidad:.2f}%")


def ejemplo_actualizaciones():
    """Ejemplo 5: Actualizaciones dinámicas"""
    print("\\n" + "=" * 70)
    print("EJEMPLO 5: Actualizaciones Dinámicas")
    print("=" * 70)

    arr = [10, 20, 30, 40, 50]
    st = SegmentTreeVariance(arr)

    print(f"Array inicial: {st.get_array()}")
    print(f"Varianza inicial: {st.query_variance(0, 4):.4f}")

    updates = [(0, 30), (4, 30)]
    for idx, val in updates:
        st.update(idx, val)
        print(f"Después update({idx}, {val}): {st.get_array()}, Var={st.query_variance(0, 4):.4f}")


def main():
    """Función principal que ejecuta todos los ejemplos"""
    print("\\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 12 + "ÁRBOL DE SEGMENTOS PARA VARIANZAS" + " " * 23 + "║")
    print("║" + " " * 20 + "Fórmula: Var(X) = E[X²] - (E[X])²" + " " * 15 + "║")
    print("╚" + "=" * 68 + "╝")

    ejemplo_basico()
    ejemplo_sensores()
    ejemplo_calificaciones()
    ejemplo_finanzas()
    ejemplo_actualizaciones()

    print("\\n" + "=" * 70)
    print("Para visualización gráfica, ejecuta:")
    print("  >>> from arbol_segmentos import visualizar_arbol")
    print("  >>> visualizar_arbol([4, 8, 6, 2])")
    print("=" * 70 + "\\n")


if __name__ == "__main__":
    main()
