import unittest
from kruskal import kruskal
from data_structures import Graph

class TestKruskal(unittest.TestCase):

  def test_kruskal_simple(self):
    # A simple triangle: A-B (1), B-C (2), A-C (3)
    # MST should exclude A-C (weight 3)
    edges = [(1, "A", "B"), (2, "B", "C"), (3, "A", "C")]
    graph = Graph.build_graph_from_edges(False, edges)
    
    mst = kruskal(graph)
    mst_edges = mst.get_edge_list()
    
    self.assertEqual(len(mst_edges), 2)
    total_weight = sum(e[0] for e in mst_edges)
    self.assertEqual(total_weight, 3) # 1 + 2

  def test_kruskal_disconnected(self):
    # Two separate components
    edges = [(1, "A", "B"), (5, "C", "D")]
    graph = Graph.build_graph_from_edges(False, edges)
    
    mst = kruskal(graph)
    self.assertEqual(len(mst.get_edge_list()), 2)

  def test_kruskal_directed_error(self):
    g = Graph(is_directed=True)
    with self.assertRaises(ValueError):
      kruskal(g)

  def test_kruskal_complex(self):
    # Graph with 4 nodes forming a square
    # A-B (1), B-C (5), C-D (1), D-A (5)
    # MST should be A-B, B-C, C-D (total 7) OR A-B, D-A, C-D (total 7)
    edges = [(1, "A", "B"), (5, "B", "C"), (1, "C", "D"), (5, "D", "A")]
    graph = Graph.build_graph_from_edges(False, edges)
    
    mst = kruskal(graph)
    mst_edges = mst.get_edge_list()
    
    self.assertEqual(len(mst_edges), 3)
    total_weight = sum(e[0] for e in mst_edges)
    self.assertEqual(total_weight, 7)

  def test_kruskal_single_node(self):
    g = Graph(is_directed=False)
    g.add_node("A")
    mst = kruskal(g)
    self.assertEqual(len(mst.get_edge_list()), 0)

if __name__ == '__main__':
    unittest.main()