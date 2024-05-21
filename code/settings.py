import pygame
from os.path import join
from os import walk

#Importa imagens
def import_image(*path, alpha = True, format = 'png'):
    full_path = join(*path) + f'.{format}'
    surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    return surf

def import_folder(*path):
	frames = []
	for folder_path, sub_folders, image_names in walk(join(*path)):
		for image_name in sorted(image_names, key = lambda name: int(name.split('.')[0])):
			full_path = join(folder_path, image_name)
			surf = pygame.image.load(full_path).convert_alpha()
			frames.append(surf)
	return frames

# Tamanho da janela
WINDOW_WIDTH = 864
WINDOW_HEIGHT = 730

# Tamanho das cartas e margem
CARD_WIDTH = 175
CARD_HEIGHT = 175
MARGIN = 10

IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128

# FPS
FPS = 60

# Cores
BLUE = (162, 202, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
STEELBLUE = (70,130,180)
GRAY =  (160,160,160)


# Número de colunas e largura de cada coluna
NUM_COLUNAS = 5
COL_WIDTH = WINDOW_WIDTH // NUM_COLUNAS
    
def calcular_coordenadas_imagens(NUM_COLUNAS, WINDOW_WIDTH, WINDOW_HEIGHT, MARGIN, IMAGE_WIDTH, IMAGE_HEIGHT):
    coordenadas = {}
    for i in range(NUM_COLUNAS):
        coluna = f'coluna{i+1}'
        coordenadas[coluna] = []
        for j in range(6):
            x = j * (IMAGE_WIDTH + MARGIN)
            y = i * (IMAGE_HEIGHT + MARGIN)
            coordenadas[coluna].append((x, y))
    return coordenadas

COORDENADAS_IMAGE = calcular_coordenadas_imagens(NUM_COLUNAS, WINDOW_WIDTH, WINDOW_HEIGHT, MARGIN, IMAGE_WIDTH, IMAGE_HEIGHT)