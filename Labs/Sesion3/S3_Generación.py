# Juan Ruiz Jiménez
# Ramón Arjona Quiñones
import numpy as np # Para los arrays
import pyaudio, wave # Para el audio
import kbhit # Para gestión de input
from scipy.io import wavfile # Para manejo de wavs
import time # Para esperar a la hebra
from Utilities import plotWave, Osc # Para pintar ondas y generar osciladores de varios tipos

SRATE = 44100 # frecuencia de muestreo para los osciladores
CHUNK = 1024
TYPE = np.float32 # generamos como floats en [0,1]


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