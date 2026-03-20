from data_structures import Graph
from kosaraju import kosaraju
import unittest

def sccs_as_frozen_sets(result):
    """Normalise a list-of-lists into a frozenset of frozensets for order-free comparison."""
    return frozenset(frozenset(scc) for scc in result)
 
 
def make_directed(*edges):
    """Convenience: build a directed Graph from (node1, node2) pairs (weight=1)."""
    g = Graph(is_directed=True)
    for n1, n2 in edges:
        g.add_edge(n1, n2)
    return g
 
 
# ── Tests ─────────────────────────────────────────────────────────────────────
 
 
class TestKosarajuInputValidation(unittest.TestCase):
    def test_raises_on_undirected_graph(self):
        g = Graph(is_directed=False)
        g.add_edge("A", "B")
        with self.assertRaises(ValueError):
            kosaraju(g)
 
    def test_empty_graph_returns_empty(self):
        g = Graph(is_directed=True)
        self.assertEqual(kosaraju(g), [])
 
    def test_single_isolated_node(self):
        g = Graph(is_directed=True)
        g.add_node("A")
        result = sccs_as_frozen_sets(kosaraju(g))
        self.assertEqual(result, frozenset([frozenset(["A"])]))
 
 
class TestKosarajuStructure(unittest.TestCase):
    def setUp(self):
        # Classic 3-SCC graph: {A,B,C}, {D}, {E,F}
        self.g = make_directed(
            ("A", "B"), ("B", "C"), ("C", "A"),   # cycle → one SCC
            ("C", "D"),                             # bridge to singleton
            ("D", "E"), ("E", "F"), ("F", "E"),    # E↔F cycle
        )
 
    def test_scc_count_matches_expected(self):
        self.assertEqual(len(kosaraju(self.g)), 3)
 
    def test_every_node_appears_exactly_once(self):
        all_nodes_in_result = [n for scc in kosaraju(self.g) for n in scc]
        self.assertEqual(sorted(all_nodes_in_result), sorted(self.g.get_all_nodes()))
 
    def test_scc_sizes_are_correct(self):
        sizes = sorted(len(scc) for scc in kosaraju(self.g))
        self.assertEqual(sizes, [1, 2, 3])
 
 
class TestKosarajuCorrectness(unittest.TestCase):
    def test_simple_cycle_is_single_scc(self):
        g = make_directed(("A", "B"), ("B", "C"), ("C", "A"))
        result = sccs_as_frozen_sets(kosaraju(g))
        self.assertEqual(result, frozenset([frozenset(["A", "B", "C"])]))
 
    def test_linear_chain_all_singletons(self):
        # A→B→C→D: no back-edges, so every node is its own SCC
        g = make_directed(("A", "B"), ("B", "C"), ("C", "D"))
        result = sccs_as_frozen_sets(kosaraju(g))
        expected = frozenset([
            frozenset(["A"]),
            frozenset(["B"]),
            frozenset(["C"]),
            frozenset(["D"]),
        ])
        self.assertEqual(result, expected)
 
    def test_two_separate_cycles(self):
        g = make_directed(
            ("A", "B"), ("B", "A"),
            ("C", "D"), ("D", "C"),
        )
        result = sccs_as_frozen_sets(kosaraju(g))
        self.assertEqual(result, frozenset([frozenset(["A", "B"]), frozenset(["C", "D"])]))
 
    def test_fully_connected_graph_is_one_scc(self):
        nodes = ["A", "B", "C", "D"]
        g = Graph(is_directed=True)
        for n1 in nodes:
            for n2 in nodes:
                if n1 != n2:
                    g.add_edge(n1, n2)
        result = sccs_as_frozen_sets(kosaraju(g))
        self.assertEqual(result, frozenset([frozenset(nodes)]))
 
    def test_classic_three_scc_graph(self):
        g = make_directed(
            ("A", "B"), ("B", "C"), ("C", "A"),
            ("C", "D"),
            ("D", "E"), ("E", "F"), ("F", "E"),
        )
        result = sccs_as_frozen_sets(kosaraju(g))
        expected = frozenset([
            frozenset(["A", "B", "C"]),
            frozenset(["D"]),
            frozenset(["E", "F"]),
        ])
        self.assertEqual(result, expected)
 
    def test_self_loop_is_its_own_scc(self):
        g = Graph(is_directed=True)
        g.add_edge("A", "A")
        g.add_edge("A", "B")
        result = sccs_as_frozen_sets(kosaraju(g))
        self.assertIn(frozenset(["A"]), result)
        self.assertIn(frozenset(["B"]), result)
 
    def test_node_with_no_outgoing_edges(self):
        g = Graph(is_directed=True)
        g.add_edge("A", "B")
        g.add_node("C")          # isolated node added explicitly
        result = sccs_as_frozen_sets(kosaraju(g))
        self.assertIn(frozenset(["C"]), result)
 
    def test_build_graph_from_edges_helper(self):
        edge_list = [
            (1, "X", "Y"), (1, "Y", "Z"), (1, "Z", "X"),
            (1, "Z", "W"),
        ]
        g = Graph.build_graph_from_edges(is_directed=True, edge_list=edge_list)
        result = sccs_as_frozen_sets(kosaraju(g))
        self.assertIn(frozenset(["X", "Y", "Z"]), result)
        self.assertIn(frozenset(["W"]), result)
 
    def test_weighted_edges_do_not_affect_scc_membership(self):
        g = Graph(is_directed=True)
        g.add_edge("A", "B", 5.0)
        g.add_edge("B", "A", 99.0)
        result = sccs_as_frozen_sets(kosaraju(g))
        self.assertEqual(result, frozenset([frozenset(["A", "B"])]))
 
    def test_large_single_cycle(self):
        nodes = [str(i) for i in range(20)]
        g = Graph(is_directed=True)
        for i in range(len(nodes)):
            g.add_edge(nodes[i], nodes[(i + 1) % len(nodes)])
        result = sccs_as_frozen_sets(kosaraju(g))
        self.assertEqual(result, frozenset([frozenset(nodes)]))
 
 
if __name__ == "__main__":
    unittest.main()