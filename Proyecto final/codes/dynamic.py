import math

def solve(team_values, m, k):
    """
    Dada la lista de valores de equipos, el número de grupos m y el tamaño k de cada grupo,
    retorna una tupla (groups, cost) donde:
      - groups es una lista de listas, en donde cada sublista representa un grupo y contiene los índices (1-indexados)
        de los equipos asignados en el orden en que se completó el grupo.
      - cost es el costo total (la suma de desbalances) de la asignación óptima.
    
    Se asume que len(team_values) == m * k.
    """
    n = len(team_values)
    if n != m * k:
        raise ValueError("La cantidad de equipos debe ser igual a m * k")
    
    # Construimos la lista de equipos agrupados por valor.
    # teams_by_value[v] contendrá los índices (0-indexados inicialmente) de los equipos cuyo valor es v+1.
    teams_by_value = [[] for _ in range(5)]
    for idx, v in enumerate(team_values):
        if v < 1 or v > 5:
            raise ValueError("Todos los valores deben estar en el rango 1 a 5")
        teams_by_value[v-1].append(idx)
    
    # Calculamos la cantidad de equipos para cada valor.
    f = [len(lst) for lst in teams_by_value]
    # Suma total de valores
    T = sum(team_values)
    
    # El estado de la DP es una tupla:
    # (c1, c2, c3, c4, c5, j, s)
    # donde c1,...,c5 son la cantidad de equipos ya asignados de cada valor,
    # j es la cantidad de equipos en el grupo en construcción, y s la suma de sus valores.
    #
    # dp[t] será un diccionario que mapea estados alcanzados al asignar t equipos
    # a una tupla (cost, parent), donde 'parent' es de la forma (prev_state, decision)
    # que nos permitirá reconstruir la solución. La 'decision' se almacenará como
    # (team_index, closed), donde team_index es el índice (1-indexado) del equipo asignado
    # en ese movimiento y closed es un booleano que indica si con esa asignación se cierra el grupo.
    
    dp = [ {} for _ in range(n + 1) ]
    init_state = (0, 0, 0, 0, 0, 0, 0)
    dp[0][init_state] = (0, None)  # Estado inicial con costo 0 y sin predecesor.
    
    # Iteramos en orden creciente según la cantidad de equipos asignados.
    for total in range(n):
        # Recorremos una copia de los estados para evitar modificar el diccionario mientras se itera.
        for state, (cost, parent) in list(dp[total].items()):
            # Extraemos la información del estado.
            counts = state[0:5]  # (c1, c2, c3, c4, c5)
            j = state[5]         # cantidad de equipos en el grupo actual
            s = state[6]         # suma de los valores en el grupo actual
# Probamos asignar un equipo de cada valor v en {1,2,3,4,5} si hay disponibles.
            for v in range(1, 6):
                if counts[v-1] < f[v-1]:
                    # Obtenemos el índice del siguiente equipo disponible de valor v.
                    # Como counts[v-1] indica cuántos equipos de ese valor se han usado,
                    # el siguiente disponible es el que está en la posición counts[v-1] de teams_by_value[v-1].
                    team_index = teams_by_value[v-1][counts[v-1]]
                    
                    # Actualizamos los contadores para el valor v.
                    new_counts = list(counts)
                    new_counts[v-1] += 1
                    new_counts = tuple(new_counts)
                    
                    # Caso 1: El grupo actual no se completa.
                    if j + 1 < k:
                        new_state = new_counts + (j + 1, s + v)
                        new_cost = cost  # No se agrega costo extra.
                        decision = (team_index + 1, False)  # Guardamos el índice 1-indexado.
                    # Caso 2: Se completa el grupo actual.
                    else:
                        new_state = new_counts + (0, 0)  # Reiniciamos el grupo.
                        local_cost = abs((s + v) * m - T)
                        new_cost = cost + local_cost
                        decision = (team_index + 1, True)
                    
                    # Actualizamos dp para total+1 equipos asignados.
                    if new_state not in dp[total + 1] or new_cost < dp[total + 1][new_state][0]:
                        dp[total + 1][new_state] = (new_cost, (state, decision))
    
    # El estado final es cuando se han asignado todos los equipos y no hay grupo incompleto.
    final_state = (f[0], f[1], f[2], f[3], f[4], 0, 0)
    if final_state not in dp[n]:
        return None, math.inf  # No se encontró una asignación válida.
    
    best_cost = dp[n][final_state][0]
    
    # Reconstrucción de la solución:
    # Recuperamos la secuencia de decisiones (movimientos) desde el estado final hacia el inicial.
    moves = []  # Cada elemento es (team_index, closed)
    current_state = final_state
    current_total = n
    while current_total > 0:
        parent_info = dp[current_total][current_state][1]  # (prev_state, decision)
        prev_state, decision = parent_info
        moves.append(decision)
        prev_total = sum(prev_state[0:5])
        current_state = prev_state
        current_total = prev_total
    moves.reverse()  # Orden correcto de asignación.
    
    # Reconstrucción de los grupos:
    groups = []
    current_group = []
    for (team_index, closed) in moves:
        current_group.append(team_index)  # team_index ya está en formato 1-indexado.
        if closed:
            groups.append(current_group)
            current_group = []
    # Por seguridad, si hubiera un grupo incompleto (no debería ocurrir), se agrega.
    if current_group:
        groups.append(current_group)
    
    return groups, best_cost

# Ejemplo de uso:
def main():
    team_values = [3 ,4, 3, 5, 2, 3, 4, 5, # 0-7
                    2, 2, 3, 2, 2, 4, 5, 4, #8-15
                      5, 2, 3, 4, 5, 4, 4, 3, # 16-23
                        2, 3 ,4, 5, 4, 2, 3, 3] # 24- 31
    m = 8
    k = 4

    groups, cost = solve(team_values, m, k)
    if groups is None:
        print("No se encontró una asignación válida.")
    else:
        print("La asignación de equipos a grupos es:")
        for i, group in enumerate(groups, 1):
            print(f"  Grupo {i}: {group}")
        print("El costo total (suma de desbalances) es:", cost/m)


main()