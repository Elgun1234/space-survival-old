import pygame
import math

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


class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("mgbullets.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = x,y



player = pygame.image.load("player2.png").convert_alpha()
player = pygame.transform.scale(player, (50, 50))

player_rect = 500 , 500

center_x = player_rect[0]
center_y = player_rect[1]
xvelo = 0
yvelo = 0

square = pygame.Surface(player.get_size())
square.fill(BLACK)
print(player.get_size())





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
    #if :

    
    center_y += yvelo
    center_x += xvelo

    screen.fill(BLACK)




    mx, my = pygame.mouse.get_pos()
    dx, dy = mx - center_x, my - center_y
    angle = math.degrees(math.atan2(-dy, dx)) - 90

    rot_image = pygame.transform.rotate(player, angle)
    rot_image_rect = rot_image.get_rect(center=player_rect)

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

    pygame.draw.circle(screen, WHITE, player_rect, 5)



    pygame.display.update()

    clock.tick(60)




pygame.quit()
