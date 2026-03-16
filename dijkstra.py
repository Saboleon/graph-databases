from data_structures import Graph
import heapq
import math

def dijkstra(graph: Graph, start_node: str):
  """
  Run the Dijkstra's algorithm on a graph with no negative edge weights to get the minimum distances from a node to all other nodes.
  Returns distances as well as shortest paths.
  """
  distances = dict()
  min_heap = []
  previous = dict()

  all_nodes = graph.get_all_nodes()
  for node in all_nodes:
    distances[node] = math.inf
  if start_node not in distances: raise ValueError(f"Node {start_node} is not in graph")
  distances[start_node] = 0

  # Standard BFS approach with a min-heap
  heapq.heappush(min_heap, (0, start_node))

  while min_heap:
    current_distance, node = heapq.heappop(min_heap)
    # since we cannot modify elements in heap, there will be some old values remaining
    # we just skip these
    if current_distance > distances[node]: continue 
    neighbors = graph.get_neighbors(node)
    for neighbor, dist in neighbors:
      new_dist = current_distance + dist
      if new_dist < distances[neighbor]:
        distances[neighbor] = new_dist
        previous[neighbor] = node
        heapq.heappush(min_heap, (new_dist, neighbor))
  
  return distances, previous
