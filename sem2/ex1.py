def has_path_dfs(n, edges, start, end):
  if start < 0 or end < 0 or start >= n or end >= n: raise ValueError("invalid start or end node")
  
  adj = {i: [] for i in range(n)}
  for u, v in edges:
    if not (0 <= u < n and 0 <= v < n): raise ValueError("invalid edge")
    adj[u].append(v)
    adj[v].append(u)

  visited = set()
  def dfs(current):
    if current == end: return True
    visited.add(current)
    for n in adj[current]:
      if n not in visited and dfs(n): return True
    
    return False
  
  return dfs(start)
