import numpy as np
import pyaudio, kbhit
from scipy.io import wavfile # para manejo de wavs

# abrimos wav y recogemos frecMuestreo y array de datos
SRATE, data = wavfile.read('piano.wav')

# miramos formato de samples
if data.dtype.name == 'int16': fmt = 2
elif data.dtype.name == 'int32': fmt = 4
elif data.dtype.name == 'float32': fmt = 4
elif data.dtype.name == 'uint8': fmt = 1
else: raise Exception('Not supported')

CHUNK = 1024 # tamanio del buffer

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(fmt), # formato de los samples
    channels=len(data.shape), # num canales (shape de data)
    rate=SRATE, # frecuencia de muestreo
    frames_per_buffer=CHUNK, # tamanio buffer
    output=True) # stream de salida

# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
bloque = np.arange(CHUNK,dtype=data.dtype)
numBloque = 0
kb = kbhit.KBHit()
c= ' '
while c!= 'q':
    # nuevo bloque
    bloque = data[ numBloque*CHUNK : numBloque*CHUNK+CHUNK ]

    # pasamos al stream haciendo conversion de tipo
    stream.write(bloque.astype((data.dtype)).tobytes())

    if kb.kbhit():
        c = kb.getch()

    numBloque += 1

kb.set_normal_term()
stream.stop_stream()
stream.close()
p.terminate()
