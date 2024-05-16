import pygame
import random
import time
from os.path import join

from settings import * 

class Game():
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode ((WINDOW_WIDTH, WINDOW_HEIGHT)) 
        pygame.display.set_caption("Memory Game by G3") 
        
        #self.icon = import_image('..', 'Memory-Game-by-G3', 'graphics', 'imagens', 'icons', 'icon')
        self.back_carta = import_image('..', 'Memory-Game-by-G3', 'graphics', 'imagens', 'back_carta')
        self.back_carta = pygame.transform.scale(self.back_carta, (CARD_WIDTH, CARD_HEIGHT))
        self.matching = import_folder_dict('..', 'Memory-Game-by-G3', 'graphics', 'imagens', 'matching')
        
        #pygame.display.set_icon(self.icon)
        self.clock = pygame.time.Clock()
        

        self.cards = self.init_cards()
        self.flipped_cards = []

    def run(self):
        while True:
            self.clock.tick(FPS)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)
                    
            self.draw_window()
            
    def draw_window(self):
        self.display_surface.fill(BLUE)
        

        for coluna in COORDENADAS_IMAGE.values():
            for coordenada in coluna:
                self.display_surface.blit(self.back_carta, coordenada)
                
                
        for card in self.cards:
            if card['revealed']:
                self.display_surface.blit(card['image'], card['position'])
            else:
                self.display_surface.blit(self.back_carta, card['position'])
                
        pygame.display.update()
        
        
    def init_cards(self):
        image_lista = list(self.matching.values())
        random.shuffle(image_lista)
        image_lista_nova = [pygame.transform.scale(image, (IMAGE_WIDTH, IMAGE_HEIGHT)) for image in image_lista]
        image_lista_nova = image_lista * 2
        
        random.shuffle(image_lista_nova)
         
         
        print(image_lista_nova)
        cards = []      
        
        for i, coluna in enumerate(COORDENADAS_IMAGE.values()):
            for j, coordenada in enumerate(coluna):
                card = {
                    'image': pygame.transform.scale(image_lista_nova[i * len(COORDENADAS_IMAGE.values()) + j], (IMAGE_WIDTH, IMAGE_HEIGHT)),
                    'position': coordenada,
                    'revealed': True,
                    'matched': False
                }
                    
                cards.append(card)
                    
        return cards
    
    
    def check_matching_cards(self):
        pass

        
    def handle_click(self, pos):
        pass
    
if __name__== "__main__":
    game = Game()
    game.run()
    