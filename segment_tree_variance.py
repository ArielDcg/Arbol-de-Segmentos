"""
Árbol de Segmentos para Mantener Varianzas de Intervalos
=========================================================

Este módulo implementa un árbol de segmentos que mantiene y consulta
la varianza de intervalos de manera eficiente.

Autor: Estructuras de Datos
Fecha: 2025
"""


class Node:
    """
    Clase que representa un nodo del árbol de segmentos.

    Atributos:
        suma: Suma de todos los elementos en el intervalo
        suma_cuadrados: Suma de los cuadrados de los elementos
        count: Cantidad de elementos en el intervalo
    """

    def __init__(self, suma=0, suma_cuadrados=0, count=0):
        """
        Inicializa un nodo del árbol.

        Args:
            suma: Suma inicial de elementos
            suma_cuadrados: Suma inicial de cuadrados
            count: Cantidad inicial de elementos
        """
        self.suma = suma
        self.suma_cuadrados = suma_cuadrados
        self.count = count

    def get_variance(self):
        """
        Calcula la varianza usando la fórmula compacta.

        Fórmula: Var(X) = E[X²] - (E[X])²
        Donde:
            E[X²] = suma_cuadrados / count
            E[X] = suma / count

        Returns:
            float: La varianza del intervalo
        """
        if self.count == 0:
            return 0

        # E[X²] - (E[X])²
        media = self.suma / self.count
        media_cuadrados = self.suma_cuadrados / self.count
        varianza = media_cuadrados - (media * media)

        # Corrección por errores de punto flotante
        return max(0, varianza)

    def get_mean(self):
        """
        Calcula la media del intervalo.

        Returns:
            float: La media del intervalo
        """
        if self.count == 0:
            return 0
        return self.suma / self.count

    def __repr__(self):
        """Representación en string del nodo."""
        return f"Node(suma={self.suma}, suma_cuad={self.suma_cuadrados}, count={self.count}, var={self.get_variance():.4f})"


