import pygame
from os.path import join
from os import walk

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

def calculate_coordinates_images(NUM_COLUMNS, WINDOW_WIDTH, WINDOW_HEIGHT, MARGIN, IMAGE_WIDTH, IMAGE_HEIGHT):
    coordinates = {}
    for i in range(NUM_COLUMNS):
        column = f'column{i+1}'
        coordinates[column] = []
        for j in range(6):
            x = j * (IMAGE_WIDTH + MARGIN)
            y = i * (IMAGE_HEIGHT + MARGIN)
            coordinates[column].append((x, y))
    return coordinates

# Tamanho da janela
WINDOW_WIDTH = 864
WINDOW_HEIGHT = 730

FPS = 60

# Tamanho das cartas e margem
CARD_WIDTH = 175
CARD_HEIGHT = 175
MARGIN = 10

# Tamanho das imagens
IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128

# Cores
BLUE = (162, 202, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
STEELBLUE = (70,130,180)
GRAY =  (160,160,160)

# Número de colunas e largura de cada coluna
NUM_COLUMNS = 5
COL_WIDTH = WINDOW_WIDTH // NUM_COLUMNS
    
COORDINATE_IMAGE = calculate_coordinates_images(NUM_COLUMNS, WINDOW_WIDTH, WINDOW_HEIGHT, MARGIN, IMAGE_WIDTH, IMAGE_HEIGHT)