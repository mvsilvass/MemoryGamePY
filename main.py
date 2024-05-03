import pygame
import random
from os.path import join

from settings import * 

class Game():
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode ((WINDOW_WIDTH, WINDOW_HEIGHT)) 
        pygame.display.set_caption("Memory Game by G3") 
        
        #self.icon = import_image('..', 'Memory-Game-by-G3', 'graphics', 'imagens', 'icons', 'icon')
        self.back_carta = import_image('..', 'Memory-Game-by-G3', 'graphics', 'imagens', 'back_carta')
        self.back_carta = pygame.transform.scale(self.back_carta, (128, 128))
        
        #pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        
    def run(self):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
            self.draw_window()
            
    def draw_window(self):
        self.display_surface.fill(BLUE)
        
        coordenadas = [COLUNAS['coluna1'], COLUNAS['coluna2'], COLUNAS['coluna3'], COLUNAS['coluna4'], COLUNAS['coluna5']]

        for coluna in coordenadas:
            for coordenada in coluna:
                self.display_surface.blit(self.back_carta, coordenada)

        pygame.display.update()
        
if __name__== "__main__":
    game = Game()
    game.run()
    