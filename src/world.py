from enum import Enum
import pygame
from random import randint
from maths import find_rotated_point
from math import sqrt
class Star:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

class CameraMode(Enum):
    fixed = 0
    fixed_rotate = 1
    rotated = 2
class World:
    def __init__(self, screen_size: tuple[int, int], render_distance: int):
        # generate everything
        self.stars = []
        self.screen_size = screen_size # (width, height)
        self.render_distance = render_distance # when to calculate things
        # self.coordinates = [0,0,0] # where the player is at
        self.rotated_angle = 0 # how much the player has rotated, not used if it is currently fixed mode
        self.mode: CameraMode = CameraMode.fixed # the camera. the available modes are fixed: camera always faces the same way and keyboard input's direction
        # directly corresponds to where the rocket would go
        self.vector = [0,0,0] # how the player's coordinates would increase each loop (x, y, r)
        self.max_speed = 150 # how fast the player can go
        # self.max_angular = 1
        for i in range(800):
            x = randint(-self.render_distance, self.screen_size[0] + self.render_distance)
            y = randint(-self.render_distance, self.screen_size[1] + self.render_distance)
            radius = randint(1, 3)
            self.stars.append(Star(x, y, radius))

    def draw(self):
        screen = pygame.display.get_surface()
        # if self.mode == CameraMode.fixed:
        for star in self.stars:
            pygame.draw.circle(screen, (255, 255, 255), (star.x, star.y), star.radius)
        pygame.draw.rect(screen, (255, 0, 0), (self.screen_size[0] // 2 - 25 - self.vector[0] * 5, self.screen_size[1] // 2 - 25 - self.vector[1] * 5, 50, 50))

    def check_stars(self):
        for star in self.stars:
            if star.x < -self.render_distance:
                star.x = randint(self.screen_size[0], self.screen_size[0] + self.render_distance)
            if star.x > self.screen_size[0] + self.render_distance:
                star.x = randint(-self.render_distance, 0)
            if star.y < -self.render_distance:
                star.y = randint(self.screen_size[1], self.screen_size[1] + self.render_distance)
            if star.y > self.screen_size[1] + self.render_distance:
                star.y = randint(-self.render_distance, 1)

    # def handle_input_fixed(self):
    #     keys = pygame.key.get_pressed()

    #     if keys[pygame.K_w] and self.vector[1] > -self.max_speed: # if w key is pressed, accelerate up
    #         self.vector[1] += 0.2
    #     if keys[pygame.K_s] and self.vector[1] < self.max_speed: # if s key is pressed, accelerate down
    #         self.vector[1] -= 0.2
    #     if keys[pygame.K_a] and self.vector[0] > -self.max_speed: # if a key is pressed, accelerate left
    #         self.vector[0] += 0.2
    #     if keys[pygame.K_d] and self.vector[0] < self.max_speed: # if d key is pressed, accelerate right
    #         self.vector[0] -= 0.2
    #     if any([keys[pygame.K_w], keys[pygame.K_s]]) == False: # if w and s key is not pressed, slow down in the y axis
    #         self.vector[1] *= 0.99
    #     if any([keys[pygame.K_a], keys[pygame.K_d]]) == False: # if a and d key is not pressed, slow down in the x axis
    #         self.vector[0] *= 0.99

    # def handle_input_rotated(self):
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_a]:
    #         self.vector[2] += 0.01
    #     if keys[pygame.K_d]:
    #         self.vector[2] -= 0.01
    #     if any([keys[pygame.K_a], keys[pygame.K_d]]) == False:
    #         self.vector[2] *= 0.95
        
    #     if keys[pygame.K_w]:
    #         self.vector[1] += 0.1
    #     if keys[pygame.K_s]:
    #         self.vector[1] -= 0.1
    #     if any([keys[pygame.K_w], keys[pygame.K_s]]) == False: # if w and s key is not pressed, slow down in the y axis
    #         self.vector[0] *= 0.99
    #         self.vector[1] *= 0.99
    #     self.vector[0], self.vector[1] = find_rotated_point(self.vector[0], self.vector[1], self.vector[2])
        
        # print(self.vector[1])
    def handle_input(self):
        keys = pygame.key.get_pressed()
        current_speed = self.vector[0] ** 2 + self.vector[1] ** 2
        max_speed = self.max_speed
        if self.mode == CameraMode.fixed:
            if keys[pygame.K_w] and current_speed < max_speed: # if w key is pressed, accelerate up
                self.vector[1] += 0.2
            if keys[pygame.K_s] and current_speed < max_speed: # if s key is pressed, accelerate down
                self.vector[1] -= 0.2
            if keys[pygame.K_a] and current_speed < max_speed: # if a key is pressed, accelerate left
                self.vector[0] += 0.2
            if keys[pygame.K_d] and current_speed < max_speed: # if d key is pressed, accelerate right
                self.vector[0] -= 0.2
            if any([keys[pygame.K_w], keys[pygame.K_s]]) == False or current_speed > max_speed: # if w and s key is not pressed, slow down in the y axis
                self.vector[1] *= 0.99
            if any([keys[pygame.K_a], keys[pygame.K_d]]) == False or current_speed > max_speed: # if a and d key is not pressed, slow down in the x axis
                self.vector[0] *= 0.99
            if self.vector[2]:
                self.vector[2] *= 0.95
        elif self.mode == CameraMode.rotated:
            # self.vector[0], self.vector[1] = find_rotated_point(self.vector[0], self.vector[1], -self.vector[2])
            if keys[pygame.K_a]:
                self.vector[2] += 0.01
            if keys[pygame.K_d]:
                self.vector[2] -= 0.01
            if any([keys[pygame.K_a], keys[pygame.K_d]]) == False:
                self.vector[2] *= 0.95
            
            if keys[pygame.K_w] and current_speed < max_speed:
                self.vector[1] += 0.2
            if keys[pygame.K_s] and current_speed < max_speed:
                self.vector[1] -= 0.2
            if any([keys[pygame.K_w], keys[pygame.K_s]]) == False or current_speed > max_speed: # if w and s key is not pressed, slow down in the y axis
                self.vector[0] *= 0.99
                self.vector[1] *= 0.99
        self.vector[0], self.vector[1] = find_rotated_point(self.vector[0], self.vector[1], self.vector[2])
    def process_world(self):
        for star in self.stars:
            star.x, star.y = find_rotated_point(star.x - self.screen_size[0] / 2, star.y - self.screen_size[1] / 2, self.vector[2])
            star.x += self.screen_size[0] / 2
            star.y += self.screen_size[1] / 2
            star.x += self.vector[0]
            star.y += self.vector[1]
        print(self.vector)
        # self.coordinates[2] += self.vector[2] 
        # self.handle_input_rotated()
        self.handle_input()
        self.check_stars()
        self.draw()

            

