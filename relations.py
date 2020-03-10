from pyrsistent import s, freeze


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

    def inverse(self):
        return Relation(self.M,
                        freeze(set(x[::-1] for x in self.rel)))

    def composition(self,R):
        return Relation(self.M.union(R.M),
                        freeze(set( (a,c) for (a,b1) in R.rel
                                    for (b2,c) in self.rel if b1 == b2)))

    def reflexive(self):
        return all(self.contains(a,a) for a in self.M)

    def symmetric(self):
        return all(self.contains(b,a) for (a,b) in self.rel)

    def transitive(self):
        return all(self.contains(a,c) or b1 != b2
                   for (a,b1) in self.rel for (b2,c) in self.rel)

    def closure(self):
        R = Relation(self.M,freeze(set((a,a) for a in self.M)).union(self.rel))
        while not R.composition(self).rel.issubset(R.rel):
            R = R.union(R.composition(self))
        return R

    def printrel(self,text):
        print()
        print(text,"=",self.rel)
        print("reflexivna?",self.reflexive())
        print("symetricka?",self.symmetric())
        print("tranzitivna?",self.transitive())



def get_relation_class(M):
    return Relation(M)


a = get_relation_class({1,2,3,4})
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

b = get_relation_class({1,2,3})
b = b.add(1,2)
b = b.add(1,3)
b = b.add(2,3)
b.printrel("B")

ab = a.composition(b)
ab.printrel("A o B")

asb = a.subtract(b)
asb.printrel("A - B")

c = get_relation_class({1,2})
c = c.add(1,2)
c = c.add(2,1)
c.printrel("C")

buc = b.union(c)
buc.printrel("B u C")





