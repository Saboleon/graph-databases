from collections import defaultdict
import heapq
import math

def shortest_paths(cities: list[str], edges: list[tuple[str, str, float, float]], start: str, dest: str, alpha=0.5) -> tuple[list[str], float]:
  """
  ## Input: 
    `cities`: A list of city names
    `edges`: A list of (city1, city2, distance, toll).
    `start`: Start city
    `dest`: Destination city
    `alpha`: weight for the toll in edge cost calculation: cost = Distance + alpha * Toll
  
  ## Output:
    `shortest_path`: A list of nodes representing the shortest path from `start` to `dest`
    `total_cost`: The total cost of the shortest path from `start` to `dest`
  """
  # check the validity of the inputs
  if start not in cities:
    raise ValueError(f"Start city '{start}' is not in the cities list.")
  if dest not in cities:
    raise ValueError(f"Destination city '{dest}' is not in the cities list.")

  if start == dest: return [start], 0
  
  # ASSUMPTION1: The graph is directed
  # ASSUMPTION2: Distance and toll cannot be negative
  
  # build the edge mapping
  mapping = defaultdict(list)
  for idx, (n1, n2, dist, toll) in enumerate(edges):
    if n1 not in cities or n2 not in cities or dist < 0 or toll < 0:
      raise ValueError(f"Invalid input in edges at index {idx}: {n1, n2, dist, toll}")
    cost = dist + alpha * toll
    mapping[n1].append((n2, cost))
  
  distances = { city: math.inf for city in cities }
  distances[start] = 0
  previous = { city: city for city in cities }
  # Standard Dijkstra with min heap
  min_heap = [(0, start)]

  while min_heap:
    cur_distance, node = heapq.heappop(min_heap)
    # in python, it's impossible to modify values in the heap
    # so there will be some leftover values that we need to skip
    if cur_distance > distances[node]: continue
    edges_from_node = mapping[node]
    for neighbor, cost in edges_from_node:
      new_distance = cur_distance + cost
      if new_distance < distances[neighbor]:
        distances[neighbor] = new_distance
        previous[neighbor] = node
        heapq.heappush(min_heap, (new_distance, neighbor))
    
  # Check if destination is unreachable from start
  if distances[dest] == math.inf:
    return [], math.inf

  # build a list of nodes that give the shortest path
  shortest_path = [dest]
  cur = dest
  while cur != start:
    shortest_path.append(previous[cur])
    cur = previous[cur]
  
  return list(reversed(shortest_path)), distances[dest]