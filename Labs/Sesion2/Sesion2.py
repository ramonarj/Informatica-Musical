import numpy as np
import matplotlib.pyplot as plt

SRATE = 44100

def plotWave(sample):
    '''
    Pinta una señal dada 
    '''
    x = sample[0]
    y = sample[1]
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

    return [x, y]

def square(frec:int, dur:float):
    '''
    Oscilador con forma de cuadrado
    '''
    # Partimos del seno
    x, y = sin(frec, dur) 

    # Cuadrado
    y = np.where(np.sign(y) >= 0, 1, -1)

    return [x, y]


def triangle(frec:int, dur:float):
    '''
    Oscilador con forma de triángulo
    '''
    # Partimos del seno
    x, y = sin(frec, dur) 

    # Triángulo
    y = 2 / np.pi * np.arcsin(y)

    return [x, y]

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

    return [x, y]


def vol(sample, factor):
    '''
    Cambia el volumen según el factor dado a la función
    '''
    x = sample[0]
    y = sample[1]

    # Multiplicamos
    y *= factor

    return [x, y]

def fadeOut(sample, t:float):
    '''
    Desvanece la señal desde el instante indicado hasta el final
    '''
    x = sample[0]
    y = sample[1]

    # Multiplicamos
    fadedSamples = (int)(len(y) - SRATE * t)
    fadeLevels = np.flip(np.arange(0.0, 1.0, step=1/fadedSamples))
    y[-fadedSamples:] *= fadeLevels

    return [x, y]


def fadeIn(sample, t:float):
    '''
    Desvanece la señal desde el principio hasta el instante indicado
    '''
    x = sample[0]
    y = sample[1]

    # Multiplicamos
    fadedSamples = (int)(SRATE * t)
    fadeLevels = np.arange(0.0, 1.0, step=1/fadedSamples)
    y[:fadedSamples] *= fadeLevels

    return [x, y]


def main():
    # Creamos generadores
    sinSamp= sin(5,10)
    squareSamp = square(5,10)
    triangleSamp = triangle(5,10)
    sawSamp = saw(5,5)

    # Efectos
    sample = sawSamp
    sample = vol(sample, 2)
    sample = fadeIn(sample, 2.5)
    sample = fadeOut(sample, 2.5)
    plotWave(sample)


main()