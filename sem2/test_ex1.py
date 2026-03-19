import unittest
from ex1 import has_path_dfs

class TestGraphDFS(unittest.TestCase):

  def test_example_case(self):
    self.assertFalse(has_path_dfs(6, [[0,1],[0,2],[3,5],[5,4],[4,3]], 0, 5))

  def test_simple_path(self):
    self.assertTrue(has_path_dfs(3, [[0,1], [1,2]], 0, 2))

  def test_no_path(self):
    self.assertFalse(has_path_dfs(4, [[0,1], [2,3]], 0, 3))

  def test_start_is_end(self):
    self.assertTrue(has_path_dfs(3, [[0,1]], 0, 0))

  def test_single_node_graph(self):
    self.assertTrue(has_path_dfs(1, [], 0, 0))

if __name__ == '__main__':
  unittest.main()