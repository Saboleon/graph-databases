from data_structures import Graph
import heapq
import math

def dijkstra(graph: Graph, start_node: str):
  distances = dict()
  min_heap = []
  previous = dict()

  all_nodes = graph.get_all_nodes()
  for node in all_nodes:
    distances[node] = math.inf
  if start_node not in distances: raise ValueError(f"Node {start_node} is not in graph")
  distances[start_node] = 0

  heapq.heappush(min_heap, (0, start_node))

  while min_heap:
    current_distance, node = heapq.heappop(min_heap)
    if current_distance > distances[node]: continue
    neighbors = graph.get_neighbors(node)
    for neighbor, dist in neighbors:
      new_dist = current_distance + dist
      if new_dist < distances[neighbor]:
        distances[neighbor] = new_dist
        previous[neighbor] = node
        heapq.heappush(min_heap, (new_dist, neighbor))
  
  return distances, previous

graph = Graph(is_directed=True)

graph.add_edge("A", "B", 7)
graph.add_edge("A", "C", 12)
graph.add_edge("B", "C", 2)
graph.add_edge("B", "D", 9)
graph.add_edge("C", "E", 10)
graph.add_edge("D", "F", 1)
graph.add_edge("E", "D", 4)
graph.add_edge("E", "F", 5)

distances, path = dijkstra(graph, "A")
print(distances)
print(path)