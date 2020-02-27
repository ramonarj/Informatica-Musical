import pyaudio, wave, kbhit

CHUNK = 1024 
FORMAT = pyaudio.paFloat32
CHANNELS = 1 
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS,
    rate=RATE, input=True, # ahora es flujo de entrada
    frames_per_buffer=CHUNK) # tamanio buffer == CHUNK !!

frames = [] # lista de samples

kb = kbhit.KBHit()
c = ' '
while c != 'q': # grabando
    data = stream.read(CHUNK) # recogida de samples
    frames.append(data)
    print("Grabando...")
    if kb.kbhit(): c = kb.getch()

kb.set_normal_term() 
stream.stop_stream() 
stream.close() 
p.terminate()

# guardamos wav
wf = wave.open("record.wav", 'wb')
wf.setnchannels(CHANNELS) 
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
