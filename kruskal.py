from data_structures import Graph

def kruskal(graph: Graph):
  if graph.is_directed: raise ValueError("Kruskal does not work on directed graphs")

  edge_list = sorted(graph.get_edge_list())
  parents = dict()
  ranks = dict()

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
    if union(node1, node2): new_edge_list.append((weight, node1, node2))
    i += 1
  
  return Graph.build_graph_from_edges(is_directed=False, edge_list=new_edge_list)
  

graph = Graph(is_directed=False)
for i in range(9):
  graph.add_node(str(i))

graph.add_edge("0", "1", 4)
graph.add_edge("0", "7", 8)
graph.add_edge("1", "2", 8)
graph.add_edge("1", "7", 11)
graph.add_edge("2", "3", 7)
graph.add_edge("2", "5", 4)
graph.add_edge("2", "8", 2)
graph.add_edge("3", "4", 9)
graph.add_edge("3", "5", 14)
graph.add_edge("4", "5", 10)
graph.add_edge("5", "6", 2)
graph.add_edge("6", "7", 1)
graph.add_edge("6", "8", 6)
graph.add_edge("7", "8", 7)

mst = kruskal(graph)
print(mst)