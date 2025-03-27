import sys
from world import World, CameraMode
import pygame
from pygame.locals import *
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
  
screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h - 200
# screen = pygame.display.set_mode((800, 300))
screen = pygame.display.set_mode((width, height))
game = World((width, height), 800)
# Game loop.
space_pressed = False
while True:
    screen.fill((0, 0, 0))
  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
  
    # Update.
    k = pygame.key.get_pressed()
    game.process_world()
    if k[K_ESCAPE]:
        break
    if k[K_c] and game.mode == CameraMode.fixed and space_pressed == False:
        game.mode = CameraMode.rotated
        space_pressed = True
    elif k[K_c] and game.mode == CameraMode.rotated and space_pressed == False:
        game.mode = CameraMode.fixed
        space_pressed = True
    elif k[K_c] == False:
        space_pressed = False
    
    game.process_world()
    game.handle_input()
    game.check_stars()
    game.draw()
    game.debug()
    # print(space_pressed)
    pygame.display.flip()
    fpsClock.tick(fps)