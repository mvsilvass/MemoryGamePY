import pygame
import random
import numpy as np # type: ignore
from os.path import join

from settings import * 

class Game():
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode ((WINDOW_WIDTH, WINDOW_HEIGHT)) 
        pygame.display.set_caption("Memory Game by G3") 
        
        self.back_carta = import_image('assets', 'back_carta')
        self.back_carta = pygame.transform.scale(self.back_carta, (CARD_WIDTH, CARD_HEIGHT))
        
        self.front_carta = import_image('assets', 'front_carta')
        self.front_carta = pygame.transform.scale(self.front_carta, (CARD_WIDTH, CARD_HEIGHT))
        self.matching = import_folder('assets', 'matching')
   
        self.clock = pygame.time.Clock()
    
        self.cards = self.init_cards()
        
        self.selected_cards = []
        
        self.match_delay = 500  # 500 milissegundos (0.5 segundo)
        self.waiting = False

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
            
            if self.waiting and pygame.time.get_ticks() >= self.wait_time:
                self.check_matching_cards()
            
    def draw_window(self):
        self.display_surface.fill(GRAY)     

        for coluna in COORDENADAS_IMAGE.values():
            for coordenada in coluna:
                self.display_surface.blit(self.back_carta, coordenada)
                
        for card in self.cards:
            card_rect = pygame.Rect(card['position'], (CARD_WIDTH, CARD_HEIGHT))
            self.display_surface.blit(self.back_carta, card['position'])
            
            if card['revealed']:
                self.display_surface.blit(self.front_carta, card['position'])
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
                    'revealed': False,
                    'matched': False,
                }

                index += 1
                cards.append(card)

        return cards

    def check_matching_cards(self):
        if len(self.selected_cards) == 2:
            card1_index, card2_index = self.selected_cards
            card1 = self.cards[card1_index]
            card2 = self.cards[card2_index]

            # Obtendo as imagens das cartas como arrays de pixels
            image1 = pygame.surfarray.array3d(card1['image'])
            image2 = pygame.surfarray.array3d(card2['image'])

            # Comparando os arrays de pixels
            if np.array_equal(image1, image2):
                card1['matched'] = True
                card2['matched'] = True
            else:
                card1['revealed'] = False
                card2['revealed'] = False

            self.selected_cards.clear()
            self.waiting = False

    def handle_click(self, pos):
        if self.waiting:
            return
        
        for indice, card in enumerate(self.cards):
            if not card['revealed'] and not card['matched']:
                card_rect = pygame.Rect(card['position'], (CARD_WIDTH, CARD_HEIGHT))
                if card_rect.collidepoint(pos) and not card['revealed'] and not card['matched']:
                    card['revealed'] = True
                    self.selected_cards.append(indice) 
                    if len(self.selected_cards) == 2:
                        self.wait_time = pygame.time.get_ticks() + self.match_delay
                        self.waiting = True
                    break
                    
if __name__== "__main__":
    game = Game()
    game.run()
    