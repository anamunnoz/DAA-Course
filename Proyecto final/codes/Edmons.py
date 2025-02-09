import networkx as nx

# Creamos un grafo no dirigido
G = nx.Graph()

# Agregamos nodos (opcional, ya que al agregar las aristas se crean automáticamente)
G.add_nodes_from(['A', 'B', 'C', 'D', 'E'])

# Agregamos aristas ponderadas (la clave 'weight' se utiliza para definir el peso de la arista)
G.add_edge('A', 'B', weight=1)
G.add_edge('A', 'C', weight=5)
G.add_edge('B', 'C', weight=8)
G.add_edge('B', 'D', weight=7)
G.add_edge('C', 'D', weight=6)
G.add_edge('C', 'E', weight=4)
G.add_edge('D', 'E', weight=3)

# Calculamos el emparejamiento máximo ponderado.
# El parámetro maxcardinality=True asegura que, entre emparejamientos de igual peso,
# se elija el de mayor cardinalidad.
matching = nx.algorithms.matching.max_weight_matching(G, maxcardinality=True, weight='weight')

print("Emparejamiento máximo ponderado:")
for edge in matching:
    # Cada arista se muestra como un conjunto inmutable (frozenset) de dos nodos
    print(edge)
