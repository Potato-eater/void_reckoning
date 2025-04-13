import sys
from world import World, CameraMode
import pygame
from pygame.locals import *
from random import randint

# from menu import title_screen
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("assets\sounds\Galactic Rhapsody.mp3")
pygame.mixer.music.play()
beep = pygame.mixer.Sound("assets\sounds\\beep.mp3")
fps = 60
fpsClock = pygame.time.Clock()
from constants import *
# screen = pygame.display.set_mode((800, 300))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# print(width, height)

title_screen = True
title_star_vect = [randint(-500, 500) / 100.0, randint(-500, 500) / 100.0, 0]
end_screen = False
score = 0
game = World((SCREEN_WIDTH, SCREEN_HEIGHT), screen)



# Game loop.
c_pressed = False
run = True

while run:
    screen.fill((0, 0, 0))
    current_fps = fpsClock.get_fps()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    k = pygame.key.get_pressed()
    # if k[K_w] or k[K_a] or k[K_s] or k[K_d] or [K_SPACE]:
    #     title_screen = False


    # Update.
    if title_screen:
        # pygame.draw.rect(screen, (0, 0, 255), (0, 0, width, height))
        title_text = pygame.font.Font(None, 74).render("Void Reckoning", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))
        screen.blit(title_text, title_rect)
        for star in game.stars:
            # star.update()
            star.move(title_star_vect)
        game.check_stars()
        game.render_stars()
        start_rect = pygame.rect.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 200, 300, 30 * 300//77)
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_on_button = start_rect.collidepoint(pygame.mouse.get_pos())
        # start button
        if mouse_on_button:
            start_button = pygame.transform.scale(pygame.image.load("assets\images\start_button_2.png"), (300, 30 * 300//77))
            screen.blit(start_button, start_rect)
        else:
            start_button = pygame.transform.scale(pygame.image.load("assets\images\start_button_1.png"), (300, 30 * 300//77))
            screen.blit(start_button, start_rect)

        if mouse_pressed[0] and mouse_on_button:
            beep.play()
            title_screen = False
            pygame.mixer.music.load("assets\sounds\Time Traveler's Serenade.mp3")
            pygame.mixer.music.play()   
            game = World((SCREEN_WIDTH, SCREEN_HEIGHT), screen)
            # game.start_game()
    elif end_screen:
        with open("assets\\high_score.txt", "r") as file:
            highscore = int(file.readline())
        with open("assets\\high_score.txt", "w") as file:
            if score > highscore:
                highscore = score
            file.write(str(highscore))
                



        title_text = pygame.font.Font(None, 74).render("You died! :(", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))

        score_text = pygame.font.Font(None, 60).render(f"score: {score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))

        highscore_text = pygame.font.Font(None, 60).render(f"highscore: {highscore}", True, (255, 255, 255))
        highscore_rect = highscore_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 140))

        again_text = pygame.font.Font(None, 60).render("press the button to start again", True, (255, 255, 255))
        again_rect = again_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(title_text, title_rect)
        screen.blit(score_text, score_rect)
        screen.blit(highscore_text, highscore_rect)
        screen.blit(again_text, again_rect)



        for star in game.stars:
            # star.update()
            star.move(title_star_vect)
        game.check_stars()
        game.render_stars()
        start_rect = pygame.rect.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 200, 300, 30 * 300//77)
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_on_button = start_rect.collidepoint(pygame.mouse.get_pos())
        # start button
        if mouse_on_button:
            start_button = pygame.transform.scale(pygame.image.load("assets\images\start_button_2.png"), (300, 30 * 300//77))
            screen.blit(start_button, start_rect)
        else:
            start_button = pygame.transform.scale(pygame.image.load("assets\images\start_button_1.png"), (300, 30 * 300//77))
            screen.blit(start_button, start_rect)

        if mouse_pressed[0] and mouse_on_button:
            beep.play()
            end_screen = False
            pygame.mixer.music.load("assets\sounds\Time Traveler's Serenade.mp3")
            pygame.mixer.music.play()   
            game = World((SCREEN_WIDTH, SCREEN_HEIGHT), screen)
    
    else:
        end_screen = not game.process_world()
        if end_screen == True:
            pygame.mixer.music.load("assets\sounds\Stardust Symphony.mp3")
            pygame.mixer.music.play()
            score = game.player_score
        game.handle_input(k, c_pressed)
        # run = game.process_world()
        game.check_stars()
        game.draw(current_fps)
        game.debug()
    # print(space_pressed)
    
    pygame.display.flip()
    fpsClock.tick(fps)
    # print(fpsClock.get_fps())
    if k[K_ESCAPE]:
        run = False
    c_pressed = k[K_c]