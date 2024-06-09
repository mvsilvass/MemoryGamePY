import pygame
import random
import numpy as np # type: ignore
from os.path import join

from settings import *

from pygame import mixer
from pygame import font

class Game():
    def __init__(self):
        pygame.init()  
        pygame.mixer.init() 
        pygame.font.init()  
        
        self.display_surface = pygame.display.set_mode ((WINDOW_WIDTH, WINDOW_HEIGHT)) # Cria a janela do jogo
        pygame.display.set_caption("Memory Game by G3")                                # Define o título da janela
        
        # Carrega e redimensiona a imagem "back_card"
        self.back_card = import_image('assets', 'cards','back_card')
        self.back_card = pygame.transform.scale(self.back_card, (CARD_WIDTH, CARD_HEIGHT))
        
        # Carrega e redimensiona a imagem "front_card"
        self.front_card = import_image('assets', 'cards', 'front_card')
        self.front_card = pygame.transform.scale(self.front_card, (CARD_WIDTH, CARD_HEIGHT))
        
        # Carrega as imagens da pasta "matching"
        self.matching = import_folder('assets', 'matching')

        self.clock = pygame.time.Clock() 
        self.cards = self.init_cards()  
        self.selected_cards = [] 
        
        self.match_delay = 500 
        self.waiting = False
        
        # Carrega as imagens dos botões e define suas posições
        self.restart_button = import_image('assets', 'icons', 'restart')
        self.logout_button = import_image('assets', 'icons', 'logout')
        self.restart_button_rect = self.restart_button.get_rect(center=(WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT // 2 + 150))
        self.logout_button_rect = self.logout_button.get_rect(center=(WINDOW_WIDTH // 2 + 60, WINDOW_HEIGHT // 2 + 150))
        
        # Carrega os sons do jogo
        self.gameover_sound = pygame.mixer.Sound(join('assets', 'sounds', 'gameover.wav'))
        self.gameover_sound.set_volume(0.5)
        self.game_over_timer = None
        self.game_over_sound_played = False  
        
        self.select_click_sound = pygame.mixer.Sound(join('assets', 'sounds', 'select_click.wav'))
        self.select_click_sound.set_volume(0.25)
        
        self.correct_sound = pygame.mixer.Sound(join('assets', 'sounds', 'correct.wav'))
        self.correct_sound.set_volume(0.5)
        
        self.game_over = False
        
    def run(self):
        while True:
            self.clock.tick(FPS) # Define a taxa de quadros por segundo
                
            for event in pygame.event.get():  # Verifica se o usuário fechou a janela
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # Verifica se o botão esquerdo do mouse foi pressionado             
                    self.handle_click(event.pos)
                    
                    if self.game_over:
                        if self.restart_button_rect.collidepoint(event.pos):
                            self.restart_game()
                        
                        if self.logout_button_rect.collidepoint(event.pos):
                            pygame.quit()
                            exit()
                        
            self.draw_window() 
            
            if self.waiting and pygame.time.get_ticks() >= self.wait_time: # Verifica se é hora de verificar as cartas correspondentes
                self.check_matching_cards()
                
            if all(card['matched'] for card in self.cards):
                self.game_over = True  
                 
    def draw_text(self, text, font_size, color): 
        font_path = join('assets', 'fonts', 'BM_Pixel.otf')
        font = pygame.font.Font(font_path, font_size)       
        text_surface = font.render(text, True, color)       
        text_rect = text_surface.get_rect()                 
        text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)  
        self.display_surface.blit(text_surface, text_rect)  

    def draw_window(self):
        self.display_surface.fill(STEELBLUE)   

        for column in COORDINATE_IMAGE.values(): # Desenha todas as cartas na posição inicial (viradas para baixo)
            for coordinate in column:
                self.display_surface.blit(self.back_card, coordinate)
                
        for card in self.cards:  # Desenha cada carta com base no seu estado (revelada ou não)
            card_rect = pygame.Rect(card['position'], (CARD_WIDTH, CARD_HEIGHT))
            self.display_surface.blit(self.back_card, card['position'])
            
            if card['revealed']:
                self.display_surface.blit(self.front_card, card['position'])
                image_rect = card['image'].get_rect(center=card_rect.center)
                self.display_surface.blit(card['image'], image_rect.topleft)
            else: 
                self.display_surface.blit(self.back_card, card['position'])
                
        if self.game_over:
            self.display_surface.fill(STEELBLUE) 
            self.draw_text("V I C T O R Y !", 100, BLACK)

            # Draw buttons
            self.display_surface.blit(self.restart_button, self.restart_button_rect)
            self.display_surface.blit(self.logout_button, self.logout_button_rect)
            
            if all(card['matched'] for card in self.cards):
                if not self.game_over:  
                    self.game_over = True
                    self.game_over_sound_played = False  

            if self.game_over and not self.game_over_sound_played:  
                self.gameover_sound.play()
                self.game_over_sound_played = True  
            
        pygame.display.update() 
        
    def init_cards(self):
        list_images = self.matching * 2  # Dobra a lista de imagens para criar pares de cartas
        random.shuffle(list_images)      # Embaralha a lista de imagens
        cards = []
    
        index = 0
        for column in COORDINATE_IMAGE.values():  # Distribui as cartas nas posições definidas
            for coordinate in column:
                card = {
                    'image': pygame.transform.scale(list_images[index], (IMAGE_WIDTH, IMAGE_HEIGHT)),
                    'position': coordinate,
                    'revealed': False, 
                    'matched': False, 
                }

                index += 1
                cards.append(card)

        return cards # Retorna a lista de cartas inicializadas  

    def check_matching_cards(self):
        if len(self.selected_cards) == 2: 
            
            card1_index, card2_index = self.selected_cards
            
            card1 = self.cards[card1_index]
            card2 = self.cards[card2_index]

            # Converte as imagens das cartas para arrays 3D de pixels
            image1 = pygame.surfarray.array3d(card1['image'])
            image2 = pygame.surfarray.array3d(card2['image'])

            # Compara os arrays de pixels para verificar se as cartas são iguais
            if np.array_equal(image1, image2):
                # Se as cartas forem iguais, marca ambas como 'matched' (combinadas)
                card1['matched'] = True
                card2['matched'] = True
                self.correct_sound.play()
            else:
                # Se as cartas não forem iguais, vira ambas de volta
                card1['revealed'] = False
                card2['revealed'] = False

            self.selected_cards.clear()
            self.waiting = False        

    def handle_click(self, pos):
        if self.waiting:    # Se o jogo estiver em estado de espera, não faz nada
            return
        
        for index, card in enumerate(self.cards):   # Itera sobre as cartas para verificar se uma foi clicada
            
            if not card['revealed'] and not card['matched']:
                card_rect = pygame.Rect(card['position'], (CARD_WIDTH, CARD_HEIGHT))
                
                if card_rect.collidepoint(pos) and not card['revealed'] and not card['matched']: # Verifica se a posição do clique está na carta
                    card['revealed'] = True
                    self.selected_cards.append(index) # Adiciona o índice da carta selecionada à lista
                    
                    self.select_click_sound.play() # Reproduz o som de clique
                    
                    if len(self.selected_cards) == 2:  # Se duas cartas forem selecionadas, inicia o timer para verificar a correspondência
                        self.wait_time = pygame.time.get_ticks() + self.match_delay
                        self.waiting = True
                    break          
                    
    def restart_game(self):
        self.cards = self.init_cards()
        self.selected_cards = []
        self.game_over = False
        self.game_over_sound_played = False
        
if __name__== "__main__":
    game = Game() 
    game.run()    
    