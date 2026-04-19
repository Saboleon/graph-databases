"""
Unit tests for `shortest_paths` (directed-graph, string-named-city version).

Adjust the import below to match your module.

Spec these tests encode:
  * `cities` is a list of string names.
  * Edges are DIRECTED — (n1, n2, d, t) means travel from n1 to n2.
  * Edge cost is:  cost = distance + alpha * toll
  * `total_cost` is the sum of those edge costs along the chosen path.
  * start == dest returns ([start], 0) (after validating membership).
  * Unreachable dest returns ([], math.inf).
  * Unknown start / dest / edge endpoint raises ValueError.
"""

import math
import unittest

from hw1 import shortest_paths  # <-- adjust to your module


class TestShortestPaths(unittest.TestCase):

    # ---------- helpers ----------

    def assert_valid_directed_path(self, path, edges, start, dest):
        """Sanity-check that `path` is a real directed walk from start to dest."""
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], dest)
        directed = {(u, v) for u, v, _, _ in edges}
        for u, v in zip(path, path[1:]):
            self.assertIn((u, v), directed, f"No directed edge {u} -> {v}")

    # ---------- trivial / boundary ----------

    def test_start_equals_dest(self):
        edges = [("A", "B", 5.0, 1.0), ("B", "C", 3.0, 0.5)]
        path, cost = shortest_paths(["A", "B", "C"], edges, "B", "B")
        self.assertEqual(path, ["B"])
        self.assertAlmostEqual(cost, 0.0)

    def test_single_city_self_query(self):
        path, cost = shortest_paths(["A"], [], "A", "A")
        self.assertEqual(path, ["A"])
        self.assertAlmostEqual(cost, 0.0)

    def test_single_direct_edge(self):
        # cost = 5.0 + 0.5 * 1.0 = 5.5
        edges = [("A", "B", 5.0, 1.0)]
        path, cost = shortest_paths(["A", "B"], edges, "A", "B")
        self.assertEqual(path, ["A", "B"])
        self.assertAlmostEqual(cost, 5.5)

    # ---------- directed-graph semantics ----------

    def test_edge_is_traversable_in_declared_direction(self):
        # Edge A -> B must be usable going from A to B.
        edges = [("A", "B", 5.0, 0.0)]
        path, cost = shortest_paths(["A", "B"], edges, "A", "B")
        self.assertEqual(path, ["A", "B"])
        self.assertAlmostEqual(cost, 5.0)

    def test_reverse_direction_is_unreachable(self):
        # Edge A -> B must NOT enable travel from B to A.
        edges = [("A", "B", 5.0, 0.0)]
        path, cost = shortest_paths(["A", "B"], edges, "B", "A")
        self.assertEqual(path, [])
        self.assertEqual(cost, math.inf)

    def test_both_directions_require_two_edges(self):
        edges = [("A", "B", 5.0, 0.0), ("B", "A", 7.0, 0.0)]
        path_fwd, cost_fwd = shortest_paths(["A", "B"], edges, "A", "B")
        path_bwd, cost_bwd = shortest_paths(["A", "B"], edges, "B", "A")
        self.assertEqual(path_fwd, ["A", "B"])
        self.assertAlmostEqual(cost_fwd, 5.0)
        self.assertEqual(path_bwd, ["B", "A"])
        self.assertAlmostEqual(cost_bwd, 7.0)

    # ---------- path-finding correctness ----------

    def test_picks_shorter_of_two_routes(self):
        # A->B->C totals 2; direct A->C is 20.
        edges = [
            ("A", "B", 1.0, 0.0),
            ("B", "C", 1.0, 0.0),
            ("A", "C", 20.0, 0.0),
        ]
        path, cost = shortest_paths(["A", "B", "C"], edges, "A", "C")
        self.assertEqual(path, ["A", "B", "C"])
        self.assertAlmostEqual(cost, 2.0)

    def test_larger_graph(self):
        # Best A->E: A->B->D->E = 1 + 2 + 1 = 4
        # Alternate: A->C->E   = 3 + 3     = 6
        edges = [
            ("A", "B", 1.0, 0.0),
            ("A", "C", 3.0, 0.0),
            ("B", "D", 2.0, 0.0),
            ("D", "E", 1.0, 0.0),
            ("C", "E", 3.0, 0.0),
        ]
        cities = ["A", "B", "C", "D", "E"]
        path, cost = shortest_paths(cities, edges, "A", "E")
        self.assert_valid_directed_path(path, edges, "A", "E")
        self.assertEqual(path, ["A", "B", "D", "E"])
        self.assertAlmostEqual(cost, 4.0)

    def test_parallel_edges_uses_cheapest(self):
        edges = [
            ("A", "B", 10.0, 0.0),
            ("A", "B", 3.0, 0.0),
        ]
        path, cost = shortest_paths(["A", "B"], edges, "A", "B")
        self.assertEqual(path, ["A", "B"])
        self.assertAlmostEqual(cost, 3.0)

    # ---------- alpha / toll semantics ----------

    def test_alpha_zero_ignores_toll(self):
        # A->B->C: distance 2, huge tolls.
        # A->C:    distance 5, zero toll.
        # alpha=0 → detour wins.
        edges = [
            ("A", "B", 1.0, 1000.0),
            ("B", "C", 1.0, 1000.0),
            ("A", "C", 5.0, 0.0),
        ]
        path, cost = shortest_paths(["A", "B", "C"], edges, "A", "C", alpha=0.0)
        self.assertEqual(path, ["A", "B", "C"])
        self.assertAlmostEqual(cost, 2.0)

    def test_alpha_one_prefers_low_toll_route(self):
        # Same graph; alpha=1 makes tolls dominate, so the zero-toll direct
        # edge wins.
        edges = [
            ("A", "B", 1.0, 1000.0),
            ("B", "C", 1.0, 1000.0),
            ("A", "C", 5.0, 0.0),
        ]
        path, cost = shortest_paths(["A", "B", "C"], edges, "A", "C", alpha=1.0)
        self.assertEqual(path, ["A", "C"])
        self.assertAlmostEqual(cost, 5.0)

    def test_default_alpha_balances_distance_and_toll(self):
        # Direct A->C: cost = 10
        # A->B->C:     cost = (3 + 0.5) + (3 + 0.5) = 7
        edges = [
            ("A", "C", 10.0, 0.0),
            ("A", "B", 3.0, 1.0),
            ("B", "C", 3.0, 1.0),
        ]
        path, cost = shortest_paths(["A", "B", "C"], edges, "A", "C")
        self.assertEqual(path, ["A", "B", "C"])
        self.assertAlmostEqual(cost, 7.0)

    def test_cost_is_distance_plus_alpha_times_toll(self):
        # Regression test distinguishing `d + alpha*t` from `(1-alpha)*d + alpha*t`:
        #
        # Under d + alpha*t,   alpha=0.3:  direct=10, detour=(3+1.5)*2=9    → detour wins
        # Under (1-a)d + a*t,  alpha=0.3:  direct=7,  detour=(2.1+1.5)*2=7.2 → direct wins
        edges = [
            ("A", "C", 10.0, 0.0),
            ("A", "B", 3.0, 5.0),
            ("B", "C", 3.0, 5.0),
        ]
        path, cost = shortest_paths(["A", "B", "C"], edges, "A", "C", alpha=0.3)
        self.assertEqual(path, ["A", "B", "C"])
        self.assertAlmostEqual(cost, 9.0)

    def test_alpha_above_one_amplifies_toll(self):
        # alpha=2:
        #   direct A->C:     cost = 5 + 2*1 = 7
        #   detour A->B->C:  cost = 3 + 3   = 6
        edges = [
            ("A", "C", 5.0, 1.0),
            ("A", "B", 3.0, 0.0),
            ("B", "C", 3.0, 0.0),
        ]
        path, cost = shortest_paths(["A", "B", "C"], edges, "A", "C", alpha=2.0)
        self.assertEqual(path, ["A", "B", "C"])
        self.assertAlmostEqual(cost, 6.0)

    # ---------- unreachable ----------

    def test_unreachable_dest_returns_empty_path_and_inf_cost(self):
        # A -> B exists; C is isolated.
        edges = [("A", "B", 1.0, 0.0)]
        path, cost = shortest_paths(["A", "B", "C"], edges, "A", "C")
        self.assertEqual(path, [])
        self.assertEqual(cost, math.inf)

    def test_unreachable_with_empty_edge_list(self):
        path, cost = shortest_paths(["A", "B"], [], "A", "B")
        self.assertEqual(path, [])
        self.assertEqual(cost, math.inf)

    # ---------- invalid input ----------

    def test_start_not_in_cities_raises(self):
        with self.assertRaises(ValueError):
            shortest_paths(["A", "B"], [("A", "B", 1.0, 0.0)], "Z", "B")

    def test_dest_not_in_cities_raises(self):
        with self.assertRaises(ValueError):
            shortest_paths(["A", "B"], [("A", "B", 1.0, 0.0)], "A", "Z")

    def test_edge_referencing_unknown_city_raises(self):
        with self.assertRaises(ValueError):
            shortest_paths(["A", "B"], [("A", "Z", 1.0, 0.0)], "A", "B")


if __name__ == "__main__":
    unittest.main()