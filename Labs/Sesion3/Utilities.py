# Juan Ruiz Jiménez
# Ramón Arjona Quiñones

import numpy as np
import matplotlib.pyplot as plt

#Por defecto
SRATE = 44100
CHUNK = 1024

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
    # Seno
    y = np.sin(2 * np.pi * (np.arange(CHUNK) + fase) * frec / SRATE)

    return y

def square(frec:int, dur:float, fase = 0):
    '''
    Oscilador con forma de cuadrado
    '''
    # Partimos del seno
    y = sin(frec, dur, fase) 

    # Cuadrado
    y = np.where(np.sign(y) >= 0, 1, -1)

    return y


def triangle(frec:int, dur:float, fase=0):
    '''
    Oscilador con forma de triángulo
    '''
    # Partimos del seno
    y = sin(frec, dur, fase) 

    # Triángulo
    y = 2 / np.pi * np.arcsin(y)

    return y

def saw(frec:int, dur:float, fase=0):
    '''
    Oscilador con forma de diente de sierra
    '''
    # Diente de sierra
    tanTerm = np.tan((2 * np.pi * (np.arange(CHUNK) + fase) * 2 * frec) / SRATE)
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