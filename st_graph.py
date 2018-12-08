import copy
import warnings

def block(graph,inputs,outputs):
    block_nodes = []
    
    inputs = set(inputs)
    outputs = set(outputs)
    
    # exclude outputs nodes from inputs nodes
    inputs_only = inputs-outputs
    
    front = list(inputs_only)
    
    block_nodes.extend(inputs_only)
    block_nodes.extend(outputs)
    
    while len(front)>0:
        new_front = set()
        for el in front:
            neighbors = [_neigh for _neigh in graph[el]]
            if len(neighbors)==0:
                raise Exception("Could not create block")
            for _neigh in neighbors:
                if _neigh not in outputs:
                    new_front.add(_neigh)
            
        new_front = list(new_front)
        block_nodes.extend(new_front)
        front = new_front
        
    block_nodes_set = set(block_nodes)
    for b_node in block_nodes_set:
        if b_node not in inputs:
            for _pred in graph.predecessors(b_node):
                if _pred not in block_nodes_set:
                    warnings.warn("Cannot create block: not input node %s points inside block"%str(_pred))
        
    return {"inputs":copy.deepcopy(inputs),"outputs":copy.deepcopy(outputs),"nodes":block_nodes}

def roll_block(graph,blck,name):
    inputs = blck["inputs"]
    outputs = blck["outputs"]
    
    input_nodes = set()
    for inp in inputs:
        for el in graph.predecessors(inp):
            input_nodes.add(el)
        
    output_nodes = set()
    for out in outputs:
        for el in graph.neighbors(out):
            output_nodes.add(el)
    
    new_graph = graph.copy()
    new_graph.remove_nodes_from(blck["nodes"])
    
    new_graph.add_node(name)
    
    for edge in input_nodes:
        new_graph.add_edge(edge,name)
    for edge in output_nodes:
        new_graph.add_edge(name,edge)
    
    return new_graph

def get_neighbors(graph,node,depth=1):
    neighbors = []
    front = set([node])
    neighbors.extend(front)
    
    while depth>0:
        new_front = set()
        for el in front:
            for _pred in graph.predecessors(el):
                new_front.add(_pred)
                
            for _neigh in graph.neighbors(el):
                new_front.add(_neigh)
                
        neighbors.extend(new_front)
        front = new_front
        
        depth -= 1
        
    return neighbors

def get_roots(graph):
    graph_roots = []
    # find roots
    for _node in graph.nodes:
        if len([_el for _el in graph.predecessors(_node)])==0:
            graph_roots.append(_node)
    return graph_roots

def get_leaves(graph):
    graph_leaves = []
    # find leaves
    for _node in graph.nodes:
        if len([_el for _el in graph.neighbors(_node)])==0:
            graph_leaves.append(_node)
    return graph_leaves

def add_depth(graph):
    front = get_roots(graph)
    for _front_node in front:
        graph.nodes[_front_node]["depth"] = 0
    
    while len(front)>0:
        new_front = set()
        for _front_node in front:
            for _node in graph.neighbors(_front_node):
                if "depth" in graph.nodes[_node]:
                    _front_node_depth = graph.nodes[_front_node]["depth"]
                    _node_depth = graph.nodes[_node]["depth"]
                    _res_depth = max(_front_node_depth+1,_node_depth)
                    graph.nodes[_node]["depth"] = _res_depth
                                                              
                else:
                    graph.nodes[_node]["depth"] = \
                        graph.nodes[_front_node]["depth"] + 1
                
                new_front.add(_node)
                
        front = list(new_front)
        
    return graph

def draw_graph(graph):
    graph = nx.drawing.nx_pydot.to_pydot(graph)
    svg_pic = graph.create_svg()
    # pg.get_nodes()[0].set_label("10\nLabel for node 0")
    return SVG(svg_pic)