class SegmentTreeVariance:
    """
    Árbol de Segmentos que mantiene varianzas de intervalos.

    Esta estructura permite:
    - Construcción en O(n)
    - Actualización de elementos en O(log n)
    - Consulta de varianza de un rango en O(log n)

    Atributos:
        arr: Array original de datos
        n: Tamaño del array
        tree: Array que representa el árbol de segmentos
    """

    def __init__(self, arr):
        """
        Inicializa el árbol de segmentos con un array dado.

        Args:
            arr: Lista de números para construir el árbol
        """
        self.arr = arr[:]  # Copia del array original
        self.n = len(arr)
        # El árbol necesita 4*n nodos en el peor caso
        self.tree = [Node() for _ in range(4 * self.n)]

        if self.n > 0:
            self._build(0, 0, self.n - 1)

    def _merge(self, left_node, right_node):
        """
        Combina dos nodos hijos para crear el nodo padre.

        La operación de merge suma los valores acumulados:
        - suma total = suma_izq + suma_der
        - suma_cuadrados total = suma_cuad_izq + suma_cuad_der
        - count total = count_izq + count_der

        Args:
            left_node: Nodo hijo izquierdo
            right_node: Nodo hijo derecho

        Returns:
            Node: Nodo resultante de la combinación
        """
        return Node(
            suma=left_node.suma + right_node.suma,
            suma_cuadrados=left_node.suma_cuadrados + right_node.suma_cuadrados,
            count=left_node.count + right_node.count
        )

    def _build(self, node_idx, left, right):
        """
        Construye el árbol de segmentos de manera recursiva.

        Proceso:
        1. Si es una hoja, guarda el elemento directamente
        2. Si no, divide el rango en dos mitades
        3. Construye recursivamente los hijos izquierdo y derecho
        4. Combina los resultados de los hijos usando merge

        Args:
            node_idx: Índice del nodo actual en el árbol
            left: Límite izquierdo del intervalo
            right: Límite derecho del intervalo
        """
        # Caso base: nodo hoja
        if left == right:
            value = self.arr[left]
            self.tree[node_idx] = Node(
                suma=value,
                suma_cuadrados=value * value,
                count=1
            )
            return

        # Caso recursivo: dividir el intervalo
        mid = (left + right) // 2
        left_child = 2 * node_idx + 1
        right_child = 2 * node_idx + 2

        # Construir subárboles
        self._build(left_child, left, mid)
        self._build(right_child, mid + 1, right)

        # Combinar resultados
        self.tree[node_idx] = self._merge(
            self.tree[left_child],
            self.tree[right_child]
        )

    def update(self, index, new_value):
        """
        Actualiza el valor en una posición específica.

        Proceso:
        1. Actualiza el array original
        2. Recorre el árbol desde la raíz hasta la hoja
        3. Actualiza todos los nodos en el camino

        Complejidad: O(log n)

        Args:
            index: Índice del elemento a actualizar (0-indexed)
            new_value: Nuevo valor a asignar

        Raises:
            IndexError: Si el índice está fuera de rango
        """
        if index < 0 or index >= self.n:
            raise IndexError(f"Índice {index} fuera de rango [0, {self.n-1}]")

        self.arr[index] = new_value
        self._update_recursive(0, 0, self.n - 1, index, new_value)

    def _update_recursive(self, node_idx, left, right, target_idx, new_value):
        """
        Función auxiliar recursiva para actualizar el árbol.

        Args:
            node_idx: Índice del nodo actual
            left: Límite izquierdo del intervalo del nodo
            right: Límite derecho del intervalo del nodo
            target_idx: Índice a actualizar
            new_value: Nuevo valor
        """
        # Caso base: nodo hoja
        if left == right:
            self.tree[node_idx] = Node(
                suma=new_value,
                suma_cuadrados=new_value * new_value,
                count=1
            )
            return

        # Caso recursivo: determinar qué subárbol actualizar
        mid = (left + right) // 2
        left_child = 2 * node_idx + 1
        right_child = 2 * node_idx + 2

        if target_idx <= mid:
            self._update_recursive(left_child, left, mid, target_idx, new_value)
        else:
            self._update_recursive(right_child, mid + 1, right, target_idx, new_value)

        # Recalcular el nodo actual combinando sus hijos
        self.tree[node_idx] = self._merge(
            self.tree[left_child],
            self.tree[right_child]
        )

    def query_variance(self, query_left, query_right):
        """
        Consulta la varianza de un rango [query_left, query_right].

        Complejidad: O(log n)

        Args:
            query_left: Límite izquierdo del rango (0-indexed, inclusivo)
            query_right: Límite derecho del rango (0-indexed, inclusivo)

        Returns:
            float: La varianza del rango consultado

        Raises:
            ValueError: Si el rango es inválido
        """
        if query_left < 0 or query_right >= self.n or query_left > query_right:
            raise ValueError(f"Rango inválido [{query_left}, {query_right}]")

        result_node = self._query_recursive(0, 0, self.n - 1, query_left, query_right)
        return result_node.get_variance()

    def query_mean(self, query_left, query_right):
        """
        Consulta la media de un rango [query_left, query_right].

        Complejidad: O(log n)

        Args:
            query_left: Límite izquierdo del rango (0-indexed, inclusivo)
            query_right: Límite derecho del rango (0-indexed, inclusivo)

        Returns:
            float: La media del rango consultado
        """
        if query_left < 0 or query_right >= self.n or query_left > query_right:
            raise ValueError(f"Rango inválido [{query_left}, {query_right}]")

        result_node = self._query_recursive(0, 0, self.n - 1, query_left, query_right)
        return result_node.get_mean()

    def query_sum(self, query_left, query_right):
        """
        Consulta la suma de un rango [query_left, query_right].

        Complejidad: O(log n)

        Args:
            query_left: Límite izquierdo del rango (0-indexed, inclusivo)
            query_right: Límite derecho del rango (0-indexed, inclusivo)

        Returns:
            float: La suma del rango consultado
        """
        if query_left < 0 or query_right >= self.n or query_left > query_right:
            raise ValueError(f"Rango inválido [{query_left}, {query_right}]")

        result_node = self._query_recursive(0, 0, self.n - 1, query_left, query_right)
        return result_node.suma

    def _query_recursive(self, node_idx, left, right, query_left, query_right):
        """
        Función auxiliar recursiva para consultar un rango.

        Casos:
        1. Sin solapamiento: retorna nodo vacío
        2. Solapamiento total: retorna el nodo actual
        3. Solapamiento parcial: divide y combina resultados

        Args:
            node_idx: Índice del nodo actual
            left: Límite izquierdo del intervalo del nodo
            right: Límite derecho del intervalo del nodo
            query_left: Límite izquierdo de la consulta
            query_right: Límite derecho de la consulta

        Returns:
            Node: Nodo con la información agregada del rango
        """
        # Caso 1: Sin solapamiento
        if query_right < left or query_left > right:
            return Node()  # Nodo vacío (elemento neutro)

        # Caso 2: Solapamiento total - el rango del nodo está completamente dentro de la consulta
        if query_left <= left and right <= query_right:
            return self.tree[node_idx]

        # Caso 3: Solapamiento parcial - dividir y conquistar
        mid = (left + right) // 2
        left_child = 2 * node_idx + 1
        right_child = 2 * node_idx + 2

        left_result = self._query_recursive(left_child, left, mid, query_left, query_right)
        right_result = self._query_recursive(right_child, mid + 1, right, query_left, query_right)

        return self._merge(left_result, right_result)

    def get_array(self):
        """
        Retorna una copia del array actual.

        Returns:
            list: Copia del array de datos
        """
        return self.arr[:]

    def print_tree(self, node_idx=0, level=0, left=None, right=None):
        """
        Imprime el árbol de segmentos de manera visual (para debugging).

        Args:
            node_idx: Índice del nodo actual
            level: Nivel de profundidad (para indentación)
            left: Límite izquierdo del rango
            right: Límite derecho del rango
        """
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


