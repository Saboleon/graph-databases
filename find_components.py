from data_structures import Graph

def find_components(graph: Graph):
  if graph.is_directed: raise ValueError("Graph must be undirected")
  visited = set()
  components = []
  all_nodes = graph.get_all_nodes()
  if len(all_nodes) == 0: return []
  for node in all_nodes:
    if node in visited: continue
    stack = [node]
    visited.add(node)
    members = [node]
    while stack:
      n = stack.pop() 
      neighbors = graph.get_neighbors(n)
      for neighbor, _ in neighbors:
        if neighbor not in visited:
          visited.add(neighbor)
          members.append(neighbor)
          stack.append(neighbor)
    components.append(members)

  return components