# Juan Ruiz Jiménez
# Ramón Arjona Quiñones

import numpy as np
import matplotlib.pyplot as plt

#Por defecto
SRATE = 44100
CHUNK = 1024

def getFormat(formatType):
    '''
    Devuelve 1, 2 3 o 4
    '''
    if formatType == np.int16: fmt = 2
    elif formatType == np.int32: fmt = 4
    elif formatType == np.float32: fmt = 4
    elif formatType == np.uint8: fmt = 1
    else: raise Exception('Not supported')

    return fmt


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


## GENERADORES ##
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


class Osc:
    '''
    Clase para representar a un oscilador que funciona por chunks.
    Puede reproducir ondas de seno, cuadrado, triángulo o sierra
    '''
    def __init__(self, shape:str, frec:int, vol:float):
        '''
        Constructora, recibe el tipo de onda, la frecuencia y el volumen
        '''
        self.frec = frec
        self.fase = 0
        self.vol = vol

        # Nos quedamos con cuál será la función que genera la forma de onda que queremos
        if(shape == "sin"):
            self.generator = sin
        elif(shape == "square"):
            self.generator = square
        elif(shape == "triangle"):
            self.generator = triangle
        elif(shape == "saw"):
            self.generator = saw


    def next(self):
        '''
        Devuelve el siguente chunk (de tamaño CHUNK)
        '''
        # Obtenemos el siguiente chunk
        dur = float(CHUNK) / float(SRATE) # duración del chunk
        data = self.vol * self.generator(self.frec, dur, self.fase) # oscilador con una frecuencia, duración y fase dadas

        # Desfasamos la onda para la próxima vez
        self.fase += CHUNK
        return data

    def srate(self):
        '''
        Devuelve el sample rate usado
        '''
        return SRATE

    def chunkSize(self):
        '''
        Devuelve el tamaño usado para los chunks
        '''
        return CHUNK

    def setVol(self, newVol):
        '''
        Cambia el volumen
        '''
        self.vol = newVol
    
    def getVol(self):
        '''
        Devuelve el volumen
        '''
        return self.vol

    def setFrec(self, newFrec):
        '''
        Cambia el volumen
        '''
        self.frec = newFrec
    
    def getFrec(self):
        '''
        Devuelve el volumen
        '''
        return self.frec


## PROCESAMIENTO ##

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


class ModulatorAmp:
    '''
    Clase para representar a un oscilador que funciona por chunks.
    Puede reproducir ondas de seno, cuadrado, triángulo o sierra
    '''
    def __init__(self, frec:int):
        '''
        Constructora, recibe el tipo de onda, la frecuencia y el volumen
        '''
        self.frec = frec
        self.fase = 0

    def next(self, data):
        '''
        Devuelve el siguente chunk (de tamaño CHUNK)
        '''

        dur = float(len(data)) / float(SRATE)
        sinData = sin(self.frec, dur, self.fase) 

        self.fase += CHUNK
        return data * sinData

'''
def ModulatorAmp(data, frec):
    dur = float(len(data)) / float(SRATE)
    sinData = sin(frec, dur, 0) 
    return data * sinDat
'''