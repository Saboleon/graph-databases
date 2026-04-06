from data_structures import Graph
from collections import defaultdict

def _build_degree_map(edges: list[tuple[float, str, str]]):
  degree_map = defaultdict(list)
  for w, n1, n2 in edges:
    degree_map[n1].append(w)
    degree_map[n2].append(w)
  
  for key in degree_map:
    degree_map[key].sort()
  
  return degree_map

def _is_consistent(mapping, graph1, graph2, node1, node2):
  for neighbor, weight in graph1.get_neighbors(node1):
    if neighbor in mapping:
      mapped_neighbor = mapping[neighbor]
      for n2_neighbor, n2_weight in graph2.get_neighbors(node2):
        if n2_neighbor == mapped_neighbor and n2_weight == weight:
          break
      else: return False

  if graph1.is_directed:
    edge_list1 = graph1.get_edge_list()
    edge_list2 = graph2.get_edge_list()
    for w1, n1, n2 in edge_list1:
      if n2 == node1 and n1 in mapping:
        mapped_neighbor = mapping[n1]
        for w2, n11, n22 in edge_list2:
          if n11 == mapped_neighbor and n22 == node2 and w1 == w2:
            break
        else: 
          return False

  return True
  
def _backtrack(nodes1, index, mapping, used, graph1, graph2, candidates):
  if index == len(nodes1): return True

  cur_node = nodes1[index]
  for node2 in candidates[cur_node]:
    if node2 in used: continue
    if _is_consistent(mapping, graph1, graph2, cur_node, node2):
      mapping[cur_node] = node2
      used.add(node2)
      if _backtrack(nodes1, index + 1, mapping, used, graph1, graph2, candidates):
        return True
      del mapping[cur_node]
      used.remove(node2)
  
  return False

def are_isomorphic(graph1: Graph, graph2: Graph):
  if graph1.is_directed != graph2.is_directed:
    return False

  if graph1 == graph2: return True

  nodes1 = graph1.get_all_nodes()
  nodes2 = graph2.get_all_nodes()
  if len(nodes1) != len(nodes2): return False

  edges1 = graph1.get_edge_list()
  edges2 = graph2.get_edge_list()
  if len(edges1) != len(edges2): return False

  if sorted(w for w, _, _ in edges1) != sorted(w for w, _, _ in edges2): return False
  
  degree_map1 = _build_degree_map(edges1)
  degree_map2 = _build_degree_map(edges2)

  if sorted(degree_map1.values()) != sorted(degree_map2.values()): return False
  
  candidates = dict()
  for n1 in nodes1:
    candidates[n1] = [n2 for n2 in nodes2 if degree_map1[n1] == degree_map2[n2]]
    if not candidates[n1]: return False
  
  sorted_nodes1 = sorted(nodes1, key= lambda n: len(candidates[n]))

  mapping = dict()
  used = set()
  return _backtrack(sorted_nodes1, 0, mapping, used, graph1, graph2, candidates)