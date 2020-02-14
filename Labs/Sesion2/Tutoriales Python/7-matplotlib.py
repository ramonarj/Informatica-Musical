'''
graficos: matplotlib
'''

#%% 

# linea solo para sacar el gráfico en el notebook
%matplotlib inline

import matplotlib.pyplot as plt
import numpy as np

x = list(range(10))
y = [v*v for v in x]

# Plot the data
plt.plot(x, y, label='x^2')

# La leyenda x^2
plt.legend()

# título 
plt.title("Una figura sencilla")

# mostrar el resultado
plt.show()

#%% cambiar colores, grosor...
plt.plot(x, y, label='x^2',color='green', linewidth=6)







#%% combinado con numpy
import numpy as np

t = np.arange(500)
a = np.sin(t/10)

plt.plot(t,a)

#%%
t = np.arange(500)
a = np.sin(t/10)


a2 = np.sin(t/10+400)

plt.plot(t,a)
plt.plot(t,a2)




#%% "bajamos volumen"
t = np.arange(500)
a = np.sin(t/10)

a1 = a*0.3

plt.plot(t,a)
plt.plot(t,a1)




#%% fade in/fade out
t = np.arange(500)
a = np.sin(t/10)
plt.plot(t,a)


env = np.arange(500)/500
a1 = a*env
plt.plot(t,a1)

env2 = env[::-1]  # forma ingeniosa de invertir
a2 = a*env2
plt.plot(t,a2)




#%% suma de señales
t = np.arange(500)

a = np.sin(t/20)
plt.plot(t,a)

b = np.sin(t/10)
plt.plot(t,b)

plt.plot(t,(a+b)/2)


#%% sumamos varios??
t = np.arange(1000)

ac = np.zeros_like(t)
for i in range(1,6):
    ac = ac + np.sin(t/(i*10))


plt.plot(t,ac)


#%% LFO
t = np.arange(1000)
a = np.sin(t/10)

lf = np.sin(t/100)

#plt.plot(t,a)
plt.plot(t,lf)

plt.plot(t,a*lf)





