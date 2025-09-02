
from classes import *
from pygame import mixer
import os
pygame.init()

class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY = False, False, False, False, False, False
        
        # window set up
        self.DISPLAY_W, self.DISPLAY_H = 800, 800
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        
        # game font
        self.font_name = "8-BIT WONDER.TTF"
        
        # colours
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        
        # menu
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.volume = VolumeMenu(self)
        self.controls = ControlsMenu(self)
        self.credits = CreditsMenu(self)
        self.highscore = HighscoreMenu(self)
        self.curr_menu = self.main_menu
       
        # visual set ups
        pygame.display.set_caption("Galactic Invaders")
        
        self.icon = pygame.image.load(os.path.join('spaceship.png'))
        mixer.music.play(-1)
 
        pygame.display.set_icon(self.icon)
    
    def draw_window(self):
        # load background
        self.BG = pygame.transform.scale(pygame.image.load(os.path.join('background-black1.png')),(self.DISPLAY_W, self.DISPLAY_H)).convert()      
        
        pygame.display.update()

    def game_loop(self):
        while self.playing:
            self.check_events()

            if self.START_KEY:
                self.playing = False
            
            self.draw_window()
            main(self)
            
            pygame.display.update()
            self.reset_keys()
            
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                    self.playing = False  
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.RIGHT_KEY, self.LEFT_KEY = False, False, False, False, False, False

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
