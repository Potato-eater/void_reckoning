from enum import Enum
import pygame
from random import randint
from maths import find_rotated_point
import math
import time
class Star:
    # a star object
    # this is made to store values of each star in the background more easily
    # x and y are the coordinates of the star
    # radius is the radius of the star
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
class Asteroid:
    # an asteroid object
    # this is made to store values of each asteroid in the background more easily
    # x and y are the coordinates of the asteroid
    # vector is the vector of the asteroid, or how fast the asteroid is going
    def __init__(self, x, y, vector=[0,0,0]):
        self.x = x
        self.y = y
        self.vector = vector
class CameraMode(Enum):
    # there are two modes for the camera
    # fixed mode is when the camera has a fixed angle
    # the player would accelerate in the direction of the key press
    # i.e.  w key would accelerate the player up, 
    #       a key would accelerate the player left, etc.
    # rotated mode is when the camera rotates with the player
    # the player would always face towards the top of the screen
    # pressing a and d keys would rotate the player (along with the camera)
    fixed = 0
    rotated = 1
class World:
    # the world object
    # since all the functions are using the same variables and are closely related to each other,
    # I put everything inside of the same class so that they can access each other's variables
    def __init__(self, screen_size: tuple[int, int], render_distance: int):
        '''
        Initializes the world object

        defines all the variables that other methods would use
        '''
        # generate everything
        self.stars = [] # all the stars in the background, would be stored in as an array of Star objects
        self.asteroids = [] # all the asteroids in the background, would be stored in as an array of Asteroid objects
        self.laser_list = [] # all the lasers in the background, would be stored in as an array of pygame.Rect objects
        self.laser_images = [] # since each laser has a different angle, we need to store the image of each laser
        self.laser_vectors = [] # the vector of each laser

        # adding 5 asteroids to the world
        for _i in range(5):
            self.asteroids.append(Asteroid(randint(0, screen_size[0]), randint(0, screen_size[1]), [randint(-2, 2), randint(-2, 2), 0]))
        
        self.screen_size = screen_size # (width, height)
        self.render_distance = render_distance # when to calculate things
        # self.coordinates = [0,0,0] # where the player is at
        self.rotated_angle = 0 # how much the player has rotated, not used if it is currently fixed mode
        self.mode: CameraMode = CameraMode.fixed # what mode the camera is in
        self.vector = [0,2,0] # how the player's coordinates would increase each loop (x, y, r)
        self.face_angle = 0 # the angle the player is facing
        self.max_speed = 150 # how fast the player can go
        self.max_angular_speed = 1.8 # how fast the player can rotate (in radians)
        # defining all the images
        self.base_laser_image = pygame.transform.scale(pygame.image.load("assets/images/laser.png"), (50, 100))
        self.base_asteroid_image = pygame.transform.scale(pygame.image.load("assets/images/asteroid.png"), (80, 80))
        self.base_spaceship_image = pygame.transform.scale(pygame.image.load("assets/images/spaceship.png"), (100, 100))

        # creating a stopwatch, used in the laser_init method
        self.stopwatch = time.time()

        # creating the stars in the background
        for _i in range(800):
            x = randint(-self.render_distance, self.screen_size[0] + self.render_distance) # random x coordinate
            y = randint(-self.render_distance, self.screen_size[1] + self.render_distance) # random y coordinate

             # the star's radius can range from 1 to 3 so that the background is more diverse
             # and looks more interesting
            radius = randint(1, 3)
            self.stars.append(Star(x, y, radius)) # adding each star to the list

    def laser_init(self):
        '''
        initializes a laser bullet

        when this method is called, a laser bullet would be created
        '''
        image = self.base_laser_image
        if self.mode == CameraMode.fixed:
            
            # getting the rotated image and its rect object
            image = pygame.transform.rotate(image, math.degrees(-math.atan2(self.vector[1], self.vector[0])) - 90)
            laser_rect = image.get_rect(center=(
                self.screen_size[0] // 2 - self.vector[0] * 10,
                self.screen_size[1] // 2 - self.vector[1] * 10
            ))

            # adding the rect object to the list
            self.laser_list.append(laser_rect)
            # magnitude = self.vector[0] ** 2 + self.vector[1] ** 2
            x = -self.vector[0] * 2
            y = -self.vector[1] * 2
            r = self.vector[2]
            self.laser_vectors.append([x,y,r])
            self.laser_images.append(image)
        elif self.mode == CameraMode.rotated:
            laser_rect = image.get_rect(center=(
                self.screen_size[0] // 2 - self.vector[0] * 10,
                self.screen_size[1] // 2 - self.vector[1] * 10
            ))
            self.laser_list.append(laser_rect)
            x, y = find_rotated_point(0, math.sqrt(self.vector[0] ** 2 + self.vector[1] ** 2) * -2, -self.vector[2])
            r = 0
            self.laser_vectors.append([x,y,r])
            self.laser_images.append(image)

    def render_player(self):
        '''
        renders the player's spaceship
        '''
        screen = pygame.display.get_surface()
        spaceship_image = self.base_spaceship_image

        # Calculate the rotation angle
        angle = math.degrees(-math.atan2(self.vector[1], self.vector[0])) + 90

        # Rotate the image
        if self.mode == CameraMode.fixed:
            rotated_image = pygame.transform.rotate(spaceship_image, angle)
        else:
            rotated_image = pygame.transform.rotate(spaceship_image, 0)

        # Get the new rect, centered at the intended position
        rotated_rect = rotated_image.get_rect(center=(
            self.screen_size[0] // 2 - self.vector[0] * 5, 
            self.screen_size[1] // 2 - self.vector[1] * 5
        ))

        # Draw the image at the corrected position
        screen.blit(rotated_image, rotated_rect.topleft)

    
    def render_lasers(self):
        '''
        renders the each laser bullet
        '''
        screen = pygame.display.get_surface()
        for i in range(len(self.laser_list)):
            self.laser_images[i] = pygame.transform.rotate(self.base_laser_image, math.degrees(-math.atan2(self.laser_vectors[i][1], self.laser_vectors[i][0])) - 90)
            rotated_rect = self.laser_images[i].get_rect(center=(self.laser_list[i].centerx, self.laser_list[i].centery))
            screen.blit(self.laser_images[i], rotated_rect)
        
    def draw(self):
        '''
        draws everything on the screen
        '''
        screen = pygame.display.get_surface()
        # if self.mode == CameraMode.fixed:
        for star in self.stars:
            pygame.draw.circle(screen, (255, 255, 255), (star.x, star.y), star.radius)
        for asteroid in self.asteroids:
            asteroid_rect = self.base_asteroid_image.get_rect()
            asteroid_rect.centerx = asteroid.x
            asteroid_rect.centery = asteroid.y
            screen.blit(self.base_asteroid_image, (asteroid_rect.left, asteroid_rect.top))
        self.render_lasers()
        self.render_player()
    def check_stars(self):
        '''
        checks if the stars are out of the screen, if they are, regenerate them
        '''
        for star in self.stars:
            if star.x < -self.render_distance:
                star.x = randint(self.screen_size[0], self.screen_size[0] + self.render_distance)
            if star.x > self.screen_size[0] + self.render_distance:
                star.x = randint(-self.render_distance, 0)
            if star.y < -self.render_distance:
                star.y = randint(self.screen_size[1], self.screen_size[1] + self.render_distance)
            if star.y > self.screen_size[1] + self.render_distance:
                star.y = randint(-self.render_distance, 1)
        # print(self.vector[1])
    def handle_input(self):
        '''
        taking input from the player and moving the player accordingly
        '''
        keys = pygame.key.get_pressed()
        current_speed = self.vector[0] ** 2 + self.vector[1] ** 2
        max_speed = self.max_speed
        if self.mode == CameraMode.fixed:
            if keys[pygame.K_w] and current_speed < max_speed: # if w key is pressed, accelerate up
                self.vector[1] += 0.1
            if keys[pygame.K_s] and current_speed < max_speed: # if s key is pressed, accelerate down
                self.vector[1] -= 0.1
            if keys[pygame.K_a] and current_speed < max_speed: # if a key is pressed, accelerate left
                self.vector[0] += 0.1
            if keys[pygame.K_d] and current_speed < max_speed: # if d key is pressed, accelerate right
                self.vector[0] -= 0.1
            if any([keys[pygame.K_w], keys[pygame.K_s]]) == False or current_speed > max_speed: # if w and s key is not pressed, slow down in the y axis
                self.vector[1] *= 0.995
            if any([keys[pygame.K_a], keys[pygame.K_d]]) == False or current_speed > max_speed: # if a and d key is not pressed, slow down in the x axis
                self.vector[0] *= 0.995
            if self.vector[2]:
                self.vector[2] *= 0.95
        elif self.mode == CameraMode.rotated:
            # self.vector[0], self.vector[1] = find_rotated_point(self.vector[0], self.vector[1], -self.vector[2])
            if keys[pygame.K_a] and self.vector[2] < self.max_angular_speed:
                self.vector[2] += 0.01
            if keys[pygame.K_d] and self.vector[2] > -self.max_angular_speed:
                self.vector[2] -= 0.01
            if any([keys[pygame.K_a], keys[pygame.K_d]]) == False:
                self.vector[2] *= 0.95
            
            if keys[pygame.K_w] and current_speed < max_speed:
                self.vector[1] += 0.1
            if keys[pygame.K_s] and current_speed < max_speed:
                self.vector[1] -= 0.1
            if any([keys[pygame.K_w], keys[pygame.K_s]]) == False or current_speed > max_speed: # if w and s key is not pressed, slow down in the y axis
                self.vector[0] *= 0.995
                self.vector[1] *= 0.995
        
        if keys[pygame.K_e] and (time.time() - self.stopwatch) > 0.5:
            
            self.laser_init()
            self.stopwatch = time.time()
        self.vector[0], self.vector[1] = find_rotated_point(self.vector[0], self.vector[1], self.vector[2])
    
    def handle_collision(self):
        '''
        calculates the collision between the player and the asteroids, and the asteroids with each other
        '''
        # player and asteroid
        for asteroid in self.asteroids:
            asteroid_collis_check_rect = pygame.rect.Rect(asteroid.x - 40, asteroid.y - 40, 80, 80)
            player_collis_check_rect = pygame.rect.Rect(self.screen_size[0] // 2 - 25 - self.vector[0] * 5, self.screen_size[1] // 2 - 25 - self.vector[1] * 5, 50, 50)
            if asteroid_collis_check_rect.colliderect(player_collis_check_rect):
                # swap relative velocity
                self.vector[0], asteroid.vector[0] = -asteroid.vector[0], -self.vector[0]
                self.vector[1], asteroid.vector[1] = -asteroid.vector[1], -self.vector[1]
                print("collision")
            if asteroid_collis_check_rect.colliderect(player_collis_check_rect) and asteroid.x > self.screen_size[0] // 2:
                asteroid.x += 1
            if asteroid_collis_check_rect.colliderect(player_collis_check_rect) and asteroid.x < self.screen_size[0] // 2:
                asteroid.x -= 1
            if asteroid_collis_check_rect.colliderect(player_collis_check_rect) and asteroid.y > self.screen_size[1] // 2:
                asteroid.y += 1
            if asteroid_collis_check_rect.colliderect(player_collis_check_rect) and asteroid.y < self.screen_size[1] // 2:
                asteroid.y -= 1
        for i in range(len(self.asteroids)):
            for j in range(i + 1, len(self.asteroids)):
                if i == j:
                    continue
                a1_rect = pygame.rect.Rect(self.asteroids[i].x - 40, self.asteroids[i].y - 40, 80, 80)
                a2_rect = pygame.rect.Rect(self.asteroids[j].x - 40, self.asteroids[j].y - 40, 80, 80)
                if a1_rect.colliderect(a2_rect):
                    self.asteroids[i].vector[0], self.asteroids[j].vector[0] = self.asteroids[j].vector[0], self.asteroids[i].vector[0]
                    self.asteroids[i].vector[1], self.asteroids[j].vector[1] = self.asteroids[j].vector[1], self.asteroids[i].vector[1]
    def process_world(self):
        '''
        processes the world
        updates the coordinates of every object in the game
        '''

        # moving the star
        for star in self.stars:
            star.x, star.y = find_rotated_point(star.x - self.screen_size[0] / 2, star.y - self.screen_size[1] / 2, self.vector[2])
            star.x += self.screen_size[0] / 2
            star.y += self.screen_size[1] / 2
            star.x += self.vector[0]
            star.y += self.vector[1]

        # moving the asteroids
        for asteroid in self.asteroids:
            asteroid.vector[0], asteroid.vector[1] = find_rotated_point(asteroid.vector[0], asteroid.vector[1], self.vector[2])
            asteroid.x, asteroid.y = find_rotated_point(asteroid.x - self.screen_size[0] / 2, asteroid.y - self.screen_size[1] / 2, self.vector[2])
            asteroid.x += self.screen_size[0] / 2
            asteroid.y += self.screen_size[1] / 2
            asteroid.x += self.vector[0]
            asteroid.y += self.vector[1]
            asteroid.x += asteroid.vector[0]
            asteroid.y += asteroid.vector[1]

            # if the asteroid is out of the screen, regenerate it
            if asteroid.x < -self.render_distance:
                asteroid.x = randint(self.screen_size[0], self.screen_size[0] + self.render_distance)
                asteroid.vector[0], asteroid.vector[1] = randint(0, 5), randint(0, 5)
            if asteroid.x > self.screen_size[0] + self.render_distance:
                asteroid.x = randint(-self.render_distance, 0)
                asteroid.vector[0], asteroid.vector[1] = randint(0, 5), randint(0, 5)
            if asteroid.y < -self.render_distance:
                asteroid.y = randint(self.screen_size[1], self.screen_size[1] + self.render_distance)
                asteroid.vector[0], asteroid.vector[1] = randint(0, 5), randint(0, 5)
            if asteroid.y > self.screen_size[1] + self.render_distance:
                asteroid.y = randint(-self.render_distance, 1)
                asteroid.vector[0], asteroid.vector[1] = randint(0, 5), randint(0, 5)

        remove_list = []

        # moving the lasers
        for i in range(len(self.laser_list)):
            self.laser_vectors[i][0], self.laser_vectors[i][1] = find_rotated_point(self.laser_vectors[i][0] , self.laser_vectors[i][1], self.vector[2])
            self.laser_list[i].x, self.laser_list[i].y = find_rotated_point(self.laser_list[i].x - self.screen_size[0] / 2, self.laser_list[i].y - self.screen_size[1] / 2, self.vector[2])
            self.laser_list[i].x += self.screen_size[0] / 2
            self.laser_list[i].y += self.screen_size[1] / 2
            if self.mode == CameraMode.fixed:
                self.laser_images[i] = pygame.transform.rotate(self.base_laser_image, math.degrees(-math.atan2(self.laser_vectors[i][1], self.laser_vectors[i][0])) - 90)
            self.laser_list[i].x += self.laser_vectors[i][0]
            self.laser_list[i].y += self.laser_vectors[i][1]
            self.laser_list[i].x += self.vector[0]
            self.laser_list[i].y += self.vector[1]

            # if the laser hit an asteroid, remove the asteroid and the laser
            for asteroid in self.asteroids:
                if self.laser_list[i].colliderect(pygame.rect.Rect(asteroid.x - 40, asteroid.y - 40, 80, 80)):
                    print("hit")
                    self.asteroids.remove(asteroid)
                    remove_list.append(i)
                    self.asteroids.append(Asteroid(-100, randint(-100, self.screen_size[0] + 100), [randint(0, 5),randint(0, 5),0]))
        
        # calls method to handle collisions between the player and asteroids
        self.handle_collision()

        # removing lasers that need to be removed (because they hit an asteroid)
        # this is done after the loop because removing an element in the middle of the loop would cause an error
        for i in remove_list:
            try:
                self.laser_list.pop(i)
                self.laser_vectors.pop(i)
                self.laser_images.pop(i)
            except IndexError:
                pass
        
        self.face_angle += self.vector[2]
        # print(self.vector[2])
        # print(self.vector)
        # self.coordinates[2] += self.vector[2] 
        # self.handle_input_rotated()

    def debug(self):
        '''
        prints the debug information
        '''
        print(self.vector)
        # print(self.face_angle)
        # print(self.mode)
        # print(self.laser_list)
        # print(self.laser_vectors)
        # # print(self.laser_images)
        # print(self.stars)
        # print(self.asteroids)
