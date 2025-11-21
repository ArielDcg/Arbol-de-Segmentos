"""
Script para visualizar el árbol de segmentos de varianzas
Genera una imagen PNG mostrando la estructura del árbol
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from segment_tree_variance import SegmentTreeVariance


def draw_segment_tree(arr, output_file='segment_tree_visualization.png'):
    """
    Dibuja una visualización del árbol de segmentos.

    Args:
        arr: Array de datos para construir el árbol
        output_file: Nombre del archivo de salida
    """
    st = SegmentTreeVariance(arr)
    n = len(arr)

    # Calcular la altura del árbol
    import math
    height = math.ceil(math.log2(n)) + 1 if n > 0 else 1

    # Configurar el tamaño de la figura
    fig_width = max(12, n * 1.5)
    fig_height = max(8, height * 2)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # Función para dibujar un nodo
    def draw_node(node_idx, left, right, x, y, level, max_level):
        if left > right or node_idx >= len(st.tree):
            return

        node = st.tree[node_idx]

        # Dimensiones del nodo
        box_width = 2.5
        box_height = 1.2

        # Dibujar el rectángulo del nodo
        color = '#E8F4F8'  # Azul claro
        if left == right:
            color = '#FFE8E8'  # Rosa claro para hojas

        rect = patches.FancyBboxPatch(
            (x - box_width/2, y - box_height/2),
            box_width, box_height,
            boxstyle="round,pad=0.1",
            linewidth=2,
            edgecolor='#2C3E50',
            facecolor=color
        )
        ax.add_patch(rect)

        # Texto del nodo
        range_text = f"[{left},{right}]"
        variance = node.get_variance()

        # Información del nodo
        info_text = f"{range_text}\n"
        info_text += f"Σ={node.suma:.0f}\n"
        info_text += f"Σ²={node.suma_cuadrados:.0f}\n"
        info_text += f"Var={variance:.2f}"

        ax.text(x, y, info_text,
               ha='center', va='center',
               fontsize=9, fontweight='bold',
               color='#2C3E50')

        # Dibujar conexiones a hijos
        if left < right:
            mid = (left + right) // 2
            left_child_idx = 2 * node_idx + 1
            right_child_idx = 2 * node_idx + 2

            # Calcular posiciones de los hijos
            horizontal_spacing = fig_width / (2 ** (level + 2))
            vertical_spacing = 2.5

            left_x = x - horizontal_spacing
            right_x = x + horizontal_spacing
            child_y = y - vertical_spacing

            # Dibujar líneas a los hijos
            ax.plot([x, left_x], [y - box_height/2, child_y + box_height/2],
                   'k-', linewidth=2, color='#34495E')
            ax.plot([x, right_x], [y - box_height/2, child_y + box_height/2],
                   'k-', linewidth=2, color='#34495E')

            # Recursivamente dibujar hijos
            draw_node(left_child_idx, left, mid, left_x, child_y, level + 1, max_level)
            draw_node(right_child_idx, mid + 1, right, right_x, child_y, level + 1, max_level)

    # Dibujar el array original en la parte superior
    array_y = height * 2.5
    ax.text(fig_width / 2, array_y + 1, f"Array Original: {arr}",
           ha='center', va='center',
           fontsize=12, fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='#FFF9E6', edgecolor='#F39C12', linewidth=2))

    # Comenzar a dibujar desde la raíz
    root_y = array_y - 2
    draw_node(0, 0, n - 1, fig_width / 2, root_y, 0, height)

    # Agregar título
    ax.text(fig_width / 2, array_y + 2.5,
           'Árbol de Segmentos para Varianzas de Intervalos',
           ha='center', va='center',
           fontsize=16, fontweight='bold',
           color='#2C3E50')

    # Agregar leyenda
    legend_y = -1
    ax.text(1, legend_y,
           'Σ = Suma de elementos\nΣ² = Suma de cuadrados\nVar = Varianza del intervalo',
           ha='left', va='top',
           fontsize=10,
           bbox=dict(boxstyle='round', facecolor='#F8F9FA', edgecolor='#95A5A6', linewidth=1))

    # Configurar los ejes
    ax.set_xlim(0, fig_width)
    ax.set_ylim(-2, array_y + 3)
    ax.axis('off')

    # Ajustar el layout y guardar
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Visualización guardada en: {output_file}")

    return output_file


def create_example_visualizations():
    """
    Crea varias visualizaciones de ejemplo.
    """
    # Ejemplo 1: Array simple pequeño
    print("Generando visualización 1: Array simple [4, 8, 6, 2]")
    arr1 = [4, 8, 6, 2]
    draw_segment_tree(arr1, 'tree_example_small.png')

    # Ejemplo 2: Array más grande
    print("\nGenerando visualización 2: Array [5, 3, 7, 2, 8, 4, 1, 6]")
    arr2 = [5, 3, 7, 2, 8, 4, 1, 6]
    draw_segment_tree(arr2, 'tree_example_medium.png')

    print("\n¡Visualizaciones generadas exitosamente!")


if __name__ == "__main__":
    create_example_visualizations()
