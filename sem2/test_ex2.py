import unittest
from ex2 import max_area_of_island

class TestIslandArea(unittest.TestCase):
  def test_example_case(self):
    grid = [
      [0,0,1,0,0],
      [1,1,1,0,0],
      [0,1,0,0,1],
      [0,0,0,1,1]
    ]
    self.assertEqual(max_area_of_island(grid), 5)

  def test_no_islands(self):
    grid = [[0, 0], [0, 0]]
    self.assertEqual(max_area_of_island(grid), 0)

  def test_single_island(self):
    grid = [[1, 1], [1, 1]]
    self.assertEqual(max_area_of_island(grid), 4)

  def test_multiple_islands(self):
    grid = [
      [1, 0],
      [0, 1]
    ]
    self.assertEqual(max_area_of_island(grid), 1)

if __name__ == '__main__':
  unittest.main()