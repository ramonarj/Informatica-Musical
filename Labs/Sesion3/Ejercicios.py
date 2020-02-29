# Juan Ruiz Jiménez
# Ramón Arjona Quiñones
import numpy as np # Para los arrays
import pyaudio, wave # Para el audio
import kbhit # Para gestión de input
from scipy.io import wavfile # Para manejo de wavs
import time # Para esperar a la hebra
from Utilities import plotWave, sin, square, saw, triangle, Osc # Para pintar ondas y generar osciladores de varios tipos
from S3_Generadores import GeneradorOSC


CHUNK = 1024 # Tamaño de los bloques (en nº muestras)
numBloque = 0 # contador de bloques procesados (variable global)
SRATE = 44100 # frecuencia de muestreo para los osciladores
TYPE = np.float32 # generamos como floats en [0,1]


def Ejercicio1(shape, frec, vol):
    '''
    Oscilador al que se le puede cambiar la frecuencia y volumen en ejecución
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
    volIncr = 0.1
    while c != 'q':
        samples = osc.next()
        stream.write(samples.astype(TYPE).tobytes())
        if kb.kbhit():
            vol = osc.getVol()
            frec = osc.getFrec()
            c = kb.getch()
            if(c == 'v'):
                osc.setVol(max(0,vol-0.05))
            elif (c == 'V'):
                osc.setVol(min(1,vol+0.05))
            if(c == 'f'):
                osc.setFrec(max(20,frec-10))
            elif (c == 'F'):
                osc.setFrec(min(20000,frec+10))
            print("Vol: ",vol)
            print("Frec: ",frec)


    # 5. Finalización
    # Del stream
    stream.stop_stream()
    stream.close()
    # De kbhit y PyAudio
    kb.set_normal_term()
    p.terminate()

Ejercicio1("square", 440, 0.7)