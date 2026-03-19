def max_area_of_island(grid):
  rows, cols = len(grid), len(grid[0])

  def dfs(r, c):
    if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == 0: return 0
    
    grid[r][c] = 0
    return 1 + dfs(r-1, c) + dfs(r+1, c) + dfs(r, c-1) + dfs(r, c+1)
  
  max_area = 0
  for i in range(rows):
    for j in range(cols):
      if grid[i][j] == 1:
        max_area = max(max_area, dfs(i, j))
  
  return max_area
