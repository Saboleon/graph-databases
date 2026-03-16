import unittest
from collections import defaultdict

from data_structures import Graph
from sorting_algorithms import topological_sort_bfs, topological_sort_dfs

class TestTopologicalSort(unittest.TestCase):

  def setUp(self):
    # A simple DAG: A -> B -> C
    self.dag_edges = [(1, "A", "B"), (1, "B", "C")]
    self.dag = Graph.build_graph_from_edges(is_directed=True, edge_list=self.dag_edges)

  def _is_valid_topological_sort(self, graph, result):
    """Helper to verify if a list is a valid topological sort for the graph."""
    if len(result) != len(graph.get_all_nodes()):
      return False
    
    # Position index for each node
    pos = {node: i for i, node in enumerate(result)}
    for weight, u, v in graph.get_edge_list():
      if pos[u] > pos[v]:
        return False
    return True

  def test_bfs_sort(self):
    result = topological_sort_bfs(self.dag)
    self.assertTrue(self._is_valid_topological_sort(self.dag, result))

  def test_dfs_sort(self):
    result = topological_sort_dfs(self.dag)
    self.assertTrue(self._is_valid_topological_sort(self.dag, result))

  def test_cycle_detection(self):
    # A -> B -> A (Cycle)
    cycle_edges = [(1, "A", "B"), (1, "B", "A")]
    cycle_graph = Graph.build_graph_from_edges(is_directed=True, edge_list=cycle_edges)
    
    with self.assertRaises(ValueError):
      topological_sort_bfs(cycle_graph)
    with self.assertRaises(ValueError):
      topological_sort_dfs(cycle_graph)

  def test_undirected_error(self):
    undirected_graph = Graph(is_directed=False)
    undirected_graph.add_edge("A", "B")
    
    with self.assertRaises(ValueError):
      topological_sort_bfs(undirected_graph)
    with self.assertRaises(ValueError):
      topological_sort_dfs(undirected_graph)

  def test_disconnected_dag(self):
    # A -> B, C -> D
    edges = [(1, "A", "B"), (1, "C", "D")]
    graph = Graph.build_graph_from_edges(is_directed=True, edge_list=edges)
    
    self.assertTrue(self._is_valid_topological_sort(graph, topological_sort_bfs(graph)))
    self.assertTrue(self._is_valid_topological_sort(graph, topological_sort_dfs(graph)))

if __name__ == '__main__':
  unittest.main()