import pygame.locals
from parents import *
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
class Laser(Movement):
    '''
    a laser object
    this is made to store values of each laser in the background more easily
    x and y are the coordinates of the laser
    vector is the vector of the laser, or how fast the laser is going
    '''
    def __init__(self, camera_mode: CameraMode, angle: float, player_vector: list[float]):
        '''
        setting up a laser object
        
        shoots in the direction the player is facing
        '''
        try:
            self.base_image = pygame.transform.scale(pygame.image.load("assets/images/laser.png"), (30, 50))
        except FileNotFoundError:
            print("something is wrong with loading the laser image")
        sound = pygame.mixer.Sound("assets/sounds/laser_gun.mp3")
        sound.play()
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
            x, y = find_rotated_point(0.0, 30.0, math.degrees(angle) + 90.0);
            self.vector = [x,y,0]
        elif camera_mode == CameraMode.rotated:
            rect = self.base_image.get_rect(center=(
                screen_size[0] // 2 - player_vector[0] * 6,
                screen_size[1] // 2 - player_vector[1] * 6
            ))
            self.rect = rect
            self.vector = [0, -30.0, 0]
        self.image = image
        super().__init__(rect.left, rect.top, self.vector)

    def update(self, player_vector: list[float]):
        '''updating the laser's location and its image orientation'''
        self.move(player_vector)
        self.rect.x = self.x
        self.rect.y = self.y
        self.image = pygame.transform.rotate(self.base_image, math.degrees(-math.atan2(self.vector[1], self.vector[0])) - 90)
        # print(self.rect.x, self.rect.y)

    def check_collision_asteroid(self, asteroid_list):
        '''check if the laser collides with an asteroid'''
        for asteroid in asteroid_list:
            if self.rect.colliderect(asteroid.rect):
                return (True, asteroid_list.index(asteroid))
        return (False, -1)

    def check_collision_bumper(self, bumper_list):
        '''
        checking if the laser is hitting a bumper.

        decreases the bumper that it hit's health
        '''
        for bumper in bumper_list:
            if self.rect.colliderect(bumper.rect):
                return (True, bumper_list.index(bumper))
        return (False, -1)
    def check_out_of_bounds(self):
        '''checking if the laser is out of bounds'''
        screen = pygame.display.get_surface()
        if abs(self.x) > screen.get_width() or abs(self.y) > screen.get_height():
            return True
    
    def check_collision_turret(self, turret_list):
        '''checking if the laser is hitting a turret'''
        for turret in turret_list:
            if self.rect.colliderect(turret.rect):
                return (True, turret_list.index(turret))
        return (False, -1)

    def check_collision_turret_bullet(self, turret_bullet_list):
        '''checking if the laser is hitting a turret bullet'''
        for turret_bullet in turret_bullet_list:
            if self.rect.colliderect(turret_bullet.rect):
                return (True, turret_bullet_list.index(turret_bullet))
        return (False, -1)

class Bomb(Movement):
    '''
    a very very very power weapon

    can kill everything that goes in its path (including your computer)
    '''
    def __init__(self, x, y):
        super().__init__(x, y, [0,0,0])
        self.radius = 0
        self.step = 0
    def update(self, player_vector) -> bool:
        self.radius = -0.1 * (self.step - 42) ** 2 + 200
        self.step += 0.5
        self.move(player_vector)
        if self.radius < 0:
            return True
        return False
    def draw(self):
        screen = pygame.display.get_surface()
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), int(self.radius), 1)
    def check_collision_asteroid(self, asteroid_list):
        '''check if the laser collides with an asteroid'''
        for asteroid in asteroid_list:
            for i in range(0, 360, 5):
                point_x, point_y = find_rotated_point(1.0, 0.0, i)
                rect = pygame.rect.Rect(self.x + point_x * self.radius, self.y + point_y * self.radius, 1, 1)
                if rect.colliderect(asteroid.rect):
                    return (True, asteroid_list.index(asteroid))
        return (False, -1)
    def check_collision_bumper(self, bumper_list):
        '''check if the laser collides with a bumper'''
        for bumper in bumper_list:
            for i in range(0, 360, 5):
                point_x, point_y = find_rotated_point(1.0, 0.0, i)
                rect = pygame.rect.Rect(self.x + point_x * self.radius, self.y + point_y * self.radius, 1, 1)
                if rect.colliderect(bumper.rect):
                    return (True, bumper_list.index(bumper))
        return (False, -1)
    def check_collision_turret(self, turret_list):
        '''check if the laser collides with a turret'''
        for turret in turret_list:
            for i in range(0, 360, 5):
                point_x, point_y = find_rotated_point(1.0, 0.0, i)
                rect = pygame.rect.Rect(self.x + point_x * self.radius, self.y + point_y * self.radius, 1, 1)
                if rect.colliderect(turret.rect):
                    return (True, turret_list.index(turret))
        return (False, -1)
    def check_collision_turret_bullet(self, turret_bullet_list):
        '''check if the laser collides with a turret bullet'''
        for turret_bullet in turret_bullet_list:
            for i in range(0, 360, 5):
                point_x, point_y = find_rotated_point(1.0, 0.0, i)
                rect = pygame.rect.Rect(self.x + point_x * self.radius, self.y + point_y * self.radius, 1, 1)
                if rect.colliderect(turret_bullet.rect):
                    return (True, turret_bullet_list.index(turret_bullet))
        return (False, -1)
    def check_collision(self, asteroid_list, bumper_list, turret_list, turret_bullet_list) -> dict["asteroid": tuple[bool, int], "bumper": tuple[bool, int], "turret": tuple[bool, int], "turret_bullet": tuple[bool, int]]:
        '''checks which object the bomb collides with'''
        ans = {
            "asteroid": (False, -1),
            "bumper": (False, -1),
            "turret": (False, -1),
            "turret_bullet": (False, -1)
        }
        for i in range(0, 360, 30):
            point_x, point_y = find_rotated_point(1.0, 0.0, i)
            
            for asteroid in asteroid_list:
                if math.sqrt((self.x - asteroid.x) ** 2 + (self.y - asteroid.y) ** 2) < self.radius:
                    ans["asteroid"] = (True, asteroid_list.index(asteroid))
                    return ans
            for bumper in bumper_list:
                if math.sqrt((self.x - bumper.x) ** 2 + (self.y - bumper.y) ** 2) < self.radius:
                    ans["bumper"] = (True, bumper_list.index(bumper))
                    return ans
            for turret in turret_list:
                if math.sqrt((self.x - turret.x) ** 2 + (self.y - turret.y) ** 2) < self.radius:
                    ans["turret"] = (True, turret_list.index(turret))
                    return ans
            for turret_bullet in turret_bullet_list:
                if math.sqrt((self.x - turret_bullet.x) ** 2 + (self.y - turret_bullet.y) ** 2) < self.radius:
                    ans["turret_bullet"] = (True, turret_bullet_list.index(turret_bullet))
            
        return ans