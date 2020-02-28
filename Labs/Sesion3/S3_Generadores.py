# Juan Ruiz Jiménez
# Ramón Arjona Quiñones
import numpy as np # Para los arrays
import pyaudio, wave # Para el audio
import kbhit # Para gestión de input
from scipy.io import wavfile # Para manejo de wavs
import time # Para esperar a la hebra
from Utilities import plotWave, sin, square, saw, triangle # Para pintar ondas y generar osciladores de varios tipos

SRATE = 44100 # frecuencia de muestreo para los osciladores
CHUNK = 1024
TYPE = np.float32 # generamos como floats en [0,1]

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


def GeneradorOSC(shape:str, frec:int, vol:float):
    '''
    Reproduce una onda recibiendo ya los datos, no un WAV
    (podría ser un oscilador o un WAV)
    '''
    # 1. Creamos instancias de PyAudio y de kbhit
    p = pyaudio.PyAudio()
    kb = kbhit.KBHit()

    # Miramos el formato de los samples (fmt)
    if TYPE == np.int16: fmt = 2
    elif TYPE == np.int32: fmt = 4
    elif TYPE == np.float32: fmt = 4
    elif TYPE == np.uint8: fmt = 1
    else: raise Exception('Not supported')

    # 3. Creamos el stream con los datos del oscilador
    osc = Osc(shape, frec, vol)
    stream = p.open(format=p.get_format_from_width(fmt), # formato de los samples
                    channels=1,                          # num canales
                    rate=osc.srate(),                          # frecuencia de muestreo
                    frames_per_buffer=osc.chunkSize(),             # tamanio buffer
                    output=True)                         # callback para leer los datos

    # Reproducimos el oscilador
    print("Press 'q' to quit")
    c= ' '
    while c != 'q':
        samples = osc.next()
        stream.write(samples.astype(TYPE).tobytes())
        if kb.kbhit():
            c = kb.getch()

    # 5. Finalización
    # Del stream
    stream.stop_stream()
    stream.close()
    # De kbhit y PyAudio
    kb.set_normal_term()
    p.terminate()
    

GeneradorOSC("square", 200, 1)