# Juan Ruiz Jiménez
# Ramón Arjona Quiñones
import numpy as np # Para los arrays
import pyaudio, wave # Para el audio
import pygame # Para el control de input sobre la pantalla
from pygame.locals import *

CHUNK = 1024 # Tamaño de los bloques (en nº muestras)
SRATE = 44100 # frecuencia de muestreo para los osciladores
TYPE = np.float32 # generamos como floats en [0,1]
CHANNELS = 2 # numero de canales
W_WIDTH = 640 # ancho de la pantalla
W_HEIGHT = 480 # alto de la pantalla

p = pyaudio.PyAudio()
#Stream de salida
stream = p.open(format=p.get_format_from_width(4), 
                channels=CHANNELS,
                rate=SRATE,
                output=True,
                frames_per_buffer=CHUNK)

# Creamos la pantalla de pygame
screen = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
pygame.display.set_caption("Theremin")

# Sintetizador a traves del cual generaremos el sonido
# [(fc,vol),(fm1,beta1),(fm2,beta2),..
def oscFM(frecs,frame):
    chunk = np.arange(CHUNK)+frame # array de frames
    samples = np.zeros(CHUNK)+frame # acumulador de síntesis

    # recorremos en orden inverso
    for i in range(len(frecs)-1,-1,-1):
        # utilizamos samples como moduladora de una nueva portadora
        samples = frecs[i][1] * np.sin(2*np.pi*frecs[i][0]*chunk/SRATE + samples)

    return samples

# Bucle ppal
quit_flag = False
mouse_x = 0
mouse_y = 0
frame = 0

while not quit_flag:

    # obtencion de la posicion del raton
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
        elif event.type == pygame.QUIT:
            quit_flag = True

    datas = []
    datas.append(mouse_x * (1000 / W_WIDTH) + 100)
    datas.append(1 - (mouse_y / W_HEIGHT))

    result = []
    result.append(datas)

    data = oscFM(result, 0)
    stream.write(data)
    frame += 1

pygame.quit()