## Glactive Invaders
## Run to play

from game1 import *
g = Game()

while g.running:
    g.playing = True
    
    g.curr_menu.display_menu()
    g.game_loop()
