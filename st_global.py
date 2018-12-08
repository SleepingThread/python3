import time
import math

def timer_decorator(func):
    def fun_decorator(*args,**kwargs):
        print "Start:",func.__name__
        start_time = time.time()
        _res = func(*args,**kwargs)
        print func.__name__+" : "+str(math.ceil(time.time()-start_time))+" sec"
        return _res
    
    return fun_decorator

def isinstance_fromlist(o,inst_list):
    for inst in inst_list:
        if isinstance(o,inst):
            return True
        
    return False

def hasattr_fromlist(o,attr_list):
    for attr in atrr_list:
        if hasattr(o,attr):
            return True
    return False

"""
iterate over dict-list storage
"""
def iterate(storage,path=[]):
    if isinstance(storage,dict):
        res = {}
        for key in storage:
            _new_path = list(path)
            _new_path.append(key)
            for _path,el2 in iterate(storage[key],path=_new_path):
                yield (_path,el2)
    elif isinstance(storage,list):
        for ind,el in enumerate(storage):
            _new_path = list(path)
            _new_path.append(ind)
            for _path,el2 in iterate(el,path=_new_path):
                yield (_path,el2)
    else:
        yield (path,storage)
    
    return

"""
    Warning: some operations require filter for applying, i.e.
        not all keys, not all types operation need to be applied
"""
def apply_operation(op,args,path=[],verbose=2):
    """
    Iteratively apply operation <op> to list of <args>
        Used for applying operations to lists and dicts
        
    Iterates over args[0]
    Stores result in res
    """
    arg0 = args[0]
    
    res = None
    
    if isinstance(arg0,dict):
        res = {}
        for key in arg0:
            _new_path = list(path)
            _new_path.append(key)
            if reduce(lambda _a,_v: _a and _v,[key in _arg for _arg in args],True):
                res[key] = apply_operation(op,[_arg[key] for _arg in args],path=_new_path)
            else:
                if verbose>1:
                    print "Skip ",key
    elif isinstance(arg0,list):
        res = []
        for ind,el in enumerate(zip(*args)):
            _new_path = list(path)
            _new_path.append(ind)
            res.append(apply_operation(op,el,path=_new_path))
    else:
        res = op(path,*args)
    
    return res

def set_path(o,path,value):
    _root = o
    
    if len(path)==0:
        raise Exception("Empty path")
    
    for el in path[:-1]:
        if el not in _root:
            _root[el] = {}
        _root = _root[el]
    
    _root[path[-1]] = value
            
    return o

def get_path(o,path):
    _root = o
    
    if len(path)==0:
        raise Exception("Empty path")
    
    for el in path:
        if isinstance(_root,list) and el<len(_root) or \
            isinstance(_root,dict) and el in _root:
            _root = _root[el]
        else:
            raise Exception("No such path")
            
    return _root

def exist_path(o,path):
    _root = o
    
    if len(path)==0:
        raise Exception("Empty path")
    
    for el in path:
        if isinstance(_root,list) and el<len(_root) or \
            isinstance(_root,dict) and el in _root:
            _root = _root[el]
        else:
            return False
            
    return True