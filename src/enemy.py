from parents import *
from maths import *
from constants import *
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
    def _random_coordinate(render_distance: int):
        screen = pygame.display.get_surface()
        x, y = randint(-render_distance, SCREEN_WIDTH + render_distance), randint(-render_distance, SCREEN_HEIGHT + render_distance)
        if (x > 0 and x < SCREEN_WIDTH) and (y > 0 and y < SCREEN_HEIGHT):
            return Bumper._random_coordinate(render_distance)
        return x, y
    def update(self, player_vector):
        # self.target_position = [400,200]
        screen = pygame.display.get_surface()
        self.target_position = find_rotated_point(self.target_position[0] - SCREEN_WIDTH // 2, self.target_position[1] - SCREEN_HEIGHT // 2, player_vector[2])
        self.target_position[0] += SCREEN_WIDTH // 2
        self.target_position[1] += SCREEN_HEIGHT // 2
        self.target_position = [self.target_position[0] + player_vector[0], self.target_position[1] + player_vector[1]]
        d_x = self.target_position[0] - self.x
        d_y = self.target_position[1] - self.y
        distance = math.sqrt(d_x ** 2 + d_y ** 2)
        self.vector[0] = (d_x / distance) * self.target_speed
        self.vector[1] = (d_y / distance) * self.target_speed
        
        self.move(player_vector)

class Bumper(Enemy):
    def __init__(self, render_distance, speed):
        self.base_image = pygame.transform.scale(pygame.image.load("assets/images/bumper.png"), (32 * 2.5, 18 * 2.5))
        super().__init__(self.base_image)
        screen = pygame.display.get_surface()
        self.x, self.y = Enemy._random_coordinate(render_distance)
        # self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # screen = pygame.display.get_surface()
        # self.vector = [randint(-50, 50) / 100.0, randint(-50, 50) / 100.0, 0]
        self.target_speed = speed
    def update_bumper(self, player_vector, player_angle: float = 0.0):
        screen = pygame.display.get_surface()
        self.target_position = SCREEN_WIDTH // 2 - player_vector[0] * 6, SCREEN_HEIGHT // 2 - player_vector[1] * 6
        super().update(player_vector)
        self.image = pygame.transform.rotate(self.base_image, -player_angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def check_collision_player(self, player_vector):
        # check if the bumper collides with the player
        screen = pygame.display.get_surface()
        player_rect = pygame.rect.Rect(SCREEN_WIDTH // 2 - 25 - player_vector[0] * 5, SCREEN_HEIGHT // 2 - 25 - player_vector[1] * 5, 50, 50)
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

class Turret(Enemy, HealthBar):
    def __init__(self, render_distance, shooting_speed):
        try:
            self.base_image = pygame.image.load("assets/images/turret.png")
        except FileNotFoundError:
            print("turret image not found")
        frame1_rect = pygame.rect.Rect(0, 0, 34, 62)
        frame2_rect = pygame.rect.Rect(34, 0, 34, 62)
        frame3_rect = pygame.rect.Rect(68, 0, 34, 62)
        frame4_rect = pygame.rect.Rect(102, 0, 34, 62)
        self.frame_1 = pygame.transform.scale(self.base_image.subsurface(frame1_rect), (34 * 2.5, 62 * 2.5))
        self.frame_2 = pygame.transform.scale(self.base_image.subsurface(frame2_rect), (34 * 2.5, 62 * 2.5))
        self.frame_3 = pygame.transform.scale(self.base_image.subsurface(frame3_rect), (34 * 2.5, 62 * 2.5))
        self.frame_4 = pygame.transform.scale(self.base_image.subsurface(frame4_rect), (34 * 2.5, 62 * 2.5))
        self.current_frame = 0
        self.frames = [self.frame_1, self.frame_2, self.frame_3, self.frame_4]
        super().__init__(self.base_image)
        screen = pygame.display.get_surface()
        self.x, self.y = Bumper._random_coordinate(render_distance)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.image = self.frame_1.copy()
        self.stopwatch = time.time()
        self.wait_time = shooting_speed
        self.max_health = 200
        self.health = 200
    def update_turret(self, player_vector) -> tuple[bool, tuple[float, float]]:
        self.move(player_vector)
        self.rect.x = self.x - 25
        self.rect.y = self.y - 25
        self.image = self.frames[self.current_frame]
        screen = pygame.display.get_surface()
        dx = self.x - SCREEN_WIDTH // 2 - player_vector[0] * 6
        dy = self.y - SCREEN_HEIGHT // 2 - player_vector[1] * 6
        angle = -math.degrees(math.atan2(dy, dx)) + 90

        if (time.time() - self.stopwatch > self.wait_time and self.current_frame == 0):
            self.stopwatch = time.time()
            self.current_frame += 1
            self.current_frame %= len(self.frames)
        elif time.time() - self.stopwatch > 0.1 and self.current_frame != 0:
            self.stopwatch = time.time()
            self.current_frame += 1
            self.current_frame %= len(self.frames)
            if self.current_frame == 2:
                return (True, [dx, dy])
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        # pygame.draw.rect(pygame.display.get_surface(), (0, 0, 255), self.rect, 1)
        return (False, [dx, dy])
    def check_collision_asteroid(self, asteroid_list):
        # check if the bumper collides with an asteroid
        for asteroid in asteroid_list:
            if self.rect.colliderect(asteroid.rect):
                self.health -= 0.01 * math.sqrt(asteroid.vector[0] ** 2 + asteroid.vector[1] ** 2)
class TurretBullet(Movement, Sprite):
    def __init__(self, x: int, y: int, vector: list[float, float], speed: float = 10.0):
        Movement.__init__(self, x, y, vector)
        try:
            self.image = pygame.image.load("assets/images/turret_bullet.png")
        except FileNotFoundError:
            print("turret bullet image not found")
        Sprite.__init__(self, x, y, self.image)
        self.x = x - 16
        self.y = y - 16
        self.speed = speed
        # self.image = pygame.transform.scale(pygame.image.load("assets/images/turret_bullet.png"), (32, 32))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        velocity = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        
        self.vector = [-vector[0] / velocity * speed, -vector[1] / velocity * speed, 0]
    def update(self, player_vector):
        self.move(player_vector)
        # pygame.draw.rect(pygame.display.get_surface(), (0, 0, 255), self.rect, 1)
        self.rect.x = self.x
        self.rect.y = self.y
    def check_collision_player(self, player_vector) -> bool:
        screen = pygame.display.get_surface()
        player_rect = pygame.rect.Rect(SCREEN_WIDTH // 2 - 25 - player_vector[0] * 5, SCREEN_HEIGHT // 2 - 25 - player_vector[1] * 5, 50, 50)
        if self.rect.colliderect(player_rect):
            return True
        return False
    def check_collision_asteroid(self, asteroid_list):
        for asteroid in asteroid_list:
            if self.rect.colliderect(asteroid.rect):
                return True

