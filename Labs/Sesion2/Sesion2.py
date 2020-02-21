# Juan ?? ??
# Ramón Arjona Quiñones

import numpy as np
import matplotlib.pyplot as plt

SRATE = 44100
BUF_SIZE = 1024

def plotWave(sample):
    '''
    Pinta una señal dada (con datos para ambos ejes)
    '''
    x = np.linspace(0, len(sample) / SRATE, num=len(sample))
    y = sample
    plt.plot(x, y)
    plt.xlabel('Tiempo')
    plt.ylabel('Intensidad')
    plt.axis('tight')
    plt.show()

def sin(frec:int, dur:float, fase=0):
    '''
    Oscilador con forma de seno
    '''
    # Creamos eje X 
    x = np.linspace(0, dur, SRATE * dur)
    lamda = 1 / frec #long.onda

    # Seno
    y = np.sin((2 * np.pi * x) / lamda + fase)

    return y

def square(frec:int, dur:float):
    '''
    Oscilador con forma de cuadrado
    '''
    # Partimos del seno
    y = sin(frec, dur) 

    # Cuadrado
    y = np.where(np.sign(y) >= 0, 1, -1)

    return y


def triangle(frec:int, dur:float):
    '''
    Oscilador con forma de triángulo
    '''
    # Partimos del seno
    y = sin(frec, dur) 

    # Triángulo
    y = 2 / np.pi * np.arcsin(y)

    return y

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

    return y


def vol(sample, factor):
    '''
    Cambia el volumen según el factor dado a la función
    '''

    # Multiplicamos
    sample *= factor

    return sample

def fadeOut(sample, t:float):
    '''
    Desvanece la señal desde el instante indicado hasta el final
    '''

    # Multiplicamos
    fadedSamples = (int)(len(sample) - SRATE * t)
    fadeLevels = np.flip(np.arange(0.0, 1.0, step=1/fadedSamples))
    sample[-fadedSamples:] *= fadeLevels

    return sample


def fadeIn(sample, t:float):
    '''
    Desvanece la señal desde el principio hasta el instante indicado
    '''

    # Multiplicamos
    fadedSamples = (int)(SRATE * t)
    fadeLevels = np.arange(0.0, 1.0, step=1/fadedSamples)
    sample[:fadedSamples] *= fadeLevels

    return sample


class Osc:
    '''
    Clase para representar a un oscilador sinusoidal que funciona por chunks
    '''
    def __init__(self, frec):
        self.frec = frec
        self.fase = 0

    def next(self):
        '''
        Devuelve el siguente chunk (de tamaño BUF_SIZE)
        '''
        # Obtenemos el siguiente chunk
        seno = sin(self.frec, BUF_SIZE / SRATE, self.fase)

        # Desfasamos la onda para la próxima vez
        self.fase += (BUF_SIZE / SRATE) * self.frec * 2 * np.pi
        return seno


def main():
    '''
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
    '''

    # Ejercicio 4
    osc = Osc(1)
    sample = osc.next()
    for i in range (80):
        sample = np.concatenate((sample, osc.next()), axis=None)

    plotWave(sample)
    

main()