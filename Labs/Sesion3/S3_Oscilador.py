import pyaudio, kbhit
import numpy as np

RATE = 44100
CHUNK = 1024
FORMAT = pyaudio.paFloat32

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT, # formato de los samples
    channels=1, # num canales (shape de data)
    rate=RATE, # frecuencia de muestreo
    frames_per_buffer=CHUNK, # tamanio buffer
    output=True) # stream de salida

last = 0 # ultimo frame generado
def oscChuck(frec,vol):
    global last # var global
    data = vol*np.sin(2*np.pi*(np.arange(CHUNK)+last)*frec/RATE)
    last += CHUNK # actualizamos ultimo generado
    return data

frec = 440
vol = 0.7
kb = kbhit.KBHit()
c= ' '
while c!= 'q':
    # pasamos al stream haciendo conversion de tipo
    samples = oscChuck(frec,vol)
    stream.write(samples.astype(np.float32).tobytes())

    if kb.kbhit():
        c = kb.getch()

kb.set_normal_term()
stream.stop_stream()
stream.close()
p.terminate()