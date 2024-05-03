import pygame
from os.path import join
from os import walk

#Importa imagens
def import_image(*path, alpha = True, format = 'png'):
    full_path = join(*path) + f'.{format}'
    surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    return surf

# Tamanho da janela
WINDOW_WIDTH = 630
WINDOW_HEIGHT = 570

# FPS
FPS = 60

# Cores
BLUE = (162, 202, 255)

#Colunas
COLUNAS = {
    
    'coluna1': [(0, WINDOW_WIDTH // 2 * 0),
                (100, WINDOW_WIDTH // 2 * 0),
                (200, WINDOW_WIDTH // 2 * 0),
                (300, WINDOW_WIDTH // 2 * 0),
                (400, WINDOW_WIDTH // 2 * 0),
                (500, WINDOW_WIDTH // 2 * 0)],
     
    'coluna2': [(0, WINDOW_WIDTH // 2 * 0.35),
                (100, WINDOW_WIDTH // 2 * 0.35),
                (200, WINDOW_WIDTH // 2 * 0.35),
                (300, WINDOW_WIDTH // 2 * 0.35),
                (400, WINDOW_WIDTH // 2 * 0.35),
                (500, WINDOW_WIDTH // 2 * 0.35)],
    
    'coluna3': [(0, WINDOW_WIDTH // 2 * 0.7),
                (100, WINDOW_WIDTH // 2 * 0.7),
                (200, WINDOW_WIDTH // 2 * 0.7),
                (300, WINDOW_WIDTH // 2 * 0.7),
                (400, WINDOW_WIDTH // 2 * 0.7),
                (500, WINDOW_WIDTH // 2 * 0.7)],
    
     'coluna4': [(0, WINDOW_WIDTH // 2 * 1.05),
                (100, WINDOW_WIDTH // 2 * 1.05),
                (200, WINDOW_WIDTH // 2 * 1.05),
                (300, WINDOW_WIDTH // 2 * 1.05),
                (400, WINDOW_WIDTH // 2 * 1.05),
                (500, WINDOW_WIDTH // 2 * 1.05)],
     
  
    'coluna5': [(0, WINDOW_WIDTH // 2 * 1.4),
                (100, WINDOW_WIDTH // 2 * 1.4),
                (200, WINDOW_WIDTH // 2 * 1.4),
                (300, WINDOW_WIDTH // 2 * 1.4),
                (400, WINDOW_WIDTH // 2 * 1.4),
                (500, WINDOW_WIDTH // 2 * 1.4)]
}



