import pygame, os, random
from menu import *
from operator import itemgetter
from pygame import mixer

pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)

DISPLAY_W, DISPLAY_H = 800, 800
display = pygame.Surface((DISPLAY_W, DISPLAY_H))
window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))

shoot_effect = pygame.mixer.Sound('shoot.wav')
explosion_effect = pygame.mixer.Sound('explosion.wav')

font_name = "8-BIT WONDER.TTF"
gameover_font = pygame.font.Font(font_name,30)
smaller_font = pygame.font.Font(font_name,25)
info_font = pygame.font.Font(font_name,15)

BG = pygame.transform.scale(pygame.image.load(os.path.join('background-black1.png')),(DISPLAY_W, DISPLAY_H)).convert()

enemy_img = pygame.image.load(os.path.join("enemy.png"))
enemy_img = pygame.transform.scale(enemy_img, (64,64))

player_bullet_img = pygame.image.load('player_bullet.png')
player_bullet_img = pygame.transform.scale(player_bullet_img, (35,35))

bullet_img = pygame.image.load(os.path.join("bullet.png"))
bullet_img = pygame.transform.scale(bullet_img, (35,35))
fire_img = pygame.image.load(os.path.join("fire.png"))
fire_img = pygame.transform.scale(fire_img, (35,35))

points = 0

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

class Fire:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.fire_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(DISPLAY_H):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        # so player can not spam shoot
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+15, self.y+5, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    def fire_shoot(self):
        if self.cool_down_counter == 0:
            fire = Laser(self.x+15, self.y+5, self.fire_img)
            self.lasers.append(fire)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = pygame.image.load(os.path.join('spaceship.png'))
        self.ship_img = pygame.transform.scale(self.ship_img, (64,64))
        self.laser_img = player_bullet_img
        self.fire_img = fire_img
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.points = 0

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(DISPLAY_H):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.points += 10
                        self.points = self.points
                        shoot_effect.play()
                        if laser in self.lasers:
                            self.lasers.remove(laser)
        
        # special attack
        if points == 100 or points == 300 or points == 500:
            for fire in self.lasers: 
                fire.move(vel)
                if fire.off_screen(DISPLAY_H):
                    self.lasers.remove(fire)
                else:
                    for obj in objs:           
                        if fire.collision(obj):
                            objs.remove(obj)
                            self.points += 50
                            self.points = self.points
                            explosion_effect.play()
                            if fire in self.lasers:
                                self.lasers.remove(fire)

    def draw(self, window):
        global pointss, points
        super().draw(window)
        self.healthbar(window)
        points_label = smaller_font.render(f"Points: {self.points}", 1, WHITE)
        pointss = str(self.points)
        points = self.points
        window.blit(points_label, (310,10))

    def healthbar(self, window):
        # drawing healthbar
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):
    COLOUR_MAP = {
                "bullet": (enemy_img, bullet_img)
                }

    def __init__(self, x, y, colour, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOUR_MAP[colour]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+15, self.y+5, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
def collide(obj1, obj2):
    # collision between two objects
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main(self):
    # game variables
    run = True
    FPS = 50
    level = 0
    lives = 5

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 5

    player = Player(360, 610)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        window.blit(BG, (0,0))
        # draw text
        lives_label = smaller_font.render(f"Lives: {lives}", 1, WHITE)
        level_label = smaller_font.render(f"Level: {level}", 1, WHITE)

        window.blit(lives_label, (10, 10))
        window.blit(level_label, (DISPLAY_H - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(window)

        player.draw(window)

        if lost:
            lost_label = gameover_font.render("GAME OVER", 1, WHITE)
            window.blit(lost_label, (DISPLAY_W/2 - lost_label.get_width()/2, 350))
            info_label = info_font.render("Press S to save you score and play again", 1, WHITE)
            window.blit(info_label, (DISPLAY_W/2 - info_label.get_width()/2, 750))
           
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        # saving scores
                        hs_file = open("highscore.txt","a")
                        hs_file.write(pointss + "\n")
                        
                        hs_file = open("highscore.txt","r")
                        with open("highscore.txt") as f:
                            lines = [line.rstrip() for line in f]

                        output = open("highscore.txt", "w")
                        
                        for line in sorted(lines, key=itemgetter(0), reverse=True):
                            output.write(''.join(line + "\n"))

                        output.close()               
                        hs_file.close()

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
            
        if len(enemies) == 0:
            level += 1
            if lost or lives == 0:
                level == 0
            
            # difficulty increase
            if level == 2:
                enemy_vel += 1
            if level == 3:
                enemy_vel += 1
            if level == 4:
                enemy_vel += 1
            if level == 5:
                enemy_vel += 1
            if level >= 6:
                enemy_vel += 1

            wave_length += 5
            for i in range(wave_length):
                # enemy random position
                enemy = Enemy(random.randrange(50, DISPLAY_W - 100), random.randrange(-1500, -100), "bullet")
                enemies.append(enemy)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.midmenu = True
                    midmenu()
                    main(self)


        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -=  player_vel
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel # LEFT
        
        if keys[pygame.K_RIGHT] and player.x + player_vel +player.get_width() < DISPLAY_W:
            player.x += player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < DISPLAY_W:
            player.x += player_vel # RIGHT
        
        if keys[pygame.K_UP] and player.y - player_vel > 0: 
            player.y -= player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel # UP
        
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < DISPLAY_H: 
            player.y += player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < DISPLAY_H:
            player.y += player_vel # DOWN

        if keys[pygame.K_SPACE]:
            player.shoot()
        
        if points == 100 or points == 300 or points == 500:
            player.fire_shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            
            if random.randrange(0, 2*60) == 1:
                # probability of enemy shooting
                enemy.shoot()

            if collide(enemy, player):
                # player colliding with enemy
                player.health -= 10
                enemies.remove(enemy)
            
            if enemy.y + enemy.get_height() > DISPLAY_H:
                # enemy going past player
                lives -= 1
                enemies.remove(enemy)
        
        player.move_lasers(-laser_vel, enemies)

# mid game menu
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
        pygame.mixer.music.load('BackgroundMusic.mp3')
        mixer.music.set_volume(1.0)
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

def midmenu():
    g = Game()

    while g.running:
        g.playing = True
        
        g.curr_menu.display_menu()
        g.game_loop()


