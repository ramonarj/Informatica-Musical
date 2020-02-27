import pyaudio, wave

#constantes
CHUNK = 1024 

# abrimos archivo de audio
wf = wave.open('piano.wav', 'rb')
# creamos instancia de pyAudio (inicializacion del sistema)
p = pyaudio.PyAudio()
# abrimos stream
# formato del wav: int16/24/32, float32, ...
stream = p.open(
    format=p.get_format_from_width(wf.getsampwidth()),
    channels=wf.getnchannels(), # num canales
    rate=wf.getframerate(), # frecuencia de muestreo
    output=True) # stream de salida

# leemos del wav por bloques
data = wf.readframes(CHUNK)

# escribimos al stream por chunks
cont = 1
while len(data) > 0:
    print("Reproduciendo chunk: ",cont)
    stream.write(data)
    data = wf.readframes(CHUNK)
    cont = cont+1

# finalizamos streams
stream.stop_stream()
stream.close()

# finalizamos pyAudio
p.terminate()