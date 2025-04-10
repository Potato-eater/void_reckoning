import sys
from world import World, CameraMode
import pygame
from pygame.locals import *
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
  
screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h
# screen = pygame.display.set_mode((800, 300))
screen = pygame.display.set_mode((width, height))
game = World((width, height), 800)
# Game loop.
c_pressed = False
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
    current_fps = fpsClock.get_fps()
    # print(space_pressed)
    game.process_world()
    game.handle_input(k, c_pressed)
    game.check_stars()
    game.draw(current_fps)
    game.debug()
    # print(space_pressed)
    pygame.display.flip()
    fpsClock.tick(fps)
    # print(fpsClock.get_fps())
    c_pressed = k[K_c]