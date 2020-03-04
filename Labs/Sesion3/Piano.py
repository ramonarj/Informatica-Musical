# Juan Ruiz Jiménez
# Ramón Arjona Quiñones

import numpy as np # Para los arrays
import pyaudio, wave # Para el audio
import kbhit # Para gestión de input
from scipy.io import wavfile # Para manejo de wavs
import time # Para esperar a la hebra
from Utilities import plotWave, Osc, ModulatorAmp, getFormat, getFormatFromString # Para pintar ondas y generar osciladores de varios tipos

CHUNK = 1024 # Tamaño de los bloques (en nº muestras)
numBloque = 0 # contador de bloques procesados (variable global)
SRATE = 44100 # frecuencia de muestreo para los osciladores
TYPE = np.float32 # generamos como floats en [0,1]

pianoKeys = {'z':0, 's':1, 'x':2, 'd':3, 'c':4, 'v':5, 'g':6, 'b':7, 'h':8, 'n':9, 'j':10, 'm':11, 'q':12, '2':13, 'w':14, '3':15, 'e':16, 'r':17, '5':18, 't':19, '6':20, 'y':21, '7':22, 'u':23} 

def Piano():
    '''
    Piano con el teclado (ZXC... para la 3º octava y QWE... para la 4º)
    '''
    # Nos definimos el callback aqui mismo para tener acceso a 'data' (y no hacerlo global)
    def callback(in_data, frame_count, time_info, status):
        '''
        Función que será llamada por la hebra de PyAudio 
        para leer chinks
        -> frame_count: numero de frames a devolver
        -> frame_count = frames_per_buffer = CHUNK
        '''
        global numBloque # para incrementar aquí
        #print("Callback bloque ", numBloque, "fc ", frame_count)

        # Recogemos el bloque de array data
        bloque = data[ numBloque*CHUNK : numBloque*CHUNK+CHUNK ]
        numBloque += 1

        # Devolvemos el bloque
        return (bloque, pyaudio.paContinue)

    # 1. Creamos instancias de PyAudio y de kbhit
    p = pyaudio.PyAudio()
    kb = kbhit.KBHit()

    # 2. Abrimos el archivo de audio y recogemos la SRATE y el array de datos
    frate, data = wavfile.read("muestras/piano.wav")

    # Miramos el formato de los samples (fmt)
    fmt = getFormatFromString(data.dtype.name)

    # 3. Reproducimos el oscilador por chunks
    print("Press '0' to quit")
    c= ' '
    volIncr = 0.1
    stream = None
    while c != '0':
        # Reseteamos el nº bloque si ha terminado el stream
        if(stream != None and not stream.is_active()):
            global numBloque
            numBloque = 0
        # Pulsación de teclado
        if kb.kbhit():
            c = kb.getch()
            # Comprobamos que sea una tecla válida
            if(c in pianoKeys):
                # Se toca una nota que ya estaba sonando
                if(stream != None and stream.is_active()):
                    stream.stop_stream()
                    numBloque = 0
                # Creamos el stream con la nota dada
                noteRate = (int)(frate * (2 ** (pianoKeys[c] / 12.0)))
                stream = p.open(format=p.get_format_from_width(fmt), # formato de los samples
                        channels=len(data.shape),            # num canales (shape de data)
                        rate=noteRate,                           # frecuencia de muestreo
                        frames_per_buffer=CHUNK,             # tamanio buffer
                        output=True,                         # stream de salida
                        stream_callback=callback)            # callback para leer los datos
                stream.start_stream()
        
        else:
            time.sleep(0.1)
            

    # De kbhit y PyAudio
    kb.set_normal_term()
    p.terminate()

Piano()