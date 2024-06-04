import pygame
import random
import numpy as np # type: ignore
from os.path import join

from settings import *

from pygame import mixer
from pygame import font

class Game():
    def __init__(self):
        pygame.init()  # Inicia o pygame
        pygame.mixer.init()  # Inicia o mixer do Pygame para áudio
        pygame.font.init()   # Inicia a font do Pygame 
        
        self.display_surface = pygame.display.set_mode ((WINDOW_WIDTH, WINDOW_HEIGHT)) # Cria a janela do jogo
        pygame.display.set_caption("Memory Game by G3") # Define o título da janela
        
        # Carrega e redimensiona a imagem "back_carta"
        self.back_carta = import_image('assets', 'cards','back_carta')
        self.back_carta = pygame.transform.scale(self.back_carta, (CARD_WIDTH, CARD_HEIGHT))
        
        # Carrega e redimensiona a imagem "front_carta"
        self.front_carta = import_image('assets', 'cards', 'front_carta')
        self.front_carta = pygame.transform.scale(self.front_carta, (CARD_WIDTH, CARD_HEIGHT))
        
        # Carrega as imagens da pasta "matching"
        self.matching = import_folder('assets', 'matching')
        
   
        self.clock = pygame.time.Clock() # Relógio para controlar a taxa de quadros
    
        self.cards = self.init_cards()  # Inicializa as cartas do jogo
        
        self.selected_cards = [] # Lista para armazenar as cartas selecionadas
        
        self.match_delay = 500  # Tempo de atraso para verificar o das cartas em milissegundos
        self.waiting = False # Flag para indicar se o jogo está esperando para verificar a correspondência das cartas
        
        # Carrega as imagens da pasta "icons" individualmente
        self.restart_button = import_image('assets', 'icons', 'restart')
        self.logout_button = import_image('assets', 'icons', 'logout')
        
        # Defina as posições dos botões
        self.restart_button_rect = self.restart_button.get_rect(center=(WINDOW_WIDTH // 2 - 60, WINDOW_HEIGHT // 2 + 150))
        self.logout_button_rect = self.logout_button.get_rect(center=(WINDOW_WIDTH // 2 + 60, WINDOW_HEIGHT // 2 + 150))
        
        self.gameover_sound = pygame.mixer.Sound(join('assets', 'sounds', 'gameover.wav'))
        self.gameover_sound.set_volume(0.5)
        self.game_over_timer = None
        self.game_over_sound_played = False  

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
                        
            self.draw_window()  # Desenha a janela do jogo
            
            if self.waiting and pygame.time.get_ticks() >= self.wait_time: # Verifica se é hora de verificar as cartas correspondentes
                self.check_matching_cards()
                
            if all(card['matched'] for card in self.cards):
                self.game_over = True  
                 
    def draw_text(self, text, font_size, color):
        font_path = join('assets', 'fonts', 'BM_Pixel.otf')
        font = pygame.font.Font(font_path, font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)  # Centraliza o texto na tela
        self.display_surface.blit(text_surface, text_rect)

    def draw_window(self):
        self.display_surface.fill(STEELBLUE)   # Preenche o fundo da janela com uma cor definida   

        for coluna in COORDENADAS_IMAGE.values(): # Desenha todas as cartas na posição inicial (viradas para baixo)
            for coordenada in coluna:
                self.display_surface.blit(self.back_carta, coordenada)
                
        for card in self.cards:  # Desenha cada carta com base no seu estado (revelada ou não)
            card_rect = pygame.Rect(card['position'], (CARD_WIDTH, CARD_HEIGHT))
            self.display_surface.blit(self.back_carta, card['position'])
            
            if card['revealed']: # Se a carta estiver revelada, desenha a frente da carta
                self.display_surface.blit(self.front_carta, card['position'])
                image_rect = card['image'].get_rect(center=card_rect.center)
                self.display_surface.blit(card['image'], image_rect.topleft)
            else:  # Se a carta não estiver revelada, desenha o verso da carta
                self.display_surface.blit(self.back_carta, card['position'])
                
                
        if self.game_over:
            self.display_surface.fill(STEELBLUE)
            self.draw_text("V I C T O R Y !", 100, BLACK)

            # Draw buttons
            self.display_surface.blit(self.restart_button, self.restart_button_rect)
            self.display_surface.blit(self.logout_button, self.logout_button_rect)
            
            if all(card['matched'] for card in self.cards):
                if not self.game_over:  # Adicione essa verificação
                    self.game_over = True
                    self.game_over_sound_played = False  # Reinicia a flag

            if self.game_over and not self.game_over_sound_played:  # Adicione essa verificação
                self.gameover_sound.play()
                self.game_over_sound_played = True  # Atualiza a flag
            
        pygame.display.update()  # Atualiza a tela do display
        
    def init_cards(self):
        lista_imagens = self.matching * 2  # Dobra a lista de imagens para criar pares de cartas
        random.shuffle(lista_imagens)      # Embaralha a lista de imagens
        cards = []
    
        index = 0
        for coluna in COORDENADAS_IMAGE.values():  # Distribui as cartas nas posições definidas
            for coordenada in coluna:
                card = {
                    'image': pygame.transform.scale(lista_imagens[index], (IMAGE_WIDTH, IMAGE_HEIGHT)), # Redimensiona a imagem da carta
                    'position': coordenada,
                    'revealed': False,  # Inicialmente, todas as cartas estão viradas para baixo
                    'matched': False,   # Inicialmente, nenhuma carta foi combinada
                }

                index += 1
                cards.append(card)

        return cards # Retorna a lista de cartas inicializadas  

    def check_matching_cards(self):
        if len(self.selected_cards) == 2: # Verifica se duas cartas foram selecionadas
            card1_index, card2_index = self.selected_cards
            card1 = self.cards[card1_index]
            card2 = self.cards[card2_index]

            # Obtém as imagens das cartas como arrays de pixels
            image1 = pygame.surfarray.array3d(card1['image'])
            image2 = pygame.surfarray.array3d(card2['image'])

            # Compara os arrays de pixels para verificar se as cartas são iguais
            if np.array_equal(image1, image2):
                card1['matched'] = True
                card2['matched'] = True
            else:
                card1['revealed'] = False
                card2['revealed'] = False

            self.selected_cards.clear() # Limpa a lista de cartas selecionadas
            self.waiting = False        # Define o estado de espera como falso

    def handle_click(self, pos):
        if self.waiting:    # Se o jogo estiver em estado de espera, não faz nada
            return
        
        for indice, card in enumerate(self.cards):   # Itera sobre as cartas para verificar se uma foi clicada
            
            if not card['revealed'] and not card['matched']: # Verifica se a carta não foi revelada ou combinada
                card_rect = pygame.Rect(card['position'], (CARD_WIDTH, CARD_HEIGHT))
                
                if card_rect.collidepoint(pos) and not card['revealed'] and not card['matched']: # Verifica se a posição do clique está na carta
                    card['revealed'] = True
                    self.selected_cards.append(indice) # Adiciona o índice da carta selecionada à lista
                    
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
    game = Game() # Cria uma instância do jogo
    game.run()    # Inicia o loop principal do jogo
    