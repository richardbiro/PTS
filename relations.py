from pyrsistent import s, freeze
import warnings

def get_relation_class(M):
    class Relation:
        rset = M
        
        def __init__(self,rel = s()):
            self.rel = rel
            
        def contains(self,a,b):
            return (a,b) in self.rel

        def add(self,a,b):
            if a in self.rset and b in self.rset:
                return Relation(self.rel.add((a,b)))
            warnings.warn("Error: both a,b must be in the set of the relation!")
            return self

        def remove(self,a,b):
            if self.contains(a,b):
                return Relation(self.rel.remove((a,b)))
            warnings.warn("Error: (a,b) not found in relation!")
            return self

        def union(self,R):
            if R.rset.issubset(self.rset):
                return Relation(self.rel.union(R.rel))
            warnings.warn("Error: relations are not on the same set!")
            return self

        def intersect(self,R):
            return Relation(self.rel.intersection(R.rel))

        def subtract(self,R):
            return Relation(self.rel.difference(R.rel))

        def inverse(self):
            return Relation(set(x[::-1] for x in self.rel))

        def composition(self,R):
            if R.rset.issubset(self.rset):
                return Relation(set( (a,c) for (a,b1) in R.rel
                                 for (b2,c) in self.rel if b1 == b2))
            warnings.warn("Error: relations are not on the same set!")
            return self
            

        def reflexive(self):
            return all(self.contains(a,a) for a in self.rset)

        def symmetric(self):
            return all(self.contains(b,a) for (a,b) in self.rel)

        def transitive(self):
            return all(self.contains(a,c) or b1 != b2
                       for (a,b1) in self.rel for (b2,c) in self.rel)

        def closure(self):
            R = Relation(freeze(set((a,a) for a in self.rset)).union(self.rel))
            while not R.composition(self).rel.issubset(R.rel):
                R = R.union(R.composition(self))
            return R

        def printrel(self,text):
            print()
            print(text,"=",self.rel)
            print("reflexivna?",self.reflexive())
            print("symetricka?",self.symmetric())
            print("tranzitivna?",self.transitive())
            
    return Relation


P = get_relation_class({1,2,3,4})

a = P()
a = a.add(1,1)
a = a.add(1,3)
a = a.add(2,2)
a = a.add(2,3)
a = a.add(3,2)
a = a.add(4,1)
a.printrel("A")

a2 = a.inverse()
a2.printrel("A^(-1)")

a3 = a.closure()
a3.printrel("A*")


Q = get_relation_class({1,2,3})

b = Q()
b = b.add(1,2)
b = b.add(1,3)
b = b.add(2,3)
b.printrel("B")

ab = a.composition(b)
ab.printrel("A o B")

asb = a.subtract(b)
asb.printrel("A - B")


R = get_relation_class({1,2})

c = R()
c = c.add(1,2)
c = c.add(2,1)
c.printrel("C")

buc = b.union(c)
buc.printrel("B u C")





