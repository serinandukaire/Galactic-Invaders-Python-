import pygame
from pygame import mixer

pygame.init()
music = pygame.mixer.music.load('BackgroundMusic.mp3')
mixer.music.set_volume(1.0)

class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.highscorex, self.highscorey = self.mid_w, self.mid_h + 70
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('GALACTIC INVADERS', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 175)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Highscore", 20, self.highscorex, self.highscorey)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.highscorex + self.offset, self.highscorey)
                self.state = 'Highscore'
            elif self.state == 'Highscore':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.highscorex + self.offset, self.highscorey)
                self.state = 'Highscore'
            elif self.state == 'Highscore':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.playing = False
                self.game.curr_menu = self.game.options
            elif self.state == 'Highscore':
                self.game.playing = False
                self.game.curr_menu = self.game.highscore
            elif self.state == 'Credits':
                self.game.playing = False
                self.game.curr_menu = self.game.credits
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Options', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Volume", 15, self.volx, self.voly)
            self.game.draw_text("Controls", 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.UP_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
                
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Volume':
                self.game.playing = False
                self.game.curr_menu = self.game.volume
            elif self.state == 'Controls':
                self.game.playing = False
                self.game.curr_menu = self.game.controls
            self.run_display = False

class VolumeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.options
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Volume', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 40)

            colour = self.game.WHITE
            
            volume = pygame.mixer.music.get_volume()
            if self.game.LEFT_KEY and volume == 1.0:
                colour = (0,0,0)
                print("hi")
                mixer.music.set_volume(0.8)
            if self.game.LEFT_KEY and volume == 0.8:
                colour = (0,0,0)
                print("hi")
                mixer.music.set_volume(0.0)
            
            
            pygame.draw.rect(self.game.display, colour, pygame.Rect(self.game.DISPLAY_W / 2 - 75, self.game.DISPLAY_H / 2, 10, 20))
            pygame.draw.rect(self.game.display, colour, pygame.Rect(self.game.DISPLAY_W / 2 - 60, self.game.DISPLAY_H / 2, 10, 20)) 
            pygame.draw.rect(self.game.display, colour, pygame.Rect(self.game.DISPLAY_W / 2 - 45, self.game.DISPLAY_H / 2, 10, 20))
            pygame.draw.rect(self.game.display, colour, pygame.Rect(self.game.DISPLAY_W / 2 - 30, self.game.DISPLAY_H / 2, 10, 20))
            pygame.draw.rect(self.game.display, colour, pygame.Rect(self.game.DISPLAY_W / 2 - 15, self.game.DISPLAY_H / 2, 10, 20))
            pygame.draw.rect(self.game.display, colour, pygame.Rect(self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2, 10, 20))
            pygame.draw.rect(self.game.display, colour, pygame.Rect(self.game.DISPLAY_W / 2 + 15, self.game.DISPLAY_H / 2, 10, 20))
            pygame.draw.rect(self.game.display, colour, pygame.Rect(self.game.DISPLAY_W / 2 + 30, self.game.DISPLAY_H / 2, 10, 20))
            pygame.draw.rect(self.game.display, colour, pygame.Rect(self.game.DISPLAY_W / 2 + 45, self.game.DISPLAY_H / 2, 10, 20))
            pygame.draw.rect(self.game.display, colour, pygame.Rect(self.game.DISPLAY_W / 2 + 60, self.game.DISPLAY_H / 2, 10, 20))
            
            
                    
            
            self.blit_screen()

class ControlsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.options
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Controls', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 150)
            self.game.draw_text('WASD', 15, self.game.DISPLAY_W / 2 - 120, self.game.DISPLAY_H / 2 - 60)
            self.game.draw_text('or', 15, self.game.DISPLAY_W / 2 - 120, self.game.DISPLAY_H / 2 - 40)
            self.game.draw_text('Arrow Keys              to Move', 15, self.game.DISPLAY_W / 2 - 20, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Space                   to Shoot', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 20)
            self.game.draw_text('Backspace                   to go to menu', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 60)
            self.game.draw_text('Enter                    to click', 15, self.game.DISPLAY_W / 2 - 10, self.game.DISPLAY_H / 2 + 100)
            self.blit_screen()


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Made by Btecoreo', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.blit_screen()


class HighscoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            
            hs_file = open("highscore.txt","r")
            lines = hs_file.readlines()
            score = lines[0]
            score2 = lines[1]
            score3 = lines[2]
            score4 = lines[3]
            score5 = lines[4]
            score6 = lines[5]
            score7 = lines[6]
            score8 = lines[7]
            score9 = lines[8]
            score10 = lines[9]
        
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Highscore', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 175)
            self.game.draw_text('1 ' + ' [ ***** '  + score + ' ***** ] ', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 90)
            self.game.draw_text('2 ' + ' [ ***** ' + score2 + ' ***** ] ', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 70)
            self.game.draw_text('3 ' + ' [ ***** ' + score3 + ' ***** ] ', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 50)
            self.game.draw_text('4 ' + ' [ ***** ' + score4 + ' ***** ] ', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text('5 ' + ' [ ***** ' + score5 + ' ***** ] ', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 10)
            self.game.draw_text('6 ' + ' [ ***** ' + score6 + ' ***** ] ', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.game.draw_text('7 ' + ' [ ***** ' + score7 + ' ***** ] ', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30)
            self.game.draw_text('8 ' + ' [ ***** ' + score8 + ' ***** ] ', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 50)
            self.game.draw_text('9 ' + ' [ ***** ' + score9 + ' ***** ] ', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 70)
            self.game.draw_text('10 ' + ' [ ***** ' + score10 + ' ***** ] ', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 90)
            self.blit_screen()
        
            

                    
            
            
            
            
            
            
            
            
            

        
            
            
                        

            
