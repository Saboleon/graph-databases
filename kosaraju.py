from data_structures import Graph
from collections import defaultdict

def _construct_stack(graph: Graph, node: str, stack: list[str], visited: set[str]):
  visited.add(node)
  neighbors = graph.get_neighbors(node)
  for n, _ in neighbors:
    if n not in visited:
      _construct_stack(graph, n, stack, visited)
  
  stack.append(node)

def _find_scc(edges: defaultdict[str, list], node: str, scc: list[str], visited: set[str]):
  visited.add(node)
  neighbors = edges[node]
  for n in neighbors:
    if n not in visited:
      _find_scc(edges, n, scc, visited)
  scc.append(node)

def kosaraju(graph: Graph):
  if not graph.is_directed: raise ValueError("Graph must be directed")
  visited = set()
  stack = []
  all_nodes = graph.get_all_nodes()

  for node in all_nodes:
    if node not in visited:
      _construct_stack(graph, node, stack, visited)
  
  reverse_edges = defaultdict(list)
  edges = graph.get_edge_list()
  for _, n1, n2 in edges: reverse_edges[n2].append(n1)

  visited.clear()
  res = []
  while stack:
    node = stack.pop()
    if node not in visited:
      scc = []
      _find_scc(reverse_edges, node, scc, visited)
      res.append(scc)
  
  return res