def main():
    """
    Función principal con ejemplos de uso del árbol de segmentos.
    """
    print("=" * 70)
    print("ÁRBOL DE SEGMENTOS PARA VARIANZAS DE INTERVALOS")
    print("=" * 70)
    print()

    # Ejemplo 1: Construcción básica
    print("Ejemplo 1: Construcción y consultas básicas")
    print("-" * 70)
    arr = [4, 8, 6, 2, 10, 12, 14, 16]
    print(f"Array original: {arr}")

    st = SegmentTreeVariance(arr)
    print()

    # Consultas de varianza
    print("Consultas de varianza:")
    ranges = [(0, 3), (2, 5), (0, 7), (4, 7)]
    for l, r in ranges:
        variance = st.query_variance(l, r)
        mean = st.query_mean(l, r)
        suma = st.query_sum(l, r)
        elements = arr[l:r+1]
        print(f"  Rango [{l}, {r}]: elementos={elements}")
        print(f"    -> Suma={suma:.2f}, Media={mean:.2f}, Varianza={variance:.4f}")

    print()

    # Ejemplo 2: Actualización
    print("Ejemplo 2: Actualización de valores")
    print("-" * 70)
    print(f"Array antes: {st.get_array()}")
    print(f"Varianza del rango [0, 3] antes: {st.query_variance(0, 3):.4f}")

    st.update(1, 4)  # Cambiar arr[1] de 8 a 4
    print(f"Array después de update(1, 4): {st.get_array()}")
    print(f"Varianza del rango [0, 3] después: {st.query_variance(0, 3):.4f}")

    print()

    # Ejemplo 3: Verificación con cálculo manual
    print("Ejemplo 3: Verificación de la fórmula compacta")
    print("-" * 70)
    test_arr = [2, 4, 4, 4, 5, 5, 7, 9]
    st2 = SegmentTreeVariance(test_arr)
    print(f"Array de prueba: {test_arr}")

    # Calcular varianza manualmente
    n = len(test_arr)
    suma_manual = sum(test_arr)
    suma_cuad_manual = sum(x*x for x in test_arr)
    media_manual = suma_manual / n
    media_cuad_manual = suma_cuad_manual / n
    var_manual = media_cuad_manual - (media_manual ** 2)

    var_arbol = st2.query_variance(0, n-1)

    print(f"Cálculo manual:")
    print(f"  Suma = {suma_manual}")
    print(f"  Suma de cuadrados = {suma_cuad_manual}")
    print(f"  Media = {media_manual}")
    print(f"  E[X²] = {media_cuad_manual}")
    print(f"  Varianza = E[X²] - (E[X])² = {media_cuad_manual} - {media_manual**2} = {var_manual:.6f}")
    print(f"Varianza del árbol: {var_arbol:.6f}")
    print(f"Diferencia: {abs(var_manual - var_arbol):.10f}")

    print()

    # Ejemplo 4: Múltiples actualizaciones
    print("Ejemplo 4: Múltiples actualizaciones y consultas")
    print("-" * 70)
    arr3 = [10, 20, 30, 40, 50]
    st3 = SegmentTreeVariance(arr3)
    print(f"Array inicial: {st3.get_array()}")
    print(f"Varianza [0, 4]: {st3.query_variance(0, 4):.4f}")

    updates = [(0, 30), (4, 30)]  # Hacer el array más uniforme
    for idx, val in updates:
        st3.update(idx, val)
        print(f"Después de update({idx}, {val}): {st3.get_array()}, Varianza [0, 4]: {st3.query_variance(0, 4):.4f}")

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
