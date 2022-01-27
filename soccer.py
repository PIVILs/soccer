import sys
import pygame
from pygame.sprite import Sprite
from random import randint
from pygame.sprite import Group
from time import sleep

screen_width = 1400
screen_height = 800
ball_speed_factor = 3

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("SOCCER")
    goalkeeper = Goalkeeper(screen)
    ball = Ball(ball_speed_factor, screen)
    
    while ball.game_active:
        screen.fill((50, 180, 50))
        check_goal(ball)
        goalkeeper.blitme()
        ball.blitme()
        collide_goalkeeper_ball(goalkeeper, ball)
        ball.update()
        check_events(screen, goalkeeper)
        goalkeeper.update()
        pygame.display.flip()

class Goalkeeper(Sprite):
    
    def __init__(self, screen):
        """ Инициализирует вратаря и задает его начальную позицию."""
        self.screen = screen
        super(Goalkeeper, self).__init__()
        
        #self.screen = screen
        self.goalkeeper_speed_factor = 1.5
        
        # Загрузка изображения вратаря и получения прямоугольника.
        self.image = pygame.image.load('images/goalkeeper-183056_640_2.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        self.center = float(self.rect.centerx)
        
        # Флаг перемещения
        self.moving_right = False
        self.moving_left = False
        
    def update(self):
        """ Обновляет позицию вратаря с учетом флагов."""
        # Обновляет атрибут center, не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += 3
        if self.moving_left and self.rect.left > 0:
            self.center -= 3
            
        # Обновление атрибута rect на основании self.center.
        self.rect.centerx = self.center
        
    def blitme(self):
        """ Рисует вратаря в текущей позиции."""
        self.screen.blit(self.image, self.rect)


class Ball(Sprite):
    def __init__(self,ball_speed_factor, screen, ball_limit=3):
        self.screen = screen
        super(Ball, self).__init__()
        self.image = pygame.image.load('images/football-157930_640_1.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Мяч появляется случайно у верхнего края экрана.
        self.rect.centerx = randint(0, screen_width)
        self.rect.top = self.screen_rect.top
        # Сохранение вещественной координаты центра мяча.
        self.center = float(self.rect.centerx)
        self.ball_speed_factor = ball_speed_factor
        self.y = float(self.rect.y)
        self.ball_limit = ball_limit
        self.game_active = True
        
    def update(self):
        """ Перемещает мяч вниз по экрану."""
        self.y += self.ball_speed_factor
        self.rect.bottom = self.y
        if self.rect.top > screen_height:
            self.rect.centerx = randint(self.rect.width/2, screen_width)
            self.y = 0
            print(self.ball_limit)
            sleep(1)
            self.ball_limit -= 1
            
        elif self.rect.top < -300:
            print(self.rect.top)
            self.rect.centerx = randint(self.rect.width/2, screen_width)
            self.ball_speed_factor *= -1

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        
def check_events(screen, goalkeeper):
    """ Обрабатывает нажатие клавиш и события мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                goalkeeper.moving_right = True
            if event.key == pygame.K_LEFT:
                goalkeeper.moving_left = True
            
            if event.key == pygame.K_q:
                sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                goalkeeper.moving_right = False
            if event.key == pygame.K_LEFT:
                goalkeeper.moving_left = False

def collide_goalkeeper_ball(goalkeeper, ball):
    """ Коллизия вратаря и мяча"""
    if pygame.sprite.collide_rect(goalkeeper, ball):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        ball.y = goalkeeper.rect.top
        ball.ball_speed_factor *= -1
        
def check_goal(ball):
    if ball.ball_limit < 1:
        print("Game Over")
        ball.game_active = False

run_game()
