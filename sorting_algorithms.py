from data_structures import Graph
from collections import defaultdict

def topological_sort_bfs(graph: Graph) -> list[str]:
  """
  Topologically sort the nodes of a directed acyclic graph. Return a list of sorted nodes.
  """
  if graph.is_directed is False: raise ValueError("Graph must be directed")
  # get indegrees for each node
  # record ones with 0 indegree
  # remove nodes with 0 indegree one by one and add them to the sorted list
  # also reduce the indegree for nodes they are connected to
  # add new nodes with 0 indegree, until all nodes are processed
  # if nodes with indegree > 0 are left, there is a cycle
  in_degrees = defaultdict(int) 
  edges = graph.get_edge_list() 
  for _, _, n2 in edges: in_degrees[n2] += 1
  all_nodes = graph.get_all_nodes()

  parentless_node_list = []
  for node in all_nodes:
    if in_degrees[node] == 0: parentless_node_list.append(node)

  sorted_list = []
  while parentless_node_list:
    node = parentless_node_list.pop()
    sorted_list.append(node)
    neighbors = graph.get_neighbors(node)
    for n, _ in neighbors:
      in_degrees[n] -= 1
      if in_degrees[n] == 0: parentless_node_list.append(n)
  
  if len(sorted_list) != len(all_nodes): raise ValueError("Graph must be acyclic")

  return sorted_list

def _explore_path(graph: Graph, node: str, nodes_status, stack: list[str]) -> bool:
  # must both explore paths and flag cycles
  # return true if there's a cycle, otherwise false
  if nodes_status[node] == 1: return True
  if nodes_status[node] == 2: return False
  nodes_status[node] = 1
  neighbors = graph.get_neighbors(node)
  for n, _ in neighbors:
    if _explore_path(graph, n, nodes_status, stack): return True
  nodes_status[node] = 2
  stack.append(node)
  return False

def topological_sort_dfs(graph: Graph) -> list[str]:
  """
  Topologically sort the nodes of a directed acyclic graph. Return a list of sorted nodes.
  """
  if graph.is_directed is False: raise ValueError("Graph must be directed")
  nodes_status = defaultdict(int) # 0 for unvisited, 1 for visiting, 2 for visited
  stack = []
  all_nodes = graph.get_all_nodes()
  for node in all_nodes:
    if nodes_status[node] == 2: continue
    if _explore_path(graph, node, nodes_status, stack): 
      raise ValueError("Graph must be acyclic")
  
  stack.reverse()
  return stack

graph = Graph(is_directed=True)

graph.add_edge("A", "B", 1)
graph.add_edge("B", "C", 1)
graph.add_edge("C", "D", 1)
graph.add_edge("D", "E", 1)
graph.add_edge("D", "F", 1)
graph.add_edge("A", "F", 1)

print(topological_sort_bfs(graph))
print(topological_sort_dfs(graph))