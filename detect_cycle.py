from data_structures import Graph
from collections import defaultdict

def _explore_path_directed(graph: Graph, node: str, nodes_status: dict) -> bool:
  # return True if cycle is detected, otherwise return False
  if nodes_status[node] == 1: return True
  if nodes_status[node] == 2: return False
  nodes_status[node] = 1
  neighbors = graph.get_neighbors(node)
  for n, _ in neighbors:
    if _explore_path_directed(graph, n, nodes_status): return True
  nodes_status[node] = 2
  return False

def _has_cycle_directed(graph: Graph) -> bool:
  """
  Detects whether a directed graph has a cycle or not. Returns True if it has a cycle, otherwise it returns False.
  """
  nodes_status = defaultdict(int) # dict[str, int] 0 for unvisited, 1 for visiting, 2 for safe
  all_nodes = graph.get_all_nodes()
  for node in all_nodes:
    if nodes_status[node] == 2: continue
    if _explore_path_directed(graph, node, nodes_status): return True
  return False

def _has_cycle_undirected(graph: Graph) -> bool:
  nodes = graph.get_all_nodes()
  roots = dict()
  for node in nodes: roots[node] = node

  def find(node):
    if roots[node] != node: roots[node] = find(roots[node])
    return roots[node]
  
  edges = graph.get_edge_list()
  for _, n1, n2 in edges:
    root1 = find(n1)
    root2 = find(n2)
    if root1 == root2: return True
    roots[root2] = root1

  return False

def has_cycle(graph: Graph) -> bool:
  """
  Detects whether a graph has a cycle or not. Returns True if it has a cycle, otherwise it returns False.
  """
  if graph.is_directed: return _has_cycle_directed(graph)
  return _has_cycle_undirected(graph)
