#%%
class Complex:
    def __init__(self, r=0, i=0):
        self.real = r
        self.img  = i
    
    def add(self, c):
        self.real += c.real
        self.img  += c.img
    
    def write(self):
        print('{} + {}i'.format(self.real, self.img))

    # otra forma: sobrecarga de str
    def __str__(self):
        return '{} + {}i'.format(self.real, self.img)

    # resta con sobrecarga (devuelve uno nuevo)
    def __sub__(self,c):
        return Complex(
            self.real - c.real,
            self.img  - c.img)


c1 = Complex(1,2)
c1.write()

c2 = Complex()
c2.write()

c3 = Complex(6)
c1.add(c3)

# utilizando la sobrecarda de c1
print(c1)

print(c3-c1)

# tb hay herencia
