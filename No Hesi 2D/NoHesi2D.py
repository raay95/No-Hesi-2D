import random
import pygame
from pygame.locals import *


WIDTH, HEIGHT = 400, 800
SPACES = 220
BOT_COUNT = 12


# player's car
class Car():
    def __init__(self, surface):
        self.surface = surface

        self.player_car = pygame.image.load("resources/cars/playercar.png").convert_alpha() # player vehicle
        self.car_x = 175
        self.car_y = 800 # starts at 800 ends up at 600
        self.speed = 4
        self.hitbox = [183, 609, 220, 701]
        self.left_pressed = False
        self.right_pressed = False

        self.surface.blit(self.player_car, (self.car_x, self.car_y))

    def update(self, updates):
        if updates <= 200:
            self.car_y -= 1

        self.velX = 0
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed

        self.car_x += self.velX
        if self.car_x < 64:
            self.car_x = 64
        elif self.car_x > 281:
            self.car_x = 281
        self.hitbox[0] = self.car_x + 3
        self.hitbox[2] = self.car_x + 52
        self.surface.blit(self.player_car, (self.car_x, self.car_y))

# Bots' cars
class Bot():
    def __init__(self, surface):
        self.surface = surface
        self.bot_xcoords_list = []
        self.bot_ycoords_list = []
        self.models_list = []
        self.bot_hitbox = [10, 8, 45, 108]

        self.gray_car = pygame.image.load("resources/cars/graycar.png").convert_alpha() # bot vehicle
        self.blue_car = pygame.image.load("resources/cars/bluecar.png").convert_alpha()
        self.red_car = pygame.image.load("resources/cars/redcar.png").convert_alpha()
        self.bot_models = [self.gray_car, self.blue_car, self.red_car]
        for i in range(BOT_COUNT):
            self.bot_xcoords_list.append(0)
            self.bot_ycoords_list.append(-i * SPACES - 600)
            self.models_list.append(random.choice(self.bot_models))

    def bot_generating(self, bot_number):
        self.x_coords = [80, 174, 265]
        self.x = random.choice(self.x_coords)
        if bot_number > 0:
            while self.x == self.bot_xcoords_list[bot_number - 1]:
                self.x = random.choice(self.x_coords)
        elif bot_number > 1:
            if self.x > self.bot_xcoords_list[bot_number - 1] and self.bot_xcoords_list[bot_number - 1] > self.bot_xcoords_list[bot_number - 2]:
                self.x = random.choice(self.x_coords)
            elif self.x < self.bot_xcoords_list[bot_number - 1] and self.bot_xcoords_list[bot_number - 1] < self.bot_xcoords_list[bot_number - 2]:
                self.x = random.choice(self.x_coords)
        self.bot_xcoords_list[bot_number] = self.x
        self.surface.blit(self.models_list[bot_number], (self.bot_xcoords_list[bot_number], self.bot_ycoords_list[bot_number]))

    def update(self):
        speed = 4
        self.velY = 0
        self.velY += speed
        for i in range(0, len(self.bot_ycoords_list)):
            self.bot_ycoords_list[i] += self.velY
            if self.bot_ycoords_list[i] >= 780:
                self.bot_xcoords_list[i] = random.choice(self.x_coords)
                self.bot_ycoords_list[i] -= SPACES * BOT_COUNT
                self.models_list[i] = random.choice(self.bot_models)
            self.surface.blit(self.models_list[i], (self.bot_xcoords_list[i], self.bot_ycoords_list[i]))


