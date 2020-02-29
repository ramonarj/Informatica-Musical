# Juan Ruiz Jiménez
# Ramón Arjona Quiñones
import numpy as np # Para los arrays
import pyaudio, wave # Para el audio
import kbhit # Para gestión de input
from scipy.io import wavfile # Para manejo de wavs
import time # Para esperar a la hebra
from Utilities import plotWave, sin, square, saw, triangle, Osc # Para pintar ondas y generar osciladores de varios tipos


CHUNK = 1024 # Tamaño de los bloques (en nº muestras)
numBloque = 0 # contador de bloques procesados (variable global)
SRATE = 44100 # frecuencia de muestreo para los osciladores
TYPE = np.float32 # generamos como floats en [0,1]

