from enum import Enum
import pygame
from random import randint
from maths import find_rotated_point
import math
import time
from weapons import *
# import movement
from constants import *

from parents import *
from enemy import *
# class CameraMode(Enum):
#     # there are two modes for the camera
#     # fixed mode is when the camera has a fixed angle
#     # the player would accelerate in the direction of the key press
#     # i.e.  w key would accelerate the player up, 
#     #       a key would accelerate the player left, etc.
#     # rotated mode is when the camera rotates with the player
#     # the player would always face towards the top of the screen
#     # pressing a and d keys would rotate the player (along with the camera)
#     fixed = 0
#     rotated = 1

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
        


class Explosion(Sprite, Movement):
    def __init__(self, x, y, explosion_sound: pygame.mixer.Sound, scale: float = 1.0,):

        self.base_image = pygame.transform.scale(pygame.image.load("assets/images/explosion.png"), (768, 512))
        if randint(1,2) == 1:
            explosion_sound = pygame.mixer.Sound("assets\sounds\explosion.mp3")
        else:
            explosion_sound = pygame.mixer.Sound("assets\sounds\explosion2.mp3")
        explosion_sound.play()
        frame_width = 256
        frame_height = 256

        # Define frame rects manually
        frame1_rect = pygame.Rect(0, 0, frame_width, frame_height)
        frame2_rect = pygame.Rect(256, 0, frame_width, frame_height)
        frame3_rect = pygame.Rect(512, 0, frame_width, frame_height)
        frame4_rect = pygame.Rect(0, 256, frame_width, frame_height)
        frame5_rect = pygame.Rect(256, 256, frame_width, frame_height)
        frame6_rect = pygame.Rect(512, 256, frame_width, frame_height)

        # Extract and scale each frame
        self.explosion_frame_1 = pygame.transform.scale(self.base_image.subsurface(frame1_rect), (frame_width * scale, frame_height * scale))
        self.explosion_frame_2 = pygame.transform.scale(self.base_image.subsurface(frame2_rect), (frame_width * scale, frame_height * scale))
        self.explosion_frame_3 = pygame.transform.scale(self.base_image.subsurface(frame3_rect), (frame_width * scale, frame_height * scale))
        self.explosion_frame_4 = pygame.transform.scale(self.base_image.subsurface(frame4_rect), (frame_width * scale, frame_height * scale))
        self.explosion_frame_5 = pygame.transform.scale(self.base_image.subsurface(frame5_rect), (frame_width * scale, frame_height * scale))
        self.explosion_frame_6 = pygame.transform.scale(self.base_image.subsurface(frame6_rect), (frame_width * scale, frame_height * scale))

        self.frame_list = [
            self.explosion_frame_1,
            self.explosion_frame_2,
            self.explosion_frame_3,
            self.explosion_frame_4,
            self.explosion_frame_5,
            self.explosion_frame_6
        ]
        self.current_frame = 0
        self.stopwatch = time.time()
        self.start_time = time.time()
        Sprite.__init__(self, x, y, self.frame_list[self.current_frame])
        Movement.__init__(self, x, y, [0, 0, 0])
        
    def update(self, player_vector: list[float], player_angle: float = 0.0):
        self.move(player_vector)
        if self.current_frame >= len(self.frame_list) - 1:
            return True
        self.image = self.frame_list[self.current_frame]
        self.image = pygame.transform.rotate(self.image, -player_angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        if time.time() - self.stopwatch > 0.1:
            self.stopwatch = time.time()
            self.current_frame += 1
            if self.current_frame >= len(self.frame_list):
                return True
            self.image = self.frame_list[self.current_frame]
        # self.current_frame = self.current_frame % len(self.frame_list) - 1
        
        return False

    def check_collision_bumper(self, bumper_list):
        for bumper in bumper_list:
            if self.rect.colliderect(bumper.rect):
                return (True, bumper_list.index(bumper))
        return (False, -1)
    def check_collision_turret(self, turret_list):
        for turret in turret_list:
            if self.rect.colliderect(turret.rect):
                return (True, turret_list.index(turret))
        return (False, -1)

class Among_Us(Sprite, Movement): # this is made as an easter egg but also to test the other classes
    def __init__(self):
        self.base_image = pygame.image.load("assets\images\\amongus.png")
        self.base_image = pygame.transform.scale(self.base_image, (40, 40))
        coordinates = Enemy._random_coordinate(RENDER_DISTANCE)
        self.angular_velocity = randint(-1, 1) / 10
        self.current_angle = 0
        Sprite.__init__(self, coordinates[0], coordinates[1], self.base_image)
        Movement.__init__(self, coordinates[0], coordinates[1], [randint(-300, 300) / 100, randint(-300, 300) / 100])
    def update(self, player_vector):
        self.move(player_vector)
        # self.rect.center = (self.x, self.y)
        self.current_angle += self.angular_velocity
        self.image = pygame.transform.rotate(self.base_image, math.degrees(self.current_angle))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        print(self.x, self.y)
    
class World:
    # the world object
    # since all the functions are using the same variables and are closely related to each other,
    # I put everything inside of the same class so that they can access each other's variables
    def __init__(self, screen_size: tuple[int, int], screen: pygame.surface.Surface):
        '''
        Initializes the world object

        defines all the variables that other methods would use
        '''
        # generate everything
        self.stars = [] # all the stars in the background, would be stored in as an array of Star objects
        self.asteroids = [] # all the asteroids in the background, would be stored in as an array of Asteroid objects

        self.bumpers = [] # all the enemies in the background, would be stored in as an array of Enemy objects

        self.turrets = [] # all the turrets in the background, would be stored in as an array of Turret objects

        self.turret_bullets = [] # all the bullets fired by the turrets, would be stored in as an array of Bullet objects

        self.laser_list = [] # all the lasers in the background, would be stored in as an array of Laser objects

        self.explosions = [] # all the explosions in the background, would be stored in as an array of Explosion objects

        self.amongus = [Among_Us()]
        # self.bombs = []
        for _i in range(INIT_ASTEROID_NUM):
            self.asteroids.append(Asteroid(randint(0, screen_size[0]), randint(0, screen_size[1]), [randint(-2, 2), randint(-2, 2), 0]))
        
        self.screen_size = screen_size # (width, height)
        self.screen = screen
        print(type(self.screen))
        # self.render_distance = render_distance # when to calculate things
        # self.coordinates = [0,0,0] # where the player is at
        self.rotated_angle = 0 # how much the player has rotated, not used if it is currently fixed mode
        self.mode: CameraMode = CameraMode.fixed # what mode the camera is in
        self.explosion_sound = pygame.mixer.Sound("assets\sounds\explosion2.mp3")
        
        self.vector = [0,2,0] # how the player's coordinates would increase each loop (x, y, r)
        self.face_angle_fixed = 0 # the angle the player is facing
        self.face_angle = 0 # the angle the player is facing, used in the rotated mode
        self.max_speed = 24 # how fast the player can go
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


        self.start_time = time.time()
        self.bumper_time = self.start_time
        self.turret_time = self.start_time
        self.asteroids_time = self.start_time
        self.bumper_speed_time = self.start_time
        self.turret_shooting_speed_time = self.start_time
        self.score_time = self.start_time
        self.turret_shooting_speed = INIT_TURRET_SHOOTING_SPEED
        self.bumper_speed = INIT_BUMPER_SPEED

        self.changing_mode = False
        self.transition_facing = 0

        self.player_score = 0
        # self.bomb_stopwatch = time.time()

        # creating the stars in the background
        for _i in range(STAR_NUM):
            x = randint(-RENDER_DISTANCE, SCREEN_WIDTH + RENDER_DISTANCE) # random x coordinate
            y = randint(-RENDER_DISTANCE, SCREEN_HEIGHT + RENDER_DISTANCE) # random y coordinate

             # the star's radius can range from 1 to 3 so that the background is more diverse
             # and looks more interesting
            radius = randint(1, 3)
            self.stars.append(Star(x, y, radius)) # adding each star to the list
        for i in range(INIT_BUMPER_NUM):
            self.bumpers.append(Bumper(RENDER_DISTANCE, INIT_BUMPER_SPEED)) # adding an enemy to the list
        
        for i in range(INIT_TURRET_NUM):
            self.turrets.append(Turret(RENDER_DISTANCE, INIT_TURRET_SHOOTING_SPEED)) # adding a turret to the list
        
    def render_player(self):
        '''
        renders the player's spaceship
        '''
        spaceship_image = self.base_spaceship_image

        # Calculate the rotation angle
        angle = math.degrees(-self.face_angle_fixed) + 90

        # Rotate the image
        if self.mode == CameraMode.rotated and self.changing_mode == False:
            rotated_image = pygame.transform.rotate(spaceship_image, 0)
        elif self.mode == CameraMode.fixed and self.changing_mode == True:
            rotated_image = pygame.transform.rotate(spaceship_image, self.transition_facing)
        else:
            rotated_image = pygame.transform.rotate(spaceship_image, angle)
        
        # Get the new rect, centered at the intended position
        rotated_rect = rotated_image.get_rect(center=(
            SCREEN_WIDTH // 2 - self.vector[0] * 6, 
            SCREEN_HEIGHT // 2 - self.vector[1] * 6
        ))

        # Draw the image at the corrected position
        self.screen.blit(rotated_image, rotated_rect.topleft)

        # draw health bar
        pygame.draw.rect(self.screen, (255, 0, 0), (SCREEN_WIDTH // 2 - 500, SCREEN_HEIGHT - 40, 1000, 25))
        pygame.draw.rect(self.screen, (0, 255, 0), (SCREEN_WIDTH // 2 - 500, SCREEN_HEIGHT - 40, (self.health / self.max_health) * 1000, 25))
        self.font.render("health", True, (255, 255, 255))
        self.screen.blit(self.font.render("HEALTH", True, (0, 0, 0)), (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 40))
    
    def render_lasers(self):
        '''
        renders the each laser bullet
        '''
        
        for laser in self.laser_list:
            # print(laser.vector)
            # laser.image = pygame.transform.rotate(laser.image, math.degrees(-math.atan2(laser.vector[1], laser.vector[0])))
            laser.rect = laser.image.get_rect(center=(
                laser.rect.centerx,
                laser.rect.centery
                # SCREEN_WIDTH // 2 - self.vector[0] * 6,
                # SCREEN_HEIGHT // 2 - self.vector[1] * 6
            ))
            self.screen.blit(laser.image, laser.rect.topleft)
    
    def render_asteroids(self):
        '''
        renders the asteroids
        '''
        
        for asteroid in self.asteroids:
            self.screen.blit(asteroid.image, asteroid.rect.topleft)
    
    def render_bumpers(self):
        '''
        renders the enemies
        '''
        
        for bumper in self.bumpers:
            # pygame.draw.circle(screen, (255, 0, 0), (enemy.x, enemy.y), 20)
            bumper.render(self.screen)
            if bumper.health != 100:
                bumper.draw_health_bar()
    
    def render_turrets(self):
        '''
        renders the turrets
        '''
        
        for turret in self.turrets:
            # pygame.draw.circle(screen, (255, 0, 0), (enemy.x, enemy.y), 20)
            turret.render(self.screen)
            if turret.health != 100:
                turret.draw_health_bar()
    
    def render_explosions(self):
        '''
        renders the explosions
        '''
        
        for explosion in self.explosions:
            explosion.render(self.screen)
    def render_stars(self):
        
        for star in self.stars:
            pygame.draw.circle(self.screen, (255, 255, 255), (star.x, star.y), star.radius)
    
    def render_arrows(self):
        player_xy = [SCREEN_WIDTH // 2 - self.vector[0] * 6, SCREEN_HEIGHT // 2 - self.vector[1] * 6]
        grey_arrow = pygame.image.load("assets\images\\arrow_1.png")
        purple_arrow = pygame.image.load("assets\images\\arrow_2.png")
        green_arrow = pygame.image.load("assets\images\\arrow_3.png")
        for asteroid in self.asteroids:
            dx, dy = asteroid.x - player_xy[0], asteroid.y - player_xy[1]
            angle = math.degrees(math.atan2(dy, dx))
            arrow = pygame.transform.rotate(grey_arrow, -angle - 90)
            arrow_rect = arrow.get_rect()
            arrow_rect.center = player_xy
            self.screen.blit(arrow, arrow_rect)

        for turret in self.turrets:
            dx, dy = turret.x - player_xy[0], turret.y - player_xy[1]
            angle = math.degrees(math.atan2(dy, dx))
            arrow = pygame.transform.rotate(purple_arrow, -angle - 90)
            arrow_rect = arrow.get_rect()
            arrow_rect.center = player_xy
            self.screen.blit(arrow, arrow_rect)
            
        for bumper in self.bumpers:
            dx, dy = bumper.x - player_xy[0], bumper.y - player_xy[1]
            angle = math.degrees(math.atan2(dy, dx))
            arrow = pygame.transform.rotate(green_arrow, -angle - 90)
            arrow_rect = arrow.get_rect()
            arrow_rect.center = player_xy
            self.screen.blit(arrow, arrow_rect)
        
    def draw(self, current_fps):
        '''
        draws everything on the screen
        '''
        
        # if self.mode == CameraMode.fixed:
        # for asteroid in self.asteroids:
        #     asteroid_rect = self.base_asteroid_image.get_rect()
        #     asteroid_rect.centerx = asteroid.x
        #     asteroid_rect.centery = asteroid.y
        #     self.screen.blit(self.base_asteroid_image, (asteroid_rect.left, asteroid_rect.top))

        # for bomb in self.bombs:
        #     # bomb.update()
        #     bomb.draw()
        for sus in self.amongus:
            sus.render(self.screen)
        self.render_stars()
        self.render_asteroids()
        self.render_turrets()
        self.render_bumpers()
        self.render_lasers()
        self.render_explosions()
        self.render_player()
        self.render_arrows()
        self.screen.blit(self.font.render("use wasd to control direction", True, (255, 255, 255)), (10, 10))
        self.screen.blit(self.font.render("press c to change camera mode", True, (255, 255, 255)), (10, 30))
        self.screen.blit(self.font.render("press e to shoot", True, (255, 255, 255)), (10, 50))
        self.screen.blit(self.font.render("press esc to exit", True, (255, 255, 255)), (10, 70))
        self.screen.blit(self.font.render("press space to slow down", True, (255, 255, 255)), (10, 90))
        self.screen.blit(self.font.render(f"current fps: {round(current_fps, 2)}", True, (255, 255, 255)), (10, 110))
        self.screen.blit(self.font.render(f"current game time {round(time.time() - self.start_time, 2)}", True, (255, 255, 255)), (10, 130))
        score = pygame.font.Font(None, 50).render(f"SCORE: {self.player_score}", True, (255, 255, 255))
        score_rect = score.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(score, score_rect)
        # self.screen.blit(self.font.render(f"amount of bumpers: {len(self.bumpers)}", True, (255, 255, 255)), (10, 150))
        # self.screen.blit(self.font.render(f"facing: {self.face_angle}", True, (255, 255, 255)), (10, 170))
        # self.screen.blit(self.font.render(f"face_angle_fixed: {((math.degrees(self.face_angle_fixed) - 90 + 180) % 360) - 180}", True, (255, 255, 255)), (10, 190))
        # self.screen.blit(self.font.render(f"transition facing {self.transition_facing}", True, (255, 255, 255)), (10, 210))
    def check_stars(self):
        '''
        checks if the stars are out of the screen, if they are, regenerate them
        '''
        for star in self.stars:
            if star.x < -RENDER_DISTANCE:
                star.x = randint(SCREEN_WIDTH, SCREEN_WIDTH + RENDER_DISTANCE)
            if star.x > SCREEN_WIDTH + RENDER_DISTANCE:
                star.x = randint(-RENDER_DISTANCE, 0)
            if star.y < -RENDER_DISTANCE:
                star.y = randint(SCREEN_HEIGHT, SCREEN_HEIGHT + RENDER_DISTANCE)
            if star.y > SCREEN_HEIGHT + RENDER_DISTANCE:
                star.y = randint(-RENDER_DISTANCE, 1)
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
            self.vector[2] += 0.02
        if keys[pygame.K_d] and self.vector[2] > -self.max_angular_speed:
            self.vector[2] -= 0.02
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
            self.transition_facing = 0
        self.transition()
    def handle_input(self, keys, c_pressed: bool):
        '''
        taking input from the player and changing the player's vector accordingly
        '''
        # keys = pygame.key.get_pressed()
        # print(c_pressed, keys[pygame.K_c])
        # if pygame.mouse.get_pressed()[2] and time.time() - self.bomb_stopwatch > 1:
        #     self.bombs.append(Bomb(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
        #     self.bomb_stopwatch = time.time()

        if c_pressed == False and keys[pygame.K_c]:
            self.swap_camera_mode()
            self.changing_mode = True
        
        if self.mode == CameraMode.fixed:
            self.handle_player_acceleration_fixed(keys, self.max_speed)
        elif self.mode == CameraMode.rotated:
            self.handle_player_acceleration_rotated(keys, self.max_speed)
        
        if (keys[pygame.K_e] or pygame.mouse.get_pressed()[0])and (time.time() - self.stopwatch) > LASER_COOLDOWN and len(self.laser_list) < 20:
            
            self.laser_list.append(Laser(self.mode, self.face_angle_fixed, self.vector))
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
            player_collis_check_rect = pygame.rect.Rect(SCREEN_WIDTH // 2 - 25 - self.vector[0] * 5, SCREEN_HEIGHT // 2 - 25 - self.vector[1] * 5, 50, 50)
            if asteroid_collis_check_rect.colliderect(player_collis_check_rect):
                # swap relative velocity
                self.vector[0], asteroid.vector[0] = -asteroid.vector[0], -self.vector[0]
                self.vector[1], asteroid.vector[1] = -asteroid.vector[1], -self.vector[1]
                print("collision")
            if asteroid_collis_check_rect.colliderect(player_collis_check_rect) and asteroid.x > SCREEN_WIDTH // 2:
                asteroid.x += 1
            if asteroid_collis_check_rect.colliderect(player_collis_check_rect) and asteroid.x < SCREEN_WIDTH // 2:
                asteroid.x -= 1
            if asteroid_collis_check_rect.colliderect(player_collis_check_rect) and asteroid.y > SCREEN_HEIGHT // 2:
                asteroid.y += 1
            if asteroid_collis_check_rect.colliderect(player_collis_check_rect) and asteroid.y < SCREEN_HEIGHT // 2:
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
    
    def handle_time(self):
        current_time = time.time()
        # print((current_time - self.bumper_time))
        if current_time - self.asteroids_time > ASTEROID_SPAWN_TIME:
            random_xy = Enemy._random_coordinate(RENDER_DISTANCE)
            self.asteroids.append(Asteroid(random_xy[0], random_xy[1], [randint(-2, 2), randint(-2, 2), 0]))
            self.asteroids_time = current_time
        if current_time - self.bumper_time > BUMPER_SPAWN_TIME:
            self.bumpers.append(Bumper(RENDER_DISTANCE, self.bumper_speed))
            self.bumper_time = current_time
        if current_time - self.turret_time > TURRET_SPAWN_TIME:
            self.turrets.append(Turret(RENDER_DISTANCE, self.turret_shooting_speed))
            self.turret_time = current_time
        if current_time - self.bumper_speed_time > BUMPER_SPEED_UPDATE_TIME:
            self.bumper_speed += 1
            self.bumper_speed_time = current_time
        if current_time - self.turret_shooting_speed_time > TURRET_SHOOTING_SPEED_UPDATE_TIME:
            self.turret_shooting_speed -= 0.1
            self.turret_shooting_speed_time = current_time
        if current_time - self.score_time > 3:
            self.player_score += 1
            self.score_time = current_time
    def process_world(self) -> bool:
        '''
        processes the world
        updates the coordinates of every object in the game
        '''
                # pass
        # self.asteroids[0].x = SCREEN_WIDTH // 2 - self.vector[0] * 6
        # self.asteroids[0].y = SCREEN_HEIGHT // 2 - self.vector[1] * 6 - 100
        # self.process_enemy()
        self.face_angle_fixed = math.atan2(self.vector[1], self.vector[0])
        self.handle_time()
        self.transition()
        # moving the star
        for star in self.stars:
            # star.x, star.y = find_rotated_point(star.x - SCREEN_WIDTH / 2, star.y - SCREEN_HEIGHT / 2, self.vector[2])
            # star.x += SCREEN_WIDTH / 2
            # star.y += SCREEN_HEIGHT / 2
            # star.x += self.vector[0]
            # star.y += self.vector[1]
            star.move(self.vector)

        # for bomb in self.bombs:
        #     result = bomb.check_collision(self.asteroids, self.bumpers, self.turrets, self.turret_bullets)
            
        #     if result["asteroid"][0]:
        #         self.explosions.append(Explosion(self.asteroids[result["asteroid"][1]].x, self.asteroids[result["asteroid"][1]].y, 0.5))
        #         self.asteroids.append(Asteroid(self.asteroids[result["asteroid"][1]].x * 10, self.asteroids[result["asteroid"][1]].y * 10, [randint(-2, 2), randint(-2, 2), 0]))
        #         self.asteroids.pop(result["asteroid"][1])
        #     if result["bumper"][0]:
        #         self.explosions.append(Explosion(self.bumpers[result["bumper"][1]].x, self.bumpers[result["bumper"][1]].y, 0.5))
        #         self.bumpers[result["bumper"][1]].health -= 10
        #     if result["turret"][0]:
        #         self.explosions.append(Explosion(self.turrets[result["turret"][1]].x, self.turrets[result["turret"][1]].y, 0.5))
        #         self.turrets[result["turret"][1]].health -= 10
        #     if result["turret_bullet"][0]:
        #         self.explosions.append(Explosion(self.turret_bullets[result["turret_bullet"][1]].x, self.turret_bullets[result["turret_bullet"][1]].y, 0.5))
        #         self.turret_bullets.pop(result["turret_bullet"][1])
            
            # if bomb.update(self.vector):
            #     self.bombs.remove(bomb)
            

        for laser in self.laser_list:
            # laser.move(self.vector)
            laser.update(self.vector)
            hit_asteroid = (laser.check_collision_asteroid(self.asteroids))
            hit_bumper = (laser.check_collision_bumper(self.bumpers))
            hit_turret = (laser.check_collision_turret(self.turrets))
            hit_turret_bullet = (laser.check_collision_turret_bullet(self.turret_bullets))
            if hit_asteroid[0]:
                self.explosions.append(Explosion(self.asteroids[hit_asteroid[1]].x, self.asteroids[hit_asteroid[1]].y, self.explosion_sound, 0.5))
                self.laser_list.remove(laser)
                self.asteroids.append(Asteroid(self.asteroids[hit_asteroid[1]].x * 10, self.asteroids[hit_asteroid[1]].y * 10, [randint(-2, 2), randint(-2, 2), 0]))
                self.asteroids.pop(hit_asteroid[1])
                self.player_score += 5
            
            elif hit_bumper[0]:
                self.laser_list.remove(laser)
                self.bumpers[hit_bumper[1]].health -= 20
            elif hit_turret[0]:
                self.laser_list.remove(laser)
                self.turrets[hit_turret[1]].health -= 20
            elif hit_turret_bullet[0]:
                self.laser_list.remove(laser)
                self.turret_bullets.pop(hit_turret_bullet[1])
                self.player_score += 1
            elif laser.check_out_of_bounds():
                self.laser_list.remove(laser)
            
            
        for bumper in self.bumpers:
            if bumper.health <= 0:
                self.bumpers.remove(bumper)
                self.explosions.append(Explosion(bumper.x, bumper.y, self.explosion_sound))
                self.player_score += 20
                print("enemy dead")
            bumper.update_bumper(self.vector)
            bumper.check_collision_bumper(self.bumpers)
            bumper.check_collision_asteroid(self.asteroids)
            if bumper.check_collision_player(self.vector):
                # return True
                self.health -= 1
        
        for turret in self.turrets:
            shoot = turret.update_turret(self.vector)
            if turret.health <= 0:
                self.turrets.remove(turret)
                self.explosions.append(Explosion(turret.x, turret.y, self.explosion_sound, 2))
                self.player_score += 30
                # self.turrets.append(Turret(RENDER_DISTANCE))
                # print("turret dead")
            if shoot[0]:
                self.turret_bullets.append(TurretBullet(turret.x, turret.y, (shoot[1][0], shoot[1][1]), 5))
            turret.check_collision_asteroid(self.asteroids)
        for bullet in self.turret_bullets:
            bullet.update(self.vector)
            
            bullet.render(self.screen)
            hit_player = bullet.check_collision_player(self.vector)
            if hit_player:
                self.turret_bullets.remove(bullet)
                self.health -= 10
            hit_asteroid = bullet.check_collision_asteroid(self.asteroids)
            if hit_asteroid:
                self.turret_bullets.remove(bullet)
            
            if bullet.x > SCREEN_WIDTH + RENDER_DISTANCE or bullet.x < -RENDER_DISTANCE or bullet.y > SCREEN_HEIGHT + RENDER_DISTANCE or bullet.y < -RENDER_DISTANCE:
                try:
                    self.turret_bullets.remove(bullet)
                except ValueError: # if the bullet is already deleted
                    pass
        # print(turret.x, turret.y)
        # moving the asteroids
        for asteroid in self.asteroids:
            asteroid.update(self.vector, self.face_angle)
            asteroid.check_out_of_bounds(self.screen_size, RENDER_DISTANCE)
        
        for explosion in self.explosions:
            finished = explosion.update(self.vector, self.face_angle)
            hit_bumper = explosion.check_collision_bumper(self.bumpers)
            hit_turret = explosion.check_collision_turret(self.turrets)
            if hit_bumper[0]:
                self.bumpers[hit_bumper[1]].health -= 5
            if hit_turret[0]:
                self.turrets[hit_turret[1]].health -= 5
            if finished:
                self.explosions.remove(explosion)
        
        for sus in self.amongus:
            sus.update(self.vector)
        self.handle_collision()
        

        
        self.face_angle += self.vector[2]

        if self.health <= 0:
            return False
        return True
    def transition(self) -> bool:
        ''''''
        # self.face_angle = math.degrees(self.face_angle_fixed)
        # fixed to rotate
        angle = ((math.degrees(self.face_angle_fixed) + 180 - 90) % 360) - 180
        if abs(angle) < 3 and self.changing_mode == True:
            self.changing_mode = False
            self.vector[2] = 0
        if angle < 0 and self.changing_mode and self.mode == CameraMode.rotated:
            self.vector[2] = 5
        elif angle > 0 and self.changing_mode and self.mode == CameraMode.rotated:
            self.vector[2] = -5
        
        elif self.mode == CameraMode.fixed and self.changing_mode and self.transition_facing < -(((math.degrees(self.face_angle_fixed) - 90 + 180) % 360) - 180):
            self.transition_facing += 5
        elif self.mode == CameraMode.fixed and self.changing_mode and self.transition_facing > -(((math.degrees(self.face_angle_fixed) - 90 + 180) % 360) - 180):
            self.transition_facing -= 5
        if abs(self.transition_facing - self.face_angle) < 1:
            print(True)
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
