def process_island(m, i, j):
  if i >= len(m) or j >= len(m[i]) or i < 0 or j < 0: return
  if m[i][j] == 0: return
  m[i][j] = 0
  process_island(m, i-1, j)
  process_island(m, i+1, j)
  process_island(m, i, j-1)
  process_island(m, i, j+1)
  

def count_islands(m):
  if len(m) == 0: return 0
  rows = len(m)
  cols = len(m[0]) 
  m_copy = [row[:] for row in m]
  ans = 0
  for i in range(rows):
    for j in range(cols):
      if m_copy[i][j] == 1: 
        process_island(m_copy, i, j)
        ans += 1
  
  return ans

mat = [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1]]
print(count_islands(mat))