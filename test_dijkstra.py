import unittest
import math
import heapq

from dijkstra import dijkstra
from data_structures import Graph

# Assuming your class and function are in the same scope or imported
class TestDijkstra(unittest.TestCase):

  def test_dijkstra_basic(self):
    # A - (1) -> B - (2) -> C
    # A - (4) -> C
    edges = [(1, "A", "B"), (2, "B", "C"), (4, "A", "C")]
    graph = Graph.build_graph_from_edges(is_directed=True, edge_list=edges)
    
    distances, previous = dijkstra(graph, "A")
    
    self.assertEqual(distances["C"], 3) # A->B->C is 3, which is < 4
    self.assertEqual(previous["C"], "B")

  def test_dijkstra_disconnected(self):
    # A -> B, C (C is isolated)
    edges = [(1, "A", "B")]
    graph = Graph.build_graph_from_edges(is_directed=True, edge_list=edges)
    graph.add_node("C")
    
    distances, previous = dijkstra(graph, "A")
    
    self.assertEqual(distances["B"], 1)
    self.assertEqual(distances["C"], math.inf)
    self.assertNotIn("C", previous)

  def test_dijkstra_invalid_start_node(self):
    graph = Graph(is_directed=True)
    graph.add_node("A")
    with self.assertRaises(ValueError):
      dijkstra(graph, "Z")

  def test_dijkstra_undirected(self):
    # A - (1) - B - (1) - C
    edges = [(1, "A", "B"), (1, "B", "C")]
    graph = Graph.build_graph_from_edges(is_directed=False, edge_list=edges)
    
    distances, _ = dijkstra(graph, "A")
    
    self.assertEqual(distances["C"], 2)

  def test_dijkstra_cycle(self):
    # Graph with a cycle and a shortcut
    # A -> B (1), B -> C (1), C -> D (1), A -> C (1)
    # Shortest path to D should be A -> C -> D (weight 2)
    edges = [(1, "A", "B"), (1, "B", "C"), (1, "C", "D"), (1, "A", "C")]
    graph = Graph.build_graph_from_edges(is_directed=True, edge_list=edges)
    
    distances, _ = dijkstra(graph, "A")
    
    self.assertEqual(distances["D"], 2)

if __name__ == '__main__':
  unittest.main()