import unittest
from data_structures import Graph
from check_isomoprhism import are_isomorphic

class TestAreIsomorphic(unittest.TestCase):

    # --- Trivial / base cases ---

    def test_both_empty(self):
        g1, g2 = Graph(False), Graph(False)
        self.assertTrue(are_isomorphic(g1, g2))

    def test_single_node_each(self):
        g1, g2 = Graph(False), Graph(False)
        g1.add_node("a")
        g2.add_node("x")
        self.assertTrue(are_isomorphic(g1, g2))

    def test_different_node_counts(self):
        g1, g2 = Graph(False), Graph(False)
        g1.add_node("a")
        g1.add_node("b")
        g2.add_node("x")
        self.assertFalse(are_isomorphic(g1, g2))

    def test_different_edge_counts(self):
        g1 = Graph.build_graph_from_edges(False, [(1, "a", "b")])
        g2 = Graph.build_graph_from_edges(False, [(1, "x", "y"), (1, "y", "z")])
        self.assertFalse(are_isomorphic(g1, g2))

    # --- Undirected graphs ---

    def test_simple_path_isomorphic(self):
        # a-b-c  vs  x-y-z
        g1 = Graph.build_graph_from_edges(False, [(1, "a", "b"), (1, "b", "c")])
        g2 = Graph.build_graph_from_edges(False, [(1, "x", "y"), (1, "y", "z")])
        self.assertTrue(are_isomorphic(g1, g2))

    def test_triangle_isomorphic(self):
        g1 = Graph.build_graph_from_edges(False, [(1, "a", "b"), (1, "b", "c"), (1, "c", "a")])
        g2 = Graph.build_graph_from_edges(False, [(1, "1", "2"), (1, "2", "3"), (1, "3", "1")])
        self.assertTrue(are_isomorphic(g1, g2))

    def test_triangle_vs_path_not_isomorphic(self):
        g1 = Graph.build_graph_from_edges(False, [(1, "a", "b"), (1, "b", "c"), (1, "c", "a")])
        g2 = Graph.build_graph_from_edges(False, [(1, "x", "y"), (1, "y", "z")])
        self.assertFalse(are_isomorphic(g1, g2))

    def test_same_degree_sequence_not_isomorphic(self):
        # Two graphs with degree sequence [2,2,2,2,2,2] but different structure
        # C6 (6-cycle) vs two triangles (K3 + K3)
        g1 = Graph.build_graph_from_edges(False, [
            (1, "a", "b"), (1, "b", "c"), (1, "c", "d"),
            (1, "d", "e"), (1, "e", "f"), (1, "f", "a"),
        ])
        g2 = Graph.build_graph_from_edges(False, [
            (1, "1", "2"), (1, "2", "3"), (1, "3", "1"),
            (1, "4", "5"), (1, "5", "6"), (1, "6", "4"),
        ])
        self.assertFalse(are_isomorphic(g1, g2))

    def test_k4_isomorphic_relabeled(self):
        g1 = Graph.build_graph_from_edges(False, [
            (1, "a", "b"), (1, "a", "c"), (1, "a", "d"),
            (1, "b", "c"), (1, "b", "d"), (1, "c", "d"),
        ])
        g2 = Graph.build_graph_from_edges(False, [
            (1, "w", "x"), (1, "w", "y"), (1, "w", "z"),
            (1, "x", "y"), (1, "x", "z"), (1, "y", "z"),
        ])
        self.assertTrue(are_isomorphic(g1, g2))

    def test_petersen_like_non_isomorphic(self):
        # Star K1,4 vs cycle C5 — same node count (5), different edge count
        g1 = Graph.build_graph_from_edges(False, [
            (1, "a", "b"), (1, "a", "c"), (1, "a", "d"), (1, "a", "e"),
        ])
        g2 = Graph.build_graph_from_edges(False, [
            (1, "1", "2"), (1, "2", "3"), (1, "3", "4"),
            (1, "4", "5"), (1, "5", "1"),
        ])
        self.assertFalse(are_isomorphic(g1, g2))

    # --- Weighted edges ---

    def test_same_structure_different_weights(self):
        g1 = Graph.build_graph_from_edges(False, [(1, "a", "b"), (2, "b", "c")])
        g2 = Graph.build_graph_from_edges(False, [(2, "x", "y"), (2, "y", "z")])
        self.assertFalse(are_isomorphic(g1, g2))

    def test_same_structure_same_weights_permuted(self):
        g1 = Graph.build_graph_from_edges(False, [(3, "a", "b"), (5, "b", "c")])
        g2 = Graph.build_graph_from_edges(False, [(5, "x", "y"), (3, "y", "z")])
        self.assertTrue(are_isomorphic(g1, g2))

    # --- Directed graphs ---

    def test_directed_isomorphic(self):
        g1 = Graph.build_graph_from_edges(True, [(1, "a", "b"), (1, "b", "c")])
        g2 = Graph.build_graph_from_edges(True, [(1, "x", "y"), (1, "y", "z")])
        self.assertTrue(are_isomorphic(g1, g2))

    def test_directed_reversed_not_isomorphic(self):
        # a->b->c  vs  x->y, z->y  (different in/out degree sequences)
        g1 = Graph.build_graph_from_edges(True, [(1, "a", "b"), (1, "b", "c")])
        g2 = Graph.build_graph_from_edges(True, [(1, "x", "y"), (1, "z", "y")])
        self.assertFalse(are_isomorphic(g1, g2))

    def test_directed_cycle_isomorphic(self):
        g1 = Graph.build_graph_from_edges(True, [(1, "a", "b"), (1, "b", "c"), (1, "c", "a")])
        g2 = Graph.build_graph_from_edges(True, [(1, "1", "2"), (1, "2", "3"), (1, "3", "1")])
        self.assertTrue(are_isomorphic(g1, g2))

    def test_directed_vs_undirected_mismatch(self):
        g1 = Graph.build_graph_from_edges(True, [(1, "a", "b")])
        g2 = Graph.build_graph_from_edges(False, [(1, "x", "y")])
        self.assertFalse(are_isomorphic(g1, g2))

    # --- Disconnected graphs ---

    def test_disconnected_isomorphic(self):
        g1 = Graph(False)
        g1.add_node("a"); g1.add_node("b"); g1.add_edge("c", "d")
        g2 = Graph(False)
        g2.add_node("w"); g2.add_node("x"); g2.add_edge("y", "z")
        self.assertTrue(are_isomorphic(g1, g2))

    def test_isolated_nodes_count_matters(self):
        g1 = Graph(False)
        g1.add_node("a"); g1.add_node("b"); g1.add_node("c")
        g2 = Graph(False)
        g2.add_node("x"); g2.add_node("y")
        self.assertFalse(are_isomorphic(g1, g2))

    # --- Self-loops ---

    def test_self_loop(self):
        g1 = Graph.build_graph_from_edges(True, [(1, "a", "a")])
        g2 = Graph.build_graph_from_edges(True, [(1, "x", "x")])
        self.assertTrue(are_isomorphic(g1, g2))

    def test_self_loop_vs_no_self_loop(self):
        g1 = Graph.build_graph_from_edges(True, [(1, "a", "a"), (1, "a", "b")])
        g2 = Graph.build_graph_from_edges(True, [(1, "x", "y"), (1, "y", "x")])
        self.assertFalse(are_isomorphic(g1, g2))


if __name__ == "__main__":
    unittest.main()