class Graph:
  @staticmethod
  def build_graph_from_edges(is_directed: bool, edge_list: list[tuple[float | int, str, str]]):
    graph = Graph(is_directed)
    for weight, node1, node2 in edge_list:
      graph.add_edge(node1, node2, weight)
    return graph
  
  def __init__(self, is_directed: bool):
    # TODO: add multi edge functionality
    self.is_directed: bool = is_directed
    self.graph: dict[str, list[tuple[str, float]]] = dict()
  
  def add_node(self, node_name: str):
    self.graph[node_name] = []

  def add_edge(self, node1: str, node2: str, edge_weight: float | int):
    if node1 in self.graph:
      self.graph[node1].append((node2, float(edge_weight)))
    else:
      self.graph[node1] = [(node2, float(edge_weight))]

    if node2 not in self.graph:
      self.add_node(node2)
    
    if self.is_directed is False:
      self.graph[node2].append((node1, float(edge_weight)))
    
  def get_neighbors(self, node: str): 
    if node in self.graph: return self.graph[node]
    else: return []
  
  def get_all_nodes(self):
    return list(self.graph.keys())

  def get_edge_list(self):
    res = []
    for node1 in self.graph:
      for node2, weight in self.graph[node1]:
        if self.is_directed or node1 < node2: res.append((weight,node1,node2))
    return res

  def __str__(self):
    graph_type = "Directed" if self.is_directed else "Undirected"
    print_str = f"{graph_type} Graph"
    for node1 in self.graph: 
      print_str += f"\n {node1}"
      for node2, weight in self.graph[node1]:
        print_str += f"\n   -> {node2} ({weight})"
    return print_str

  # add vertex
  # add edge
  # remove vertex
  # remove edge
  # change edge weight
  # get edge weight
  