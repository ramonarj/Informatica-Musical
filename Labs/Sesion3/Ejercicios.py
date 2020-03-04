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
MAX_KEYNO = 3
NUM_BLOQUES = [0, 0, 0]


def Ejercicios1y2(shape, frec, vol):
    '''
    Oscilador al que se le puede cambiar la frecuencia y volumen en ejecución
    '''
    print("Oscilador " + str(shape) + ": " + str(frec) + "Hz, Volumen: " + str(vol))

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
    volIncr = 0.05
    while c != 'q' and c != 'Q':
        samples = osc.next()
        stream.write(samples.astype(TYPE).tobytes())
        if kb.kbhit():
            vol = osc.getVol()
            frec = osc.getFrec()
            c = kb.getch()
            if(c == 'v'):
                osc.setVol(max(0,vol-volIncr))
            elif (c == 'V'):
                osc.setVol(min(1,vol+volIncr))
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



def Ejercicio3(shape, frec, vol):
    '''
    Oscilador que se va a modular con un seno
    '''
    print("Oscilador " + str(shape) + ": " + str(frec) + "Hz, Volumen: " + str(vol))

    # 1. Creamos instancias de PyAudio y de kbhit
    p = pyaudio.PyAudio()
    kb = kbhit.KBHit()

    # Miramos el formato de los samples (fmt)
    fmt = getFormat(TYPE)

    # 2. Creamos el oscilador, el modulador de amplitud...
    osc = Osc(shape, frec, vol)
    modAmp = ModulatorAmp(1) #1Hz

    # ... y el stream con los datos del oscilador
    stream = p.open(format=p.get_format_from_width(fmt), # formato de los samples
                    channels=1,                          # num canales
                    rate=osc.srate(),                          # frecuencia de muestreo
                    frames_per_buffer=osc.chunkSize(),             # tamanio buffer
                    output=True)                         # callback para leer los datos

    # 3. Reproducimos el oscilador por chunks
    print("Press 'q' to quit")
    c= ' '
    volIncr = 0.1
    while c != 'q' and c != 'Q':
        samples = osc.next()   
        modSamples = modAmp.next(samples)
        #plotWave(modSamples)
        stream.write(modSamples.astype(TYPE).tobytes())
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


    # 4. Finalización
    # Del stream
    stream.stop_stream()
    stream.close()
    # De kbhit y PyAudio
    kb.set_normal_term()
    p.terminate()


def Ejercicio8():
    '''
    Piano
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
    activeStreams = []
    while c != '0':
        print(activeStreams)
        global numBloque
        # Reseteamos el nº bloque si ha terminado el stream
        lol = ["1", "2","3"]
        for stream in (activeStreams):
            #print(lol)
            if(stream != None and not stream.is_active() and numBloque != 0):
                activeStreams.remove(stream)
                numBloque = 0
        # Pulsación de teclado
        if kb.kbhit():
            c = kb.getch()
            # Comprobamos que sea una tecla válida
            if(c in pianoKeys):
                if(len(activeStreams) > MAX_KEYNO):
                    stream = activeStreams.pop(0)
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
                activeStreams.append(stream)
        
        else:
            time.sleep(0.1)
            

    # De kbhit y PyAudio
    kb.set_normal_term()
    p.terminate()

#Ejercicios1y2("triangle", 440, 0.7)
#Ejercicio3("triangle", 440, 0.7)
Ejercicio8()