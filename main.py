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
        self.folder = import_folder('..', 'Memory-Game-by-G3', 'graphics', 'imagens', 'matching')
        
        #pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        self.new_board = True
        self.board_state = []
        
    def run(self):
        while True:
            self.clock.tick(FPS)
            
            if self.new_board:
                self.board_state = self.generate_board()
                self.new_board = False
                
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
                
        for numero in self.board_state:
            for images in self.folder:
                pass

        pygame.display.update()
        
    def generate_board(self):
        options_list = []
        spaces_list = []
        used_list = []
    
        for item in range(30// 2):
            options_list.append(item)
        
        for item in range(30):
            piece = options_list[random.randint(0, len(options_list)-1)]
            spaces_list.append(piece)
            
            if piece in used_list:
                used_list.remove(piece)
                options_list.remove(piece)
            else:
                used_list.append(piece)
                
if __name__== "__main__":
    game = Game()
    game.run()
    