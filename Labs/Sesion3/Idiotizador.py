#Ramon Arjona Quiñones
#Juan Ruiz Jimenez

import pyaudio, wave, kbhit, time
import numpy as np

CHUNK = 1024 
FORMAT = pyaudio.paInt16
CHANNELS = 2 
RATE = 44100

p = pyaudio.PyAudio()

# Stream para la grabacion
rec_stream = p.open(format=FORMAT, channels=CHANNELS,
    rate=RATE, input=True, # ahora es flujo de entrada
    frames_per_buffer=CHUNK) # tamanio buffer == CHUNK !!

# Stream para la reproduccion
out_stream = p.open(format=FORMAT, channels=CHANNELS,
    rate=RATE, output=True) #flujo de salida

frames = [] # lista de samples

kb = kbhit.KBHit()
c = ' '
indx = 0

delay = 0.1

timer_flag = True
timer_start = time.time()

# Bucle ppal
# Hasta que no se pase el tiempo de delay, no se reproduce
while c != 'q': # grabando

	if timer_flag:
		data = rec_stream.read(CHUNK) # recogida de samples
		frames.append(data) 
		timer_end = time.time()

		if timer_end - timer_start > delay:
			timer_flag = False

	else:
		data = rec_stream.read(CHUNK) # recogida de samples
		frames.append(data)       
		out_stream.write(frames[indx]) # reproduccion
		indx+=1

	if kb.kbhit(): 
		c = kb.getch()

kb.set_normal_term() 

rec_stream.stop_stream() 
rec_stream.close() 

out_stream.stop_stream() 
out_stream.close() 

p.terminate()