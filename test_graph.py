import unittest
from data_structures import Graph


class TestGraph(unittest.TestCase):
  def test_add_node(self):
    g = Graph(is_directed=True)
    g.add_node("A")
    self.assertIn("A", g.get_all_nodes())
    self.assertEqual(g.get_neighbors("A"), [])

  def test_directed_graph(self):
    g = Graph(is_directed=True)
    g.add_edge("A", "B", 5.0)
    
    self.assertEqual(g.get_neighbors("A"), [("B", 5.0)])
    self.assertEqual(g.get_neighbors("B"), [])
    self.assertEqual(len(g.get_edge_list()), 1)

  def test_undirected_graph(self):
    g = Graph(is_directed=False)
    g.add_edge("A", "B", 5.0)
    
    # In undirected, A -> B and B -> A exist
    self.assertIn(("B", 5.0), g.get_neighbors("A"))
    self.assertIn(("A", 5.0), g.get_neighbors("B"))
    # get_edge_list should only show 1 entry for undirected
    self.assertEqual(len(g.get_edge_list()), 1)

  def test_build_from_edges(self):
    edges = [(1.5, "A", "B"), (2.0, "B", "C")]
    g = Graph.build_graph_from_edges(True, edges)
    
    nodes = g.get_all_nodes()
    self.assertCountEqual(nodes, ["A", "B", "C"])
    self.assertEqual(len(g.get_edge_list()), 2)

  def test_get_edge_list_order(self):
    # Verify that node1 < node2 logic works for undirected edge listing
    g = Graph(is_directed=False)
    g.add_edge("B", "A", 1.0)
    edges = g.get_edge_list()
    # Should return (1.0, 'A', 'B') because 'A' < 'B'
    self.assertEqual(edges[0][1], 'A')
    self.assertEqual(edges[0][2], 'B')

  def test_nonexistent_node(self):
    g = Graph(is_directed=True)
    self.assertEqual(g.get_neighbors("Z"), [])

if __name__ == '__main__':
    unittest.main()