class Simple(object):
    def __init__(self):
        self.a = None
        self.b = 12
        return

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

def fill_storage(storage,layer,types_to_copy,verbose=1):
    for attr in layer.__dict__:
        if isinstance_fromlist(layer.__dict__[attr],types_to_copy):
            if verbose>0:
                print "copy ",attr," from ",layer
            storage[attr] = K.eval(layer.__dict__[attr])
    
    if hasattr(layer,"layer"):
        storage["layer"] = {}
        fill_storage(storage["layer"],layer.layer,types_to_copy)
    if hasattr(layer,"cell"):
        storage["cell"] = {}
        fill_storage(storage["cell"],layer.cell,types_to_copy)

    return

def set_keras_layer(storage,layer,types_to_copy,verbose=1):
    for key in storage:
        if not hasattr(layer,key):
            if verbose>0:
                print "-",key," not exists in ",layer
            continue
            
        if key!="layer" and key!="cell":
            if isinstance_fromlist(layer.__dict__[key],types_to_copy):
                K.set_value(layer.__dict__[key],storage[key])
            else:
                if verbose>0:
                    print "-",key," in ",layer," (not in types_to_copy) "        
        else:
            set_keras_layer(storage[key],layer.__dict__[key],types_to_copy)
        
    return

class NNModel(object):
    """
    Usage:
        n_model = NNModel().fromKeras(model)
        nn_model.toKeras(model)
    """
    def __init__(self):
        self.storage = {}
        return

    def __getitem__(self,name):
        """
        For generic types (why generic?) - like dict,list
        """
        return self.storage[name]

    def __setitem__(self,name,value):
        self.storage[name] = value
        return

    def fromKeras(self, keras_model,verbose=1):
        self.storage = {}
        for layer in keras_model.layers:
            self.storage[layer.name] = {}
            fill_storage(self.storage[layer.name],layer,
                         [K.variable([0]).__class__,K.constant([0]).__class__],verbose=verbose)
            
        return self

    def toKeras(self,keras_model,verbose=1):
        for layer in keras_model.layers:
            if layer.name in self.storage:
                set_keras_layer(self.storage[layer.name],layer,
                                [K.variable([0]).__class__,K.constant([0]).__class__],verbose=verbose)
            else:
                if verbose>0:
                    print "-",layer.name," not exists in storage"
        return self

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
"""
class Model(object):
    def __init__(self):
        return

    def __getattr__(self,name):
        print "Call for ",name
        return

    def __setattr__(self,name,value):
        print "Setting ",name," with ",value
        return

    def __delattr__(self,name):
        print "Delete ",name
        return

    def __getitem__(self,name):
        """
        For generic types (why generic?) - like dict,list
        """
        print "FIND ",name," FOR ME!"
        return

    def __setitem__(self,name,value):
        print "Set dict value ",name,"with ",value
        return

    @staticmethod
    def _keras_layer(storage,layer):
        
        return

    def fromKeras(self, model):
        storage = {}
        for lr in model.layers:
            
        return 

    def toKeras(self,keras_model):
        return

"""
