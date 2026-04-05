import unittest
from data_structures import Graph
from .longest_path_dag import longest_path_dag


def build_graph(edges):
    """Helper: builds a directed graph from a list of (src, dst, weight) tuples."""
    g = Graph(True)
    nodes = set()
    for src, dst, w in edges:
        nodes.add(src)
        nodes.add(dst)
    for node in nodes:
        g.add_node(node)
    for src, dst, w in edges:
        g.add_edge(src, dst, w)
    return g


def reconstruct_path(previous, target):
    """Helper: reconstructs the path from source to target using the previous dict."""
    if target not in previous:
        return None
    path = [target]
    while previous[path[-1]] != path[-1]:
        path.append(previous[path[-1]])
    path.reverse()
    return path


class TestBasicCases(unittest.TestCase):

    def test_simple_linear_chain(self):
        """A -> B -> C, should find the only path."""
        g = build_graph([("A", "B", 5), ("B", "C", 3)])
        dist, prev = longest_path_dag(g, "A")
        self.assertEqual(dist["A"], 0)
        self.assertEqual(dist["B"], 5)
        self.assertEqual(dist["C"], 8)
        self.assertEqual(reconstruct_path(prev, "C"), ["A", "B", "C"])

    def test_multiple_paths_picks_longest(self):
        """Two paths from A to C: A->C (weight 2) and A->B->C (weight 3+4=7)."""
        g = build_graph([("A", "B", 3), ("B", "C", 4), ("A", "C", 2)])
        dist, prev = longest_path_dag(g, "A")
        self.assertEqual(dist["C"], 7)
        self.assertEqual(reconstruct_path(prev, "C"), ["A", "B", "C"])

    def test_negative_edge_weights(self):
        """Negative weights: A->B (10), B->C (-3), A->C (6). Longest to C is max(10-3, 6) = 7."""
        g = build_graph([("A", "B", 10), ("B", "C", -3), ("A", "C", 6)])
        dist, prev = longest_path_dag(g, "A")
        self.assertEqual(dist["B"], 10)
        self.assertEqual(dist["C"], 7)
        self.assertEqual(reconstruct_path(prev, "C"), ["A", "B", "C"])

    def test_all_negative_weights(self):
        """All edges negative: A->B (-2), B->C (-5). Longest path is still through them."""
        g = build_graph([("A", "B", -2), ("B", "C", -5)])
        dist, prev = longest_path_dag(g, "A")
        self.assertEqual(dist["B"], -2)
        self.assertEqual(dist["C"], -7)
        self.assertEqual(reconstruct_path(prev, "C"), ["A", "B", "C"])


class TestEdgeCases(unittest.TestCase):

    def test_single_node(self):
        """Graph with only the source node."""
        g = Graph(True)
        g.add_node("A")
        dist, prev = longest_path_dag(g, "A")
        self.assertEqual(dist["A"], 0)
        self.assertEqual(prev["A"], "A")

    def test_unreachable_node(self):
        """D is not reachable from A."""
        g = build_graph([("A", "B", 1), ("B", "C", 2)])
        g.add_node("D")
        dist, prev = longest_path_dag(g, "A")
        self.assertEqual(dist["D"], -float("inf"))
        self.assertNotIn("D", prev)

    def test_invalid_source_raises(self):
        """Source not in graph should raise ValueError."""
        g = build_graph([("A", "B", 1)])
        with self.assertRaises(ValueError):
            longest_path_dag(g, "Z")


class TestComplexDAGs(unittest.TestCase):

    def test_diamond_dag(self):
        """
        Diamond shape:
            A
           / \
          B   C
           \ /
            D
        A->B (1), A->C (2), B->D (4), C->D (3)
        Longest to D: max(1+4, 2+3) = 5 via both.
        """
        g = build_graph([("A", "B", 1), ("A", "C", 2), ("B", "D", 4), ("C", "D", 3)])
        dist, prev = longest_path_dag(g, "A")
        self.assertEqual(dist["A"], 0)
        self.assertEqual(dist["B"], 1)
        self.assertEqual(dist["C"], 2)
        self.assertEqual(dist["D"], 5)

    def test_longer_dag_with_multiple_paths(self):
        """
        A -> B (3), A -> C (2)
        B -> D (1), C -> D (4)
        D -> E (2), C -> E (10)
        Longest to E: A->C->E = 2+10 = 12
        """
        g = build_graph([
            ("A", "B", 3), ("A", "C", 2),
            ("B", "D", 1), ("C", "D", 4),
            ("D", "E", 2), ("C", "E", 10),
        ])
        dist, prev = longest_path_dag(g, "A")
        self.assertEqual(dist["E"], 12)
        self.assertEqual(reconstruct_path(prev, "E"), ["A", "C", "E"])

    def test_source_in_middle_of_dag(self):
        """
        A -> B -> C -> D. Source is B.
        A should remain -inf, C and D reachable.
        """
        g = build_graph([("A", "B", 5), ("B", "C", 3), ("C", "D", 7)])
        dist, prev = longest_path_dag(g, "B")
        self.assertEqual(dist["A"], -float("inf"))
        self.assertEqual(dist["B"], 0)
        self.assertEqual(dist["C"], 3)
        self.assertEqual(dist["D"], 10)
        self.assertNotIn("A", prev)

    def test_path_reconstruction_stops_at_source(self):
        """Verify that path reconstruction terminates at the source node."""
        g = build_graph([("S", "A", 1), ("A", "B", 2), ("B", "C", 3)])
        dist, prev = longest_path_dag(g, "S")
        path = reconstruct_path(prev, "C")
        self.assertEqual(path[0], "S")
        self.assertEqual(path, ["S", "A", "B", "C"])


if __name__ == "__main__":
    unittest.main()