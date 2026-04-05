from data_structures import Graph
from sorting_algorithms import topological_sort_dfs

def longest_path_dag(graph: Graph, source: str):
  distances = dict()
  previous = dict()
  all_nodes = graph.get_all_nodes()
  contains_source = False
  for node in all_nodes:
    if node == source: contains_source = True
    distances[node] = -float("inf")
  if not contains_source: raise ValueError("Invalid source node")
  distances[source] = 0
  previous[source] = source
  sorted_nodes = topological_sort_dfs(graph)
  for node in sorted_nodes:
    neighbors = graph.get_neighbors(node)
    for n, w in neighbors:
      new_dist = distances[node] + w
      if new_dist > distances[n]: 
        distances[n] = new_dist
        previous[n] = node
        
  return distances, previous 
    