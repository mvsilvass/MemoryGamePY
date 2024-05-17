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
        
        self.back_carta = import_image('assets', 'back_carta')
        self.back_carta = pygame.transform.scale(self.back_carta, (CARD_WIDTH, CARD_HEIGHT))
        self.matching = import_folder('assets', 'matching')
   
        self.clock = pygame.time.Clock()
    
        self.cards = self.init_cards()

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
            card_rect = pygame.Rect(card['position'], (CARD_WIDTH, CARD_HEIGHT))
            self.display_surface.blit(self.back_carta, card['position'])
            
            if card['revealed']:
                image_rect = card['image'].get_rect(center=card_rect.center)
                self.display_surface.blit(card['image'], image_rect.topleft)
            else:
                self.display_surface.blit(self.back_carta, card['position'])
                
        pygame.display.update()
        
        
    def init_cards(self):
        lista_imagens = self.matching * 2
        random.shuffle(lista_imagens)
        cards = []

        index = 0
        for coluna in COORDENADAS_IMAGE.values():
            for coordenada in coluna:
                card = {
                    'image': pygame.transform.scale(lista_imagens[index], (IMAGE_WIDTH, IMAGE_HEIGHT)),
                    'position': coordenada,
                    'revealed': True,
                    'matched': False
                }

                index += 1
                cards.append(card)

        return cards

    def check_matching_cards(self):
        pass

        
    def handle_click(self, pos):
        pass
    
if __name__== "__main__":
    game = Game()
    game.run()
    