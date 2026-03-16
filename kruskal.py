from data_structures import Graph

def kruskal(graph: Graph):
  """
  Run a Kruskal's algorithm on an undirected graph to get the Minimum Spanning Tree.
  """
  if graph.is_directed: raise ValueError("Kruskal does not work on directed graphs")

  edge_list = sorted(graph.get_edge_list())
  parents = dict()
  ranks = dict()

  # set up initial lookup for unionfind
  all_nodes = graph.get_all_nodes()
  for node in all_nodes:
    parents[node] = node
    ranks[node] = 0
  
  def find(node):
    if parents[node] != node: 
      parents[node] = find(parents[node])
    return parents[node]

  def union(node1, node2):
    root1 = find(node1)
    root2 = find(node2)
    if root1 == root2: return False
    if ranks[root1] == ranks[root2]:
      parents[root2] = root1
      ranks[root1] += 1
    elif ranks[root1] > ranks[root2]: 
      parents[root2] = root1
    else: 
      parents[root1] = root2
    return True
  
  new_edge_list = []
  num_of_nodes = len(all_nodes)
  i = 0
  while len(new_edge_list) < num_of_nodes - 1 and i < len(edge_list):
    weight, node1, node2 = edge_list[i]
    # use union find to find cycle. If no cycle, add edge
    if union(node1, node2): new_edge_list.append((weight, node1, node2))
    i += 1
  
  return Graph.build_graph_from_edges(is_directed=False, edge_list=new_edge_list)
