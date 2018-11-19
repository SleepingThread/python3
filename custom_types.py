

class mdict(dict):
    def __add__(self,other):
        res = mdict({})
        if isinstance(other,mdict) or isinstance(other,dict):
            for key in self:
                if key in other:
                    res[key] = self[key]+other[key]
        else:
            for key in self:
                res[key] = self[key]+other
            
        return res
    
    def __sub__(self,other):
        res = mdict({})
        if isinstance(other,mdict) or isinstance(other,dict):
            for key in self:
                if key in other:
                    res[key] = self[key]-other[key]
        else:
            for key in self:
                res[key] = self[key]-other
            
        return res
    
    def __mul__(self,other):
        res = mdict({})
        if isinstance(other,mdict) or isinstance(other,dict):
            for key in self:
                if key in other:
                    res[key] = self[key]*other[key]
        else:
            for key in self:
                res[key] = self[key]*other
            
        return res
    
    def __truediv__(self,other):
        res = mdict({})
        if isinstance(other,mdict) or isinstance(other,dict):
            for key in self:
                if key in other:
                    res[key] = self[key]/other[key]
        else:
            for key in self:
                res[key] = self[key]/other
            
        return res
    
    def __floordiv__(self,other):
        res = mdict({})
        if isinstance(other,mdict) or isinstance(other,dict):
            for key in self:
                if key in other:
                    res[key] = self[key]//other[key]
        else:
            for key in self:
                res[key] = self[key]//other
            
        return res