class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('No Hesi 2D')

        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.mixer.init()
        programIcon = pygame.image.load('icon.png').convert_alpha()
        pygame.display.set_icon(programIcon)
        self.surface.fill((0, 122, 5))
        self.road_x = 0
        self.road0_y = 800
        self.road1_y = 0
        self.road2_y = -800
        self.road_speed = 8
        self.score = 0
        self.last_point = 0

        self.personal_best = 0
        file_pb_read = open('score_record.json', 'r')
        read = int(file_pb_read.readline())
        if self.personal_best < read:
            self.personal_best = read
        file_pb_read.close()

        self.amount_of_updates = 0

        self.clock = pygame.time.Clock()

        self.road = pygame.image.load("resources/road.png").convert()
        self.head = pygame.image.load("resources/head.png").convert()
        self.right_arrow = pygame.image.load("resources/right_arrow.png").convert_alpha()
        self.left_arrow = pygame.image.load("resources/left_arrow.png").convert_alpha()
        self.d_letter = pygame.image.load("resources/d_letter.png").convert_alpha()
        self.a_letter = pygame.image.load("resources/a_letter.png").convert_alpha()
        self.game_over_screen = pygame.image.load("resources/game_over.png").convert()
        self.surface.blit(self.road, (self.road_x, self.road1_y))
        self.surface.blit(self.road, (self.road_x, self.road2_y))
        self.surface.blit(self.head, (0, 0))
        self.background_music()

        self.car = Car(self.surface)
        self.bot = Bot(self.surface)

        for i in range(BOT_COUNT):
            self.bot.bot_generating(i)

    def move(self, direction, down):
        if direction == 'right':
            self.car.right_pressed = down
        elif direction == 'left':
            self.car.left_pressed = down

    def road_move(self, speed):
        self.road0_y += speed
        self.road1_y += speed
        self.road2_y += speed

        if self.road0_y == 800:
            self.road0_y -= 1600
        elif self.road1_y == 800:
            self.road1_y -= 1600
        elif self.road2_y == 800:
            self.road2_y -= 1600

    def collision(self, bot_number):
        if self.car.hitbox[1] <= (self.bot.bot_hitbox[1] + self.bot.bot_ycoords_list[bot_number]) <= self.car.hitbox[3] or self.car.hitbox[1] <= (self.bot.bot_hitbox[3] + self.bot.bot_ycoords_list[bot_number]) <= self.car.hitbox[3]:
            if self.car.hitbox[0] <= (self.bot.bot_hitbox[0] + self.bot.bot_xcoords_list[bot_number]) <= self.car.hitbox[2] or self.car.hitbox[0] <= (self.bot.bot_hitbox[2] + self.bot.bot_xcoords_list[bot_number]) <= self.car.hitbox[2]:
                raise "collision occured"
            
    def bot_passed(self, bot_number):
        if self.last_point != bot_number and self.car.hitbox[1] <= (self.bot.bot_hitbox[1] + self.bot.bot_ycoords_list[bot_number]) <= self.car.hitbox[3]:
            self.score += 1
            self.last_point = bot_number

    def head_update(self):
        score_font = pygame.font.SysFont('arial', 44)
        score_text = score_font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_text_rect = score_text.get_rect(center=(WIDTH/2, 25))

        pb_font = pygame.font.SysFont('arial', 24)
        pb_text = pb_font.render(f"Your best: {self.personal_best}", True, (255, 255, 255))
        pb_text_rect = pb_text.get_rect(center=(WIDTH/2, 60))
        
        self.surface.blit(self.head, (0, 0))
        self.surface.blit(score_text, score_text_rect)
        self.surface.blit(pb_text, pb_text_rect)

        # Controls hint
        controls_font = pygame.font.SysFont('arial', 16)
        left_controls = controls_font.render("To move left:", True, (255, 255, 255))
        right_controls_txt = controls_font.render("To move right:", True, (255, 255, 255))

        if self.amount_of_updates < 500:
            self.surface.blit(left_controls, (8, 15))
            self.surface.blit(right_controls_txt, (315, 15))
            self.surface.blit(self.a_letter, (47, 40))
            self.surface.blit(self.left_arrow, (12, 40))
            self.surface.blit(self.d_letter, (322, 40))
            self.surface.blit(self.right_arrow, (358, 40))

        self.amount_of_updates += 1

    def background_music(self):
        pygame.mixer.music.load("resources/background.mp3")
        pygame.mixer.music.play(loops=-1)

    def update(self):
        self.surface.fill((0, 122, 5))
        self.surface.blit(self.road, (self.road_x, self.road1_y))
        self.surface.blit(self.road, (self.road_x, self.road2_y))
        self.bot.update()
        self.car.update(self.amount_of_updates)
        self.head_update()
        for i in range(BOT_COUNT):
            self.collision(i)
            self.bot_passed(i)

        pygame.display.flip()

    def game_over(self):
        pygame.mixer.music.stop()

        head_font = pygame.font.SysFont('arial', 48)
        head_text = head_font.render("You crashed!", True, (255, 255, 255))
        head_rect = head_text.get_rect(center=(WIDTH/2, 240))

        line2_font = pygame.font.SysFont('arial', 28)
        line2_text = line2_font.render(f'Your score is {self.score}', True, (255, 255, 255))
        line2_rect = line2_text.get_rect(center=(WIDTH/2, 280))

        line3_font = pygame.font.SysFont('arial', 28)
        line3_text = line3_font.render(f'Your personal best is {self.personal_best}', True, (255, 255, 255))
        line3_rect = line3_text.get_rect(center=(WIDTH/2, 310))

        again_font = pygame.font.SysFont('arial', 22)
        again_text = again_font.render(f'To play again press SPACE or ESCAPE to exit', True, (255, 255, 255))
        again_rect = again_text.get_rect(center=(WIDTH/2, 370))

        self.surface.blit(self.game_over_screen, (0, 200))
        self.surface.blit(head_text, head_rect)
        self.surface.blit(line2_text, line2_rect)
        self.surface.blit(line3_text, line3_rect)
        self.surface.blit(again_text, again_rect)

        pygame.display.flip()

    def new_record(self):
        if self.personal_best < self.score:
            self.personal_best = self.score
            file_pb_write = open('score_record.json', 'w')
            file_pb_write.write (str(self.personal_best))
            file_pb_write.close()

    def reset(self):
        self.__init__()
        self.car.__init__(self.surface)
        self.bot.__init__(self.surface)
        for i in range(BOT_COUNT):
            self.bot.bot_generating(i)
        

    def run(self):
        running = True
        pause = False
        m_pressed = 0

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_m:
                        if m_pressed == 0:
                            pygame.mixer.music.pause()
                            m_pressed = 1
                        elif m_pressed == 1:
                            pygame.mixer.music.unpause()
                            m_pressed = 0
                    if not pause:
                        if event.key == K_RIGHT or event.key == K_d:
                            self.move('right', True)
                        if event.key == K_LEFT or event.key == K_a:
                            self.move('left', True)
                    if pause:
                        if event.key == K_SPACE:
                            self.reset()
                            pause = False
                if event.type == KEYUP:
                    if not pause:
                        if event.key == K_RIGHT or event.key == K_d:
                            self.move('right', False)
                        if event.key == K_LEFT or event.key == K_a:
                            self.move('left', False)

            try:
                if not pause:
                    self.road_move(self.road_speed)
                    self.update()
                    self.clock.tick(120)
            except Exception as exception:
                self.new_record()
                self.game_over()
                pause = True

if __name__ == '__main__':
    game = Game()
    game.run()