import pygame
import math
import time

import pygame.sprite

pygame.init()
clock = pygame.time.Clock()
xres = 1820
yres = 980
screen = pygame.display.set_mode((xres, yres))
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255,255,255)
screen.fill(BLACK)
dt = 0
speed = 1
vert_max = 12
hor_max = 16
friction = 0.93
mg_speed = 5
mg_bullets = []
mg_fr = 1


class Bullets:
    def __init__(self, pos_x, pos_y,angle):
        self.image = pygame.image.load("mgbullets.png").convert_alpha()
        self.x = pos_x
        self.y = pos_y


        self.angle = angle +90
        self.xvelo = math.cos(2 * math.pi * (self.angle / 360)) * mg_speed
        self.yvelo = math.sin(2 * math.pi * (self.angle / 360)) * mg_speed
        if self.angle<-90:
            self.xvelo = self.xvelo
            self.yvelo =-self.yvelo
        if self.angle<0 and self.angle>-90:
            self.yvelo = -self.yvelo
        if angle>-90:
            self.yvelo = -self.yvelo







player = pygame.image.load("player2.png").convert_alpha()
player = pygame.transform.scale(player, (50, 50))

player_rect = 500 , 500

center_x = player_rect[0]
center_y = player_rect[1]
xvelo = 0
yvelo = 0

square = pygame.Surface(player.get_size())
square.fill(BLACK)






running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if -yvelo <= vert_max:
            yvelo -= speed
    if keys[pygame.K_s]:
        if yvelo <= vert_max:
            yvelo += speed
    if keys[pygame.K_d]:
        if xvelo <= hor_max:
            xvelo += speed
    if keys[pygame.K_a]:
        if -xvelo <= hor_max:
            xvelo -= speed
    if keys[pygame.K_w] == False and keys[pygame.K_s] == False:
        yvelo = yvelo * friction

    if keys[pygame.K_d] == False and keys[pygame.K_a] == False:
        xvelo = xvelo * friction


    
    center_y += yvelo
    center_x += xvelo

    screen.fill(BLACK)




    mx, my = pygame.mouse.get_pos()
    dx, dy = mx - center_x, my - center_y
    angle = math.degrees(math.atan2(-dy, dx)) - 90

    rot_image = pygame.transform.rotate(player, angle)
    rot_image_rect = rot_image.get_rect(center=player_rect)

    buttons = pygame.mouse.get_pressed()
    if buttons[0]:
        mg_bullets.append(Bullets(center_x, center_y, angle))
        #time.sleep(mg_fr)


    if center_x - 25 > xres:
        center_x -= (25 + xres)
    if center_x + 25 < 0:
        center_x += xres
    if center_y+25 >= yres:
        center_y = yres -25
    if center_y-25 <= 0:
        center_y = 25



    player_rect = center_x, center_y


    screen.blit(square, (center_x-25,center_y-24))
    screen.blit(rot_image, rot_image_rect.topleft)
    for i in mg_bullets:
        screen.blit(i.image, (i.x, i.y))
        i.x += i.xvelo
        i.y += i.yvelo
        if i.x > xres or i.x<0 or i.y > yres or i.y <0:
            mg_bullets.remove(i)

    pygame.draw.circle(screen, WHITE, player_rect, 5)



    pygame.display.update()

    clock.tick(60)




pygame.quit()
