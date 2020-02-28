# Juan Ruiz Jiménez
# Ramón Arjona Quiñones
import numpy as np # Para los arrays
import pyaudio, wave # Para el audio
import kbhit # Para gestión de input
from scipy.io import wavfile # Para manejo de wavs
import time # Para esperar a la hebra
from Utilities import plotWave, Osc # Para pintar ondas y generar osciladores de varios tipos


CHUNK = 1024 # Tamaño de los bloques (en nº muestras)
numBloque = 0 # contador de bloques procesados (variable global)
SRATE = 44100 # frecuencia de muestreo para los osciladores
TYPE = np.float32 # generamos como floats en [0,1]

def ReproductorSimple(waveName):
    '''
    Ejemplo de un reproductor sin usar NumPy ni multihebra.
    Lee por chunks.
    '''
    # 1. Creamos instancias de PyAudio y de kbhit
    p = pyaudio.PyAudio()
    kb = kbhit.KBHit()

    # 2. Abrimos el archivo de audio y creamos un stream  de salida
    wf = wave.open(waveName, 'rb')
    # Formato del wav (int16/24/32, float32...)
    # Número de canales
    # Frecuencia de muestreo
    # Tipo del stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
    channels=wf.getnchannels(),
    rate=wf.getframerate(), 
    output=True) 

    # 3. Leemos los datos del wav (POR BLOQUES)
    data = wf.readframes(CHUNK)
    cont = 1

    #Hasta que se acabe
    while len(data) > 0:
        # Reproducimos el chunk guardado
        print("Reproduciendo chunk: ",cont)
        stream.write(data)

        # Leemos el siguente chunk
        data = wf.readframes(CHUNK)
        cont = cont+1

    # Esto es si lo leyéramos todo de golpe (BLOQUEANTE)
    #data = wf.readframes(wf.getnframes())
    #stream.write(data)

    # 5. Finalización
    # Del stream
    stream.stop_stream()
    stream.close()
    # De kbhit y PyAudio
    kb.set_normal_term()
    p.terminate()


def ReproductorNumpy(waveName):
    '''
    Ejemplo de reproductor usando NumPy y con subida/bajada de volumen,
    pero sin multihebra.
    '''
    # 1. Creamos instancias de PyAudio y de kbhit
    p = pyaudio.PyAudio()
    kb = kbhit.KBHit()

    # 2. Abrimos el archivo de audio y recogemos la SRATE y el array de datos
    frate, data = wavfile.read(waveName)

    # Miramos el formato de los samples (fmt)
    if data.dtype.name == 'int16': fmt = 2
    elif data.dtype.name == 'int32': fmt = 4
    elif data.dtype.name == 'float32': fmt = 4
    elif data.dtype.name == 'uint8': fmt = 1
    else: raise Exception('Not supported')

    # 3. Creamos el stream con los datos dados
    stream = p.open(format=p.get_format_from_width(fmt), # formato de los samples
                    channels=len(data.shape),            # num canales (shape de data)
                    rate=frate,                          # frecuencia de muestreo
                    frames_per_buffer=CHUNK,             # tamanio buffer
                    output=True)                         # stream de salida


    # 4. Reproducimos en el stream por chunks (en data está el wav completo)
    bloque = np.arange(CHUNK,dtype=data.dtype)
    numBloque = 0
    vol = 1.0
    c= ' '
    while (c!= 'q' and len(bloque) > 0):
        # Guardamos el nuevo bloque
        bloque = data[ numBloque*CHUNK : numBloque*CHUNK+CHUNK ]

        # Todas las muestras se multiplican por VOL (es global)
        bloque = bloque * vol

        # Lo pasamos al stream haciendo conversion de tipo
        stream.write(bloque.astype((data.dtype)).tobytes())
        if kb.kbhit():
            c = kb.getch()
            if(c == 'v'):
                vol= max(0,vol-0.05)
            elif (c == 'V'):
                vol= min(1,vol+0.05)
            print("Vol: ",vol)
        
        numBloque += 1


    # 5. Finalización
    # Del stream
    stream.stop_stream()
    stream.close()
    # De kbhit y PyAudio
    kb.set_normal_term()
    p.terminate()


def ReproductorMultiHebra(waveName):
    '''
    Reproductor que usa Numpy para cargar el WAV y 
    un callback para que lo use la hebra de PyAudio (exclusiva para el flujo de salida)
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
        print("Callback bloque ", numBloque, "fc ", frame_count)

        # Recogemos el bloque de array data
        bloque = data[ numBloque*CHUNK : numBloque*CHUNK+CHUNK ]
        numBloque += 1

        # Devolvemos el bloque
        return (bloque, pyaudio.paContinue)

    # 1. Creamos instancias de PyAudio y de kbhit
    p = pyaudio.PyAudio()
    kb = kbhit.KBHit()

    # 2. Abrimos el archivo de audio y recogemos la SRATE y el array de datos
    frate, data = wavfile.read(waveName)

    # Miramos el formato de los samples (fmt)
    if data.dtype.name == 'int16': fmt = 2
    elif data.dtype.name == 'int32': fmt = 4
    elif data.dtype.name == 'float32': fmt = 4
    elif data.dtype.name == 'uint8': fmt = 1
    else: raise Exception('Not supported')

    # 3. Creamos el stream con los datos dados
    stream = p.open(format=p.get_format_from_width(fmt), # formato de los samples
                    channels=len(data.shape),            # num canales (shape de data)
                    rate=frate,                           # frecuencia de muestreo
                    frames_per_buffer=CHUNK,             # tamanio buffer
                    output=True,                         # stream de salida
                    stream_callback=callback)            # callback para leer los datos

    # Lo iniciamos
    stream.start_stream()

    # Mientras no acabe el stream, mantenemos viva la hebra
    while stream.is_active(): 
        time.sleep(1)

    # 5. Finalización
    # Del stream
    stream.stop_stream()
    stream.close()
    # De kbhit y PyAudio
    kb.set_normal_term()
    p.terminate()

def ReproductorOsc(shape:str, frec:int, vol:float):
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

#ReproductorSimple('muestras/piano.wav')
#ReproductorNumpy('muestras/piano.wav')
#ReproductorMultiHebra('muestras/piano.wav')
ReproductorOsc("triangle", 200, 1)