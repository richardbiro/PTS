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

    def union(self,R):
        return Relation(self.M,self.rel.union(R.rel))

    def intersect(self,R):
        return Relation(self.M,self.rel.intersection(R.rel))

    def subtract(self,R):
        return Relation(self.M,self.rel.difference(R.rel))

    def reflexive(self):
        return all(self.contains(a,a) for a in self.M)

    def symmetric(self):
        return all(self.contains(b,a) for (a,b) in self.rel)

    def transitive(self):
        return all(self.contains(a,c) or b1 != b2
                   for (a,b1) in self.rel for (b2,c) in self.rel)

def get_relation_class(M):
    return Relation(M)
