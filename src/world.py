from enum import Enum
import pygame
from random import randint
from maths import find_rotated_point
import math
import time
# import movement
from random import randint
class Movement:
    def __init__(self, x: int, y: int, vector: list[float, float]):
        self.x = x
        self.y = y
        self.vector = vector
    def move(self, player_vector: list[float, float, float]):
        
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
    def __init__(self, x: int, y: int, image: pygame.Surface):
        self.image = image
        self.rect = image.get_rect(center=(x, y))
    def render(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect.topleft)
        # pygame.draw.rect(screen, (0, 0, 255), self.rect, 1)

class HealthBar:
    def __init__(self, x: int, y: int, max_health=100, health=100):
        self.max_health = max_health
        self.health = health
        self.x = x
        self.y = y
    def draw_health_bar(self):
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, (255, 0, 0), (self.x - 30, self.y - 30, 60, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.x - 30, self.y - 30, (self.health / self.max_health) * 50, 10))
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

class Star(Movement):
    ''''''
    # a star object
    # this is made to store values of each star in the background more easily
    # x and y are the coordinates of the star
    # radius is the radius of the star

    def __init__(self, x, y, radius):
    #     self.x = x
    #     self.y = y
        super().__init__(x, y, [0,0,0])
        self.radius = radius

class Enemy(Movement, Sprite, HealthBar):
    def __init__(self, image: pygame.Surface):
        # self.x = 0
        # self.y = 0
        # self.vector = [x,y,0]
        Movement.__init__(self, 0, 0, [0,0,0])
        Sprite.__init__(self, self.x, self.y, image)
        HealthBar.__init__(self, self.x, self.y, 100, 100)
        self.target_position = [0,0]
        self.target_speed = 1
    def update(self, player_vector):
        # self.target_position = [400,200]
        screen = pygame.display.get_surface()
        self.target_position = find_rotated_point(self.target_position[0] - screen.get_width() // 2, self.target_position[1] - screen.get_height() // 2, player_vector[2])
        self.target_position[0] += screen.get_width() // 2
        self.target_position[1] += screen.get_height() // 2
        self.target_position = [self.target_position[0] + player_vector[0], self.target_position[1] + player_vector[1]]
        d_x = self.target_position[0] - self.x
        d_y = self.target_position[1] - self.y
        distance = math.sqrt(d_x ** 2 + d_y ** 2)
        self.vector[0] = (d_x / distance) * self.target_speed
        self.vector[1] = (d_y / distance) * self.target_speed
        
        self.move(player_vector)

class Bumper(Enemy):
    def _random_coordinate(render_distance: int):
        screen = pygame.display.get_surface()
        x, y = randint(-render_distance, screen.get_width() + render_distance), randint(-render_distance, screen.get_height() + render_distance)
        if (x > 0 and x < screen.get_width()) and (y > 0 and y < screen.get_height()):
            return Bumper._random_coordinate(render_distance)
        return x, y
    def __init__(self, render_distance):
        self.base_image = pygame.transform.scale(pygame.image.load("assets/images/bumper.png"), (32 * 2.5, 18 * 2.5))
        super().__init__(self.base_image)
        screen = pygame.display.get_surface()
        self.x, self.y = Bumper._random_coordinate(render_distance)
        # self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # screen = pygame.display.get_surface()
        # self.vector = [randint(-50, 50) / 100.0, randint(-50, 50) / 100.0, 0]
        self.target_speed = 1
    def update_bumper(self, player_vector, player_angle: float = 0.0):
        screen = pygame.display.get_surface()
        self.target_position = screen.get_width() // 2 - player_vector[0] * 6, screen.get_height() // 2 - player_vector[1] * 6
        super().update(player_vector)
        self.image = pygame.transform.rotate(self.base_image, -player_angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def check_collision_player(self, player_vector):
        # check if the bumper collides with the player
        screen = pygame.display.get_surface()
        player_rect = pygame.rect.Rect(screen.get_width() // 2 - 25 - player_vector[0] * 5, screen.get_height() // 2 - 25 - player_vector[1] * 5, 50, 50)
        bumper_rect = pygame.rect.Rect(self.x - 25, self.y - 25, 50, 50)
        if bumper_rect.colliderect(player_rect):
            return True
        return False

    def check_collision_bumper(self, bumper_list):
        # check if the bumper collides with another bumper
        for bumper in bumper_list:
            if not self.rect.colliderect(bumper.rect) or self == bumper:
                continue
            # pygame.draw.rect(pygame.display.get_surface(), (0, 0, 255), self.rect)
            if self.rect.y > bumper.rect.y:
                self.rect.y += 1
                self.y += 1
            if self.rect.y < bumper.rect.y:
                self.rect.y -= 1
                self.y -= 1
            if self.rect.x > bumper.rect.x:
                self.rect.x += 1
                self.x += 1
            if self.rect.x < bumper.rect.x:
                self.rect.x -= 1
                self.x -= 1
    def check_collision_asteroid(self, asteroid_list):
        # check if the bumper collides with an asteroid
        for asteroid in asteroid_list:
            while self.rect.colliderect(asteroid.rect):
                if self.rect.y > asteroid.rect.y:
                    self.rect.y += 1
                    self.y += 1
                if self.rect.y < asteroid.rect.y:
                    self.rect.y -= 1
                    self.y -= 1
                if self.rect.x > asteroid.rect.x:
                    self.rect.x += 1
                    self.x += 1
                if self.rect.x < asteroid.rect.x:
                    self.rect.x -= 1
                    self.x -= 1
                self.health -= 0.01 * math.sqrt(asteroid.vector[0] ** 2 + asteroid.vector[1] ** 2)

class Asteroid(Movement):
    '''
    an asteroid object
    this is made to store values of each asteroid in the background more easily
    x and y are the coordinates of the asteroid
    vector is the vector of the asteroid, or how fast the asteroid is going
    '''
    def __init__(self, x: int, y: int, vector: list[float]):
        super().__init__(x, y, vector)
        self.base_image = pygame.transform.scale(pygame.image.load("assets/images/asteroid.png"), (80, 80))
        self.image = self.base_image.copy()
        self.rect = self.base_image.get_rect(center=(x, y))
    def update(self, player_vector: list[float], player_angle: float = 0.0):
        self.move(player_vector)
        self.image = pygame.transform.rotate(self.base_image, -player_angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # pygame.draw.rect(pygame.display.get_surface(), (0, 0, 255), self.rect)
    def check_out_of_bounds(self, screen_size: tuple[int, int], render_distance: int):
        # if the asteroid is out of the screen, regenerate it
        if self.x < -render_distance:
            self.x = randint(screen_size[0], screen_size[0] + render_distance)
            self.vector[0], self.vector[1] = randint(0, 5), randint(0, 5)
        if self.x > screen_size[0] + render_distance:
            self.x = randint(-render_distance, 0)
            self.vector[0], self.vector[1] = randint(0, 5), randint(0, 5)
        if self.y < -render_distance:
            self.y = randint(screen_size[1], screen_size[1] + render_distance)
            self.vector[0], self.vector[1] = randint(0, 5), randint(0, 5)
        if self.y > screen_size[1] + render_distance:
            self.y = randint(-render_distance, 0)
            self.vector[0], self.vector[1] = randint(0, 5), randint(0, 5)
        
class laser(Movement):
    '''
    a laser object
    this is made to store values of each laser in the background more easily
    x and y are the coordinates of the laser
    vector is the vector of the laser, or how fast the laser is going
    '''
    def __init__(self, camera_mode: CameraMode, angle: float, player_vector: list[float]):
        # self.x = x
        # self.y = y
        # self.vector = vector
        self.base_image = pygame.transform.scale(pygame.image.load("assets/images/laser.png"), (30, 50))
        image = self.base_image.copy()
        screen = pygame.display.get_surface()
        screen_size = screen.get_size()
        if camera_mode == CameraMode.fixed:
            image = pygame.transform.rotate(self.base_image, -math.degrees(angle) + 90.0)
            rect = image.get_rect(center=(
                screen_size[0] // 2 - player_vector[0] * 6,
                screen_size[1] // 2 - player_vector[1] * 6
            ))
            self.rect = rect
            x, y = find_rotated_point(0.0, 15.0, math.degrees(angle) + 90.0);
            self.vector = [x,y,0]
        elif camera_mode == CameraMode.rotated:
            rect = self.base_image.get_rect(center=(
                screen_size[0] // 2 - player_vector[0] * 6,
                screen_size[1] // 2 - player_vector[1] * 6
            ))
            self.rect = rect
            self.vector = [0, -15.0, 0]
        self.image = image
        super().__init__(rect.left, rect.top, self.vector)

    def update(self, player_vector: list[float]):

        self.move(player_vector)
        self.rect.x = self.x
        self.rect.y = self.y
        self.image = pygame.transform.rotate(self.base_image, math.degrees(-math.atan2(self.vector[1], self.vector[0])) - 90)
        # print(self.rect.x, self.rect.y)

    def check_collision_asteroid(self, asteroid_list):
        # check if the laser collides with an asteroid
        for asteroid in asteroid_list:
            if self.rect.colliderect(pygame.rect.Rect(asteroid.x - 40, asteroid.y - 40, 80, 80)):
                return (True, asteroid_list.index(asteroid))
        return (False, -1)

    def check_collision_bumper(self, bumper_list):
        # laser_rect = pygame.rect.Rect(self.x - 40, self.y - 40, 80, 80)
        # pygame.draw.rect(pygame.display.get_surface(), (0, 0, 255), self.rect)
        # check if the laser collides with an asteroid
        for bumper in bumper_list:
            if self.rect.colliderect(pygame.rect.Rect(bumper.x - 25, bumper.y - 25, 50, 50)):
                return (True, bumper_list.index(bumper))
        return (False, -1)
    def check_out_of_bounds(self):
        screen = pygame.display.get_surface()
        if abs(self.x) > screen.get_width() or abs(self.y) > screen.get_height():
            return True
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

        self.bumpers = [] # all the enemies in the background, would be stored in as an array of Enemy objects

        self.laser_list = [] # all the lasers in the background, would be stored in as an array of Laser objects

        # adding 5 asteroids to the world
        for _i in range(5):
            self.asteroids.append(Asteroid(randint(0, screen_size[0]), randint(0, screen_size[1]), [randint(-2, 2), randint(-2, 2), 0]))
        
        self.screen_size = screen_size # (width, height)
        self.render_distance = render_distance # when to calculate things
        # self.coordinates = [0,0,0] # where the player is at
        self.rotated_angle = 0 # how much the player has rotated, not used if it is currently fixed mode
        self.mode: CameraMode = CameraMode.fixed # what mode the camera is in
        self.vector = [0,2,0] # how the player's coordinates would increase each loop (x, y, r)
        self.face_angle_fixed = 0 # the angle the player is facing
        self.face_angle = 0 # the angle the player is facing, used in the rotated mode
        self.max_speed = 12 # how fast the player can go
        self.max_angular_speed = 1 # how fast the player can rotate (in radians)
        self.max_health = 500
        self.health = 500
        # defining all the images
        # self.base_laser_image = pygame.transform.scale(pygame.image.load("assets/images/laser.png"), (50, 100))
        # self.base_asteroid_image = pygame.transform.scale(pygame.image.load("assets/images/asteroid.png"), (80, 80))
        self.base_spaceship_image = pygame.transform.scale(pygame.image.load("assets/images/spaceship.png"), (100, 100))
        self.font = pygame.font.SysFont("Arial", 20)
        # creating a stopwatch, used in the laser_init method
        self.stopwatch = time.time()

        # creating the stars in the background
        for _i in range(300):
            x = randint(-self.render_distance, self.screen_size[0] + self.render_distance) # random x coordinate
            y = randint(-self.render_distance, self.screen_size[1] + self.render_distance) # random y coordinate

             # the star's radius can range from 1 to 3 so that the background is more diverse
             # and looks more interesting
            radius = randint(1, 3)
            self.stars.append(Star(x, y, radius)) # adding each star to the list
        for i in range(100):
            self.bumpers.append(Bumper(self.render_distance)) # adding an enemy to the list
        # self.bumpers[0].random_position() # generating a random position for the enemy
    # def laser_init(self):
    #     '''
    #     initializes a laser bullet

    #     when this method is called, a laser bullet would be created
    #     '''
    #     image = self.base_laser_image
    #     if self.mode == CameraMode.fixed:
            
    #         # getting the rotated image and its rect object
    #         image = pygame.transform.rotate(image, math.degrees(-math.atan2(self.vector[1], self.vector[0])) - 90)
    #         laser_rect = image.get_rect(center=(
    #             self.screen_size[0] // 2 - self.vector[0] * 6,
    #             self.screen_size[1] // 2 - self.vector[1] * 6
    #         ))

    #         # adding the rect object to the list
    #         self.laser_list.append(laser_rect)
    #         # magnitude = self.vector[0] ** 2 + self.vector[1] ** 2
    #         x, y = find_rotated_point(0.0, 15.0, math.degrees(self.face_angle_fixed) + 90.0);
    #         r = self.vector[2]
    #         self.laser_vectors.append([x,y,r])
    #         self.laser_images.append(image)
    #     elif self.mode == CameraMode.rotated:
    #         laser_rect = image.get_rect(center=(
    #             self.screen_size[0] // 2 - self.vector[0] * 6,
    #             self.screen_size[1] // 2 - self.vector[1] * 6
    #         ))
    #         self.laser_list.append(laser_rect)
    #         x, y = 0, -15.0;
    #         r = 0
    #         self.laser_vectors.append([x,y,r])
    #         self.laser_images.append(image)
    def render_player(self):
        '''
        renders the player's spaceship
        '''
        screen = pygame.display.get_surface()
        spaceship_image = self.base_spaceship_image

        # Calculate the rotation angle
        angle = math.degrees(-self.face_angle_fixed) + 90

        # Rotate the image
        if self.mode == CameraMode.fixed:
            rotated_image = pygame.transform.rotate(spaceship_image, angle)
        else:
            rotated_image = pygame.transform.rotate(spaceship_image, 0)

        # Get the new rect, centered at the intended position
        rotated_rect = rotated_image.get_rect(center=(
            self.screen_size[0] // 2 - self.vector[0] * 6, 
            self.screen_size[1] // 2 - self.vector[1] * 6
        ))

        # Draw the image at the corrected position
        screen.blit(rotated_image, rotated_rect.topleft)

        # draw health bar
        pygame.draw.rect(screen, (255, 0, 0), (self.screen_size[0] // 2 - 500, self.screen_size[1] - 40, 1000, 25))
        pygame.draw.rect(screen, (0, 255, 0), (self.screen_size[0] // 2 - 500, self.screen_size[1] - 40, (self.health / self.max_health) * 1000, 25))
        self.font.render("health", True, (255, 255, 255))
        screen.blit(self.font.render("HEALTH", True, (0, 0, 0)), (self.screen_size[0] // 2 - 20, self.screen_size[1] - 40))
    
    def render_lasers(self):
        '''
        renders the each laser bullet
        '''
        screen = pygame.display.get_surface()
        for laser in self.laser_list:
            # print(laser.vector)
            # laser.image = pygame.transform.rotate(laser.image, math.degrees(-math.atan2(laser.vector[1], laser.vector[0])))
            laser.rect = laser.image.get_rect(center=(
                laser.rect.centerx,
                laser.rect.centery
                # screen.get_width() // 2 - self.vector[0] * 6,
                # screen.get_height() // 2 - self.vector[1] * 6
            ))
            screen.blit(laser.image, laser.rect.topleft)
    
    def render_asteroids(self):
        '''
        renders the asteroids
        '''
        screen = pygame.display.get_surface()
        for asteroid in self.asteroids:
            screen.blit(asteroid.image, asteroid.rect.topleft)
    
    def render_enemies(self):
        '''
        renders the enemies
        '''
        screen = pygame.display.get_surface()
        for enemy in self.bumpers:
            # pygame.draw.circle(screen, (255, 0, 0), (enemy.x, enemy.y), 20)
            enemy.render(screen)
            if enemy.health != 100:
                enemy.draw_health_bar()
    def draw(self, current_fps):
        '''
        draws everything on the screen
        '''
        screen = pygame.display.get_surface()
        # if self.mode == CameraMode.fixed:
        for star in self.stars:
            pygame.draw.circle(screen, (255, 255, 255), (star.x, star.y), star.radius)
        # for asteroid in self.asteroids:
        #     asteroid_rect = self.base_asteroid_image.get_rect()
        #     asteroid_rect.centerx = asteroid.x
        #     asteroid_rect.centery = asteroid.y
        #     screen.blit(self.base_asteroid_image, (asteroid_rect.left, asteroid_rect.top))
        self.render_asteroids()
        self.render_lasers()
        self.render_enemies()
        self.render_player()
        
        screen.blit(self.font.render("use wasd to control direction", True, (255, 255, 255)), (10, 10))
        screen.blit(self.font.render("press c to change camera mode", True, (255, 255, 255)), (10, 30))
        screen.blit(self.font.render("press e to shoot", True, (255, 255, 255)), (10, 50))
        screen.blit(self.font.render("press esc to exit", True, (255, 255, 255)), (10, 70))
        screen.blit(self.font.render("press space to slow down", True, (255, 255, 255)), (10, 90))
        screen.blit(self.font.render(f"current fps: {round(current_fps, 2)}", True, (255, 255, 255)), (10, 110))
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

    def handle_player_acceleration_fixed(self, keys, max_speed):
        current_speed = math.sqrt(self.vector[0] ** 2 + self.vector[1] ** 2)
        if keys[pygame.K_w] and current_speed < max_speed: # if w key is pressed, accelerate up
            self.vector[1] += 0.1
        if keys[pygame.K_s] and current_speed < max_speed: # if s key is pressed, accelerate down
            self.vector[1] -= 0.1
        if keys[pygame.K_a] and current_speed < max_speed: # if a key is pressed, accelerate left
            self.vector[0] += 0.1
        if keys[pygame.K_d] and current_speed < max_speed: # if d key is pressed, accelerate right
            self.vector[0] -= 0.1
        if any([keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_SPACE]]) == False or current_speed > max_speed: # if w and s key is not pressed, slow down in the y axis
            self.vector[1] *= 0.995
        if any([keys[pygame.K_a], keys[pygame.K_d], keys[pygame.K_SPACE]]) == False or current_speed > max_speed: # if a and d key is not pressed, slow down in the x axis
            self.vector[0] *= 0.995
        if self.vector[2]:
            self.vector[2] *= 0.95
    def handle_player_acceleration_rotated(self, keys, max_speed):
        current_speed = math.sqrt(self.vector[0] ** 2 + self.vector[1] ** 2)
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

    def swap_camera_mode(self):
        if self.mode == CameraMode.fixed:
            self.mode = CameraMode.rotated
        else:
            self.mode = CameraMode.fixed
        self.transition()
    def handle_input(self, keys, c_pressed: bool):
        '''
        taking input from the player and changing the player's vector accordingly
        '''
        # keys = pygame.key.get_pressed()
        # print(c_pressed, keys[pygame.K_c])


        if c_pressed == False and keys[pygame.K_c]:
            self.swap_camera_mode()
        
        if self.mode == CameraMode.fixed:
            self.handle_player_acceleration_fixed(keys, self.max_speed)
        elif self.mode == CameraMode.rotated:
            self.handle_player_acceleration_rotated(keys, self.max_speed)
        
        if (keys[pygame.K_e] or pygame.mouse.get_pressed()[0])and (time.time() - self.stopwatch) > 0.10 and len(self.laser_list) < 20:
            
            self.laser_list.append(laser(self.mode, self.face_angle_fixed, self.vector))
            self.stopwatch = time.time()
        self.vector[0], self.vector[1] = find_rotated_point(self.vector[0], self.vector[1], self.vector[2])
        if keys[pygame.K_SPACE]:
                self.vector[0] *= 0.97
                self.vector[1] *= 0.97
                self.vector[2] *= 0.97
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
    
    # def process_enemy(self):
    #     for enemy in self.bumpers:
    #         enemy.x += enemy.vector[0]
    #         enemy.y += enemy.vector[1]
    def process_world(self) -> bool:
        '''
        processes the world
        updates the coordinates of every object in the game
        '''
        self.asteroids[0].x = self.screen_size[0] // 2 - self.vector[0] * 6
        self.asteroids[0].y = self.screen_size[1] // 2 - self.vector[1] * 6 - 100
        # self.process_enemy()
        self.face_angle_fixed = math.atan2(self.vector[1], self.vector[0])
        # moving the star
        for star in self.stars:
            # star.x, star.y = find_rotated_point(star.x - self.screen_size[0] / 2, star.y - self.screen_size[1] / 2, self.vector[2])
            # star.x += self.screen_size[0] / 2
            # star.y += self.screen_size[1] / 2
            # star.x += self.vector[0]
            # star.y += self.vector[1]
            star.move(self.vector)


        for laser in self.laser_list:
            # laser.move(self.vector)
            laser.update(self.vector)
            hit_asteroid = (laser.check_collision_asteroid(self.asteroids))
            hit_bumper = (laser.check_collision_bumper(self.bumpers))
            if hit_asteroid[0]:
                self.laser_list.remove(laser)
                self.asteroids.append(Asteroid(self.asteroids[hit_asteroid[1]].x * 10, self.asteroids[hit_asteroid[1]].y * 10, [randint(-2, 2), randint(-2, 2), 0]))
                self.asteroids.pop(hit_asteroid[1])

            
            elif hit_bumper[0]:
                self.laser_list.remove(laser)
                self.bumpers[hit_bumper[1]].health -= 10

            elif laser.check_out_of_bounds():
                self.laser_list.remove(laser)
            
            
        for bumper in self.bumpers:
            if bumper.health <= 0:
                self.bumpers.remove(bumper)
                self.bumpers.append(Bumper(self.render_distance))
                print("enemy dead")
            bumper.update_bumper(self.vector)
            bumper.check_collision_bumper(self.bumpers)
            bumper.check_collision_asteroid(self.asteroids)
            if bumper.check_collision_player(self.vector):
                # return True
                self.health -= 0.01
            
        # moving the asteroids
        for asteroid in self.asteroids:
            asteroid.update(self.vector, self.face_angle)
            asteroid.check_out_of_bounds(self.screen_size, self.render_distance)
            # bumper.move(self.vector)
        # calls method to handle collisions between the player and asteroids
        self.handle_collision()
        

        
        self.face_angle += self.vector[2]
        return True
    def transition(self):
        # self.face_angle = math.degrees(self.face_angle_fixed)
        '''thing'''
        pass
        # self.vector[2] = 2
    def debug(self):
        '''
        prints the debug information
        '''
        # print(len(self.laser_list))
        # print(self.face_angle, self.face_angle_fixed)
        # print(self.mode)
        # print(self.laser_list)
        # print(self.laser_vectors)
        # # print(self.laser_images)
        # print(self.stars)
        # print(self.asteroids)
