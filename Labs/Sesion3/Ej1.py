import numpy as np
import matplotlib.pyplot as plt
import pyaudio, wave


def main():
    # 1. Inicialización
    # abrimos archivo de audio
    wf = wave.open('bombo.wav', 'rb')

    # creamos instaancia de pyAudio (inicializacion del sistema)
    p = pyaudio.PyAudio()

    # 2. abrimos stream
    stream = p.open(
    # formato del wav: int16/24/32, float32, ...
    format=p.get_format_from_width(wf.getsampwidth()),
    channels=wf.getnchannels(), # num canales
    rate=wf.getframerate(), # frecuencia de muestreo
    output=True) # stream de salida

    # 3. leemos TODOS los datos del wav
    data = wf.readframes(wf.getnframes())
    # escribimos al stream. BLOQUEANTE!!
    stream.write(data)

    # 4.Finalizamos 
    # stream
    stream.stop_stream()
    stream.close()

    # pyAudio
    p.terminate()


main()
