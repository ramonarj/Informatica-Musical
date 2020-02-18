import numpy as np
import matplotlib.pyplot as plt

SRATE = 44100


def plotWave(x:np.array, y:np.array):
    '''
    Pinta una señal dada 
    '''
    plt.plot(x, y)
    plt.xlabel('Tiempo')
    plt.ylabel('Intensidad')
    plt.axis('tight')
    plt.show()

def sin(frec:int, dur:float):
    '''
    Oscilador con forma de seno
    '''
    # Creamos eje X 
    x = np.linspace(0, dur, SRATE * dur)
    lamda = 1 / frec #long.onda

    # Seno
    y = np.sin((2 * np.pi * x) / lamda)

    return x, y

def square(frec:int, dur:float):
    '''
    Oscilador con forma de cuadrado
    '''
    # Partimos del seno
    x, y = sin(frec, dur) 

    # Cuadrado
    y = np.where(np.sign(y) >= 0, 1, -1)

    return x, y


def triangle(frec:int, dur:float):
    '''
    Oscilador con forma de triángulo
    '''
    # Partimos del seno
    x, y = sin(frec, dur) 

    # Triángulo
    y = 2 / np.pi * np.arcsin(y)

    return x, y

def saw(frec:int, dur:float):
    '''
    Oscilador con forma de diente de sierra
    '''
    # Creamos eje X 
    x = np.linspace(0, dur, SRATE * dur)
    lamda = 1 / frec #long.onda

    # Diente de sierra
    tanTerm = np.tan((2 * np.pi * x) / (2 * lamda))
    y = 2 / np.pi * np.arctan(tanTerm)

    return x, y


def main():
    x, y = sin(1,1)
    plotWave(x, y)
    x, y = square(1,1)
    plotWave(x, y)
    x, y = triangle(1,1)
    plotWave(x, y)
    x, y = saw(1,1)
    plotWave(x, y)


main()
