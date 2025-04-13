from enum import Enum
import pygame
from random import randint
from maths import find_rotated_point
import math
import time
# import movement
from random import randint
class Movement:
    '''a generic class that handles all the movement logic'''
    def __init__(self, x: int, y: int, vector: list[float, float]):
        self.x = x
        self.y = y
        self.vector = vector
    def move(self, player_vector: list[float, float, float]):
        '''actually moving the object'''
        screen = pygame.display.get_surface()
        width = screen.get_width() // 2
        height = screen.get_height() // 2
        self.vector = find_rotated_point(self.vector[0], self.vector[1], player_vector[2])
        self.x, self.y = find_rotated_point(self.x - width, self.y - height, player_vector[2])
        self.x += width
        self.y += height
        self.x += self.vector[0]
        self.y += self.vector[1]
        self.x += player_vector[0]
        self.y += player_vector[1]
        return [self.x, self.y]
class Sprite:
    '''a generic class that handles rendering sprites'''
    def __init__(self, x: int, y: int, image: pygame.Surface):
        self.image = image
        self.rect = image.get_rect(center=(x, y))
    def render(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect.topleft)
        # pygame.draw.rect(screen, (0, 0, 255), self.rect, 1)

class HealthBar:
    '''a generic class that process health for its child classes'''
    def __init__(self, x: int, y: int, max_health=100, health=100):
        self.max_health = max_health
        self.health = health
        self.x = x
        self.y = y
    def draw_health_bar(self):
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, (255, 0, 0), (self.x - 30, self.y - 30, 60, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.x - 30, self.y - 30, (self.health / self.max_health) * 50, 10))