import pygame
import numpy as np
import math
import random
import time
 
 
pygame.init()
 
WIDTH = 800
HEIGHT = 600
BG_COLOR = "#000000"
window = pygame.display.set_mode((WIDTH, HEIGHT))
 
BACKSPACING = 30
 
PADDLE_COLOR = "#ffffff"
BALL_COLOR = "#ffffff"
 
player1_points = 0
player2_points = 0
 
 
class Paddle(pygame.sprite.Sprite):
    def __init__(self, left=False):
        self.left = left
        self.height = 150
        self.width = 15
        self.speed = 5
        if left:
            self.x = self.width/2 + BACKSPACING
        else:
            self.x = WIDTH - self.width/2 - BACKSPACING
        self.y = HEIGHT/2
       
        self.topleft_x = self.x - self.width/2
        self.topleft_y = self.y - self.height/2
       
   
    def move(self, factor):
        self.y += self.speed * factor
        if self.y < self.height/2:
            self.y = self.height/2
        if self.y > HEIGHT - self.height/2:
            self.y = HEIGHT - self.height/2
       
       
    def update(self):
        self.topleft_x = self.x - self.width/2
        self.topleft_y = self.y - self.height/2
       
       
    def collide(self, other):
        if (self.width/2 + other.radius) > (max(self.x, other.x) - min(self.x, other.x)):
            if (self.y - self.height/2) < other.y < (self.y + self.height/2):
                if self.x < WIDTH/2:
                    radians = math.atan2(self.y - other.y, self.x - self.height/2 - other.x)
                    other.xVel = other.speed * math.cos(radians)
                    other.yVel = (other.speed * math.sin(radians)) * -1
                    other.xVel = abs(other.xVel)
                elif self.x > WIDTH/2:
                    radians = math.atan2(self.y - other.y, self.x + self.height/2 - other.x)
                    other.xVel = other.speed * math.cos(radians)
                    other.yVel = (other.speed * math.sin(radians)) * -1
                    other.xVel = abs(other.xVel) * -1
       
   
   
    def draw(self, surface):
        pygame.draw.rect(surface, PADDLE_COLOR, (self.topleft_x, self.topleft_y, self.width, self.height))
   
       
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        self.radius = 10
        self.speed = 4
        self.angle = random.randint(30, 60) * random.choice((-1, 1))
        self.angle = math.radians(self.angle)
        self.spawn_time = time.time()+5
        self.x = WIDTH/2 - self.radius
        self.y = HEIGHT/2 - self.radius
        self.xVel = self.speed * math.cos(self.angle)
        self.yVel = self.speed * math.sin(self.angle)
 
       
    def update(self):
        if self.spawn_time < time.time():
            self.x += self.xVel
            self.y += self.yVel
       
        if self.y < self.radius or self.y > HEIGHT - self.radius:
            self.yVel *= -1
 
    def goal(self):
        global player1_points, player2_points
        if self.x < -self.radius:
            player2_points += 1
            self.x = WIDTH/2 - self.radius
            self.y = HEIGHT/2 - self.radius
            self.spawn_time = time.time()+5
 
           
           
           
        if self.x > WIDTH + self.radius:
            player1_points += 1
            self.x = WIDTH/2 - self.radius
            self.y = HEIGHT/2 - self.radius
            self.spawn_time = time.time()+5
 
           
 
       
    def draw(self, surface):
        if self.spawn_time < time.time():
            pygame.draw.circle(surface, BALL_COLOR, (self.x, self.y), self.radius)
       
   
paddle1 = Paddle(True)
paddle2 = Paddle()
ball = Ball()
 
 
def main():
    window.fill(BG_COLOR)
    pygame.display.set_caption(f"Player1 points: {player1_points}\t\tPlayer2 points: {player2_points}")
   
    paddle1.update()
    paddle2.update()
    ball.update()
   
    ball.goal()
   
    paddle1.collide(ball)
    paddle2.collide(ball)
   
    paddle1.draw(window)
    paddle2.draw(window)
    ball.draw(window)
 
 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1.move(-1)
    if keys[pygame.K_s]:
        paddle1.move(1)
    if keys[pygame.K_i]:
        paddle2.move(-1)
    if keys[pygame.K_k]:
        paddle2.move(1)
   
   
    main()
   
    pygame.display.flip()
    pygame.time.delay(5)
 
pygame.quit()