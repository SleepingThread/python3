import numpy as np
import networkx as nx
import copy
import keras.backend as K

from st_global import isinstance_fromlist,timer_decorator, set_path
from st_graph import add_depth
from st_graphics import bar_fromarray
from st_global import iterate,exist_path,apply_operation

def _iterateKerasLayer(layer,types=[],names=[],path=[]):
    for el in layer.__dict__:
        newpath = list(path)
        newpath.append(el)
        if el in ["layer","cell"]:
            for el2 in _iterateKerasLayer(layer.__dict__[el],types=types,names=names,path=newpath):
                yield el2
        elif isinstance_fromlist(layer.__dict__[el],types):
            yield (newpath,layer.__dict__[el])
        elif el in names:
            yield (newpath,layer.__dict__[el])
            
    return

def iterateKerasLayers(model,types=[],names=[],path=[]):
    layers = model.layers
    for ind,layer in enumerate(layers):
        for el in _iterateKerasLayer(layer,types=types,names=names,path=[ind]):
            yield el
            
    return

class NNModel(object):
    """
    Todo:
        __add__
        __sub__
        toKeras
        setKeras (with batch mode)
        blocks
        get input/output for block
    """
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.storage = {}
        return

    def __getitem__(self,name):
        """
        For generic types (why generic?) - like dict,list
        """
        return self.graph.node[name]

    #def __setitem__(self,name,value):
    #    self.graph.node[name] = value
    #    return

    @timer_decorator
    def fromKeras(self, keras_model,verbose=1):
        graph = nx.DiGraph()
        
        config = keras_model.get_config()
        
        for key in config:
            if key!="layers":
                graph.graph[key] = copy.deepcopy(config[key])
        
        # add nodes
        for lr in config["layers"]:
            graph.add_node(lr["name"])
            # add layer config to node
            graph.nodes[lr["name"]]["config"] = copy.deepcopy(lr)
            # initialize dict for weights
            graph.nodes[lr["name"]]["weights"] = {}
            
            
        # add edges
        for lr in config["layers"]:
            if len(lr["inbound_nodes"])==0:
                continue
            for inb_node in lr["inbound_nodes"][0]:
                inb_layer = inb_node[0]
                graph.add_edge(inb_layer,lr["name"])
        
        # batch weights unload
        w_dict = {}

        paths = []
        keras_variables = []
        for el in iterateKerasLayers(keras_model,types=[K.variable([0]).__class__]):
            _path = [keras_model.layers[el[0][0]].name]
            _path.extend(el[0][1:])
            paths.append(_path)
            keras_variables.append(el[1])

        # we can replace batch_get_value with cycle with K.eval
        keras_values = K.batch_get_value(keras_variables)
    
        for path,val in zip(paths,keras_values):
            set_path(w_dict,path,val)        

        for _node in w_dict:
            graph.nodes[_node]["weights"] = w_dict[_node]
        
        self.graph = graph
        
        """        
        self.storage = {}
        for layer in keras_model.layers:
            self.storage[layer.name] = {}
            fill_storage(self.storage[layer.name],layer,
                         [K.variable([0]).__class__,K.constant([0]).__class__],verbose=verbose)
        """
            
        return self
    
    @timer_decorator
    def setKeras(self,keras_model):

        path_list = []
        var_list = []
        for el in iterateKerasLayers(keras_model,types=[K.variable([0]).__class__]):
            _path = list(el[0])
            _path[0] = keras_model.layers[_path[0]].name
            _path.insert(1,"weights")
            
            path_list.append(_path)
            var_list.append(el[1])
            
        var_value_list = []
        for _path,_var in zip(path_list,var_list):
            if exist_path(self.graph.nodes[_path[0]],_path[1:]):
                var_value_list.append((_var,self(_path)))
            
        K.batch_set_value(var_value_list)
    
        return
    
    def toKeras(self,keras_model,verbose=1):
        # build topology 
        
        # initialize weights
        
        
        for layer in keras_model.layers:
            if layer.name in self.storage:
                set_keras_layer(self.storage[layer.name],layer,
                                [K.variable([0]).__class__,K.constant([0]).__class__],verbose=verbose)
            else:
                if verbose>0:
                    print "-",layer.name," not exists in storage"
        return self
    
    def __call__(self,path):
        path_root = self.graph.nodes
        for el in path:
            path_root = path_root[el]
            
        return path_root
    
    def sub(self,nn_model,strict=False):
        """
        """
        new_nn_model = copy.deepcopy(self)
        
        new_nodes = new_nn_model.graph.nodes
        nodes = self.graph.nodes
        nodes2 = nn_model.graph.nodes
        for _node in nodes:
            if _node not in nodes2:
                if strict:
                    raise Exception("Models are not equal")
                else:
                    continue
            new_nodes[_node]["weights"] = \
                apply_operation(lambda _path,_a,_b: _a-_b, [nodes[_node]["weights"],nodes2[_node]["weights"]])
        return new_nn_model
    
    def add(self,nn_model,strict=False):
        """
        """
        new_nn_model = copy.deepcopy(self)
        
        new_nodes = new_nn_model.graph.nodes
        nodes = self.graph.nodes
        nodes2 = nn_model.graph.nodes
        for _node in nodes:
            if _node not in nodes2:
                if strict:
                    raise Exception("Models are not equal")
                else:
                    continue
            new_nodes[_node]["weights"] = \
                apply_operation(lambda _path,_a,_b: _a+_b, [nodes[_node]["weights"],nodes2[_node]["weights"]])
        return new_nn_model
    
    def __sub__(self,nn_model):
        return self.sub(nn_model,strict=True)
    
    def __add__(self,nn_model):
        return self.add(nn_model,strict=True)
    
    def apply_operation(self,op,verbose=2):
        result = {}
        nodes = self.graph.nodes
        for _node in nodes:
            result[_node] = apply_operation(op,[nodes[_node]["weights"]],verbose=verbose)
        return result
        
    def getSVG(self):
        graph = nx.drawing.nx_pydot.to_pydot(self.graph)
        
        for _node in graph.get_nodes():
            _name = _node.get_name().strip('"')

            _config = self.graph.nodes[_name]["config"]["config"]
            _label1 = _name+" : "+self.graph.nodes[_name]["config"]["class_name"]
            
            if "layer" in _config:
                _layer = _config["layer"]
                _node.set_label(_label1+"\nlayer: "+_layer["config"]["name"]+" : "+_layer["class_name"])
                
            elif "cell" in _config:
                _cell = _config["cell"]
                _node.set_label(_label1+"\ncell: "+_cell["config"]["name"]+" : "+_cell["class_name"])
                
            else:
                _node.set_label(_label1)
        
        svg_pic = graph.create_svg()
        # pg.get_nodes()[0].set_label("10\nLabel for node 0")
        return svg_pic
    
    def drawGraph(self):
        SVG = None
        try:
            from IPython.display import SVG
        except:
            print "Cannot load SVG from IPython.display"
            
        if SVG is not None:
            return SVG(self.getSVG())
        
        return None
        
    """
    def __getattr__(self,name):
        print "Call for ",name
        return

    def __setattr__(self,name,value):
        print "Setting ",name," with ",value
        return

    def __delattr__(self,name):
        print "Delete ",name
        return
        
    @staticmethod
    def _keras_layer(storage,layer):
        
        return
    """

def minmaxWindow(array,w_size):
    if w_size<0:
        raise Exception("Window must be >= 0")

    new_array = []
    array = array.reshape((-1,))
    for ind in range(0,array.shape[0],w_size):
        _window = array[ind*w_size:(ind+1)*w_size]
        new_array.extend([np.min(_window),np.max(_window)])

    return np.array(new_array)

def draw_weights(nn_model,layers=None,names=None,color_list=None,w_size=100):
    """
    :param layers: List of layer names for drawing
    :param names: List of weight names
    """
    
    add_depth(nn_model.graph)
    
    if layers is None:
        layers = [_node for _node in nn_model.graph.nodes]
        
    array_list = []
    labels_list = []
    # array depth - depth of correspondent layer
    array_depth = []
        
    for _node in nn_model.graph.nodes:
        if _node not in layers:
            continue
        for _path,_weight in iterate(nn_model.graph.nodes[_node]["weights"]):
            _depth = nn_model.graph.nodes[_node]["depth"]
            if names is None:
                array_list.append(minmaxWindow(_weight,w_size))
                labels_list.append(_node+" : "+str(_depth)+"\n"+_path[-1])
                array_depth.append(nn_model.graph.nodes[_node]["depth"])
            elif _path[-1] in names:
                array_list.append(minmaxWindow(_weight,w_size))
                labels_list.append(_node+" : "+str(_depth)+"\n"+_path[-1])
                array_depth.append(nn_model.graph.nodes[_node]["depth"])
                
    # sort array_list and labels list with respect to array_depth
    sort_trans = np.argsort(array_depth)
    array_list = np.asarray(array_list)[sort_trans]
    labels_list = np.asarray(labels_list)[sort_trans]
    
    return bar_fromarray(array_list,labels_list,color_list=color_list)
