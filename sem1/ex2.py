def count_components(edges: list[tuple[str, str]]) -> int:
  parent = {}
  
  def find(node):
    if parent[node] == node:
      return node
    parent[node] = find(parent[node]) 
    return parent[node]
      
  def union(n1, n2):
    root1 = find(n1)
    root2 = find(n2)
    if root1 != root2:
      parent[root1] = root2

  for u, v in edges:
    parent[u] = u
    parent[v] = v
      
  for u, v in edges:
    union(u, v)
      
  unique_components = set(find(node) for node in parent)
  return len(unique_components)

edges = [("1", "2"), ("2", "3"), ("5", "1"), ("4", "5"), ("6", "7"), ("7", "2"), ("8", "7")] 
print(count_components(edges))