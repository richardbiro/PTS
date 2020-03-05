from pyrsistent import s

class Relation:
    def __init__(self,M,rel = s()):
        self.M = M 
        self.rel = rel
        
    def contains(self,a,b):
        return (a,b) in self.rel

    def add(self,a,b):
        if a in self.M and b in self.M:
            return Relation(self.M,self.rel.add((a,b)))
        return self

    def remove(self,a,b):
        if self.contains(a,b):
            return Relation(self.M,self.rel.remove((a,b)))
        return self

def get_relation_class(M):
    return Relation(M)
