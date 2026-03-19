from data_structures import Graph
from collections import defaultdict

def page_rank(graph: Graph, damping_factor=0.85, iterations=100):
  if graph.is_directed is False: raise ValueError("Graph must be directed")
  # set up initial scores and record end nodes (nodes with 0 outdegree)
  scores = dict()
  all_nodes = graph.get_all_nodes()
  n = len(all_nodes)
  if n == 0: return scores
  end_nodes = []
  for node in all_nodes: 
    scores[node] = 1 / n
    if len(graph.graph[node]) == 0: end_nodes.append(node)
  
  # record the parent nodes of every node in a dict
  all_edges = graph.get_edge_list()
  in_degrees = defaultdict(list)
  for _, n1, n2 in all_edges:
    in_degrees[n2].append(n1)
  
  # precalcualte base score as it does not change
  base_score = (1 - damping_factor) / n
  for _ in range(iterations):
    # calculate the dangling bonus
    dangling_bonus = sum([scores[node] for node in end_nodes]) * damping_factor / n

    new_scores = dict()
    for node in all_nodes:
      # for each node, calculate the number of incoming votes from parent nodes
      votes = 0
      for parent in in_degrees[node]: votes += scores[parent] / len(graph.graph[parent])
      new_scores[node] = base_score + dangling_bonus + votes * damping_factor
    scores = new_scores
  
  return scores 
