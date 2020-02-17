import numpy as np
import matplotlib.pyplot as plt

SRATE = 44100


def plotWave(x:np.array, y:np.array):
    '''
    Pinta una señal dada 
    '''
    plt.plot(x, y)
    plt.xlabel('Tiempo')
    plt.ylabel('Valor')
    plt.axis('tight')
    plt.show()

def sin(frec:int, dur:float):
    '''
    Oscilador con forma de seno
    '''
    # Creamos eje X
    x = np.linspace(0, dur * frec, SRATE * dur)
    
    # Seno
    y = np.sin(x * 2 * np.pi)

    # "Comprimimos" la onda a la duración de verdad
    x = x/frec
    return x, y

def saw(frec:int, dur:float):
    '''
    Oscilador con forma de diente de sierra
    '''
    # Creamos eje X: lo creamos de "dur*frec" segundos para hacer como si fuera una onda de 1Hz; 
    # así luego al comprimir estos valores a la duración real, la onda queda con la frecuencia adecuada.
    x = np.linspace(0, dur * frec, SRATE * dur)

    # Diente de sierra
    incr = x - np.floor(x) #Entre 0 y 1
    y = 2 * incr - 2 * np.around(incr) 

    # "Comprimimos" la onda a la duración de verdad
    x = x / frec
    return x, y


def square(frec:int, dur:float):
    '''
    Oscilador con forma de cuadrado
    '''
    # Creamos eje X 
    x = np.linspace(0, dur * frec, SRATE * dur)

    # Cuadrado
    incr = x - np.floor(x)
    y = 1 - 2 * np.around(incr)

    # "Comprimimos" la onda a la duración de verdad
    x = x / frec
    return x, y


def triangle(frec:int, dur:float):
    '''
    Oscilador con forma de triángulo
    '''
    # Creamos eje X 
    x = np.linspace(0, dur * frec, SRATE * dur)

    # Triángulo
    # TODO: hacerlo

    # "Comprimimos" la onda a la duración de verdad
    x = x / frec
    return x, y


def main():
    x, y = triangle(1,1)
    plotWave(x, y)


main()
