import pip
pip.main(["install", "--user", "Pygame"])
import pygame
import math
import time
import pygame.sprite



pygame.init()
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255,255,255)
GREEN = (170, 255, 0)



'''

class Button():
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(width*scale),(height*scale))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
'''




xres = 1820
yres = 980

bg= pygame.image.load("bg.png")
bg = pygame.transform.scale(bg, (1820, 980))

screen = pygame.display.set_mode((xres, yres))
screen.fill(BLACK)

speed = 1
vert_max = 12
hor_max = 12
friction = 0.93 # higher = more slide

mg_speed = 7
mg_bullets = []
mg_tl = 7
mg_dmg = 5
max_mg = 200

DD = 0 # dmg dealt

font = pygame.font.SysFont(None,20)

regen_time = 3 # regen after 3 secs
greater_regen_time = 1.5 # more regen after 5
greater_regen_amm = 2 # 0.5 + 2 per frame
regen_amm = 2
start_regen = 0 # time of last hit

def write(text, font, color, surface, x, y):
    text = font.render(text, 1, color)
    rect = text.get_rect()
    rect.topleft = (x,y)
    surface.blit(text, rect)
click = False
def StartMenu():
    running = True
    while running:
        screen.blit(bg,(0,0))
        write("play",font,WHITE,screen,100,100)
        mx, my = pygame.mouse.get_pos()
        button1 = pygame.Rect(890,440,100,50)
        if button1.collidepoint((mx,my)):
            if click:
                running = False
        pygame.draw.rect(screen,WHITE,button1)
        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True
        pygame.display.update()
        clock.tick(60)
def game():
    running = True
    while running:


        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if -player.yvelo <= vert_max:
                player.yvelo -= speed
        if keys[pygame.K_s]:
            if player.yvelo <= vert_max:
                player.yvelo += speed
        if keys[pygame.K_d]:
            if player.xvelo <= hor_max:
                player.xvelo += speed
        if keys[pygame.K_a]:
            if -player.xvelo <= hor_max:
                player.xvelo -= speed
        if keys[pygame.K_w] == False and keys[pygame.K_s] == False:
            player.yvelo = player.yvelo * friction

        if keys[pygame.K_d] == False and keys[pygame.K_a] == False:
            player.xvelo = player.xvelo * friction

        player.center_y += player.yvelo
        player.center_x += player.xvelo
        enemy.center_x += 2

        screen.fill(BLACK)

        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - player.center_x, my - player.center_y
        angle = math.degrees(math.atan2(-dy, dx)) - 90

        rot_image = pygame.transform.rotate(player.img, angle)
        rot_image_rect = rot_image.get_rect(center=(player.center_x, player.center_y))

        buttons = pygame.mouse.get_pressed()
        if buttons[0]:
            mg_bullets.append(Bullets(player.center_x, player.center_y, angle, time.time()))

        if player.center_x - 25 > xres:
            player.center_x -= (25 + xres)
        if player.center_x + 25 < 0:
            player.center_x += xres
        if player.center_y + 25 >= yres:
            player.center_y = yres - 25
        if player.center_y - 25 <= 0:
            player.center_y = 25

        if enemy.center_x - 25 > xres:
            enemy.center_x -= (25 + xres)
        if enemy.center_x + 25 < 0:
            enemy.center_x += xres
        if enemy.center_y + 25 >= yres:
            enemy.center_y = yres - 25
        if enemy.center_y - 25 <= 0:
            enemy.center_y = 25

        screen.blit(enemy.img, (enemy.center_x - 25, enemy.center_y - 25))

        screen.blit(rot_image, rot_image_rect.topleft)

        pygame.draw.rect(screen, GREEN, pygame.Rect(20 + DD, 20, xres - 40 - DD, 20))

        '''
            for i in mg_bullets:
                mg_bullets.remove(i)
            player.yvelo = 0
            player.xvelo = 0
            screen.blit(label, (910, 440))
        '''

        for i in mg_bullets:
            if i.x < enemy.center_x + 25 and i.x > enemy.center_x - 45 and i.y < enemy.center_y + 25 and i.y > enemy.center_y - 45:
                HIT = True
                DD += mg_dmg
                if DD >= xres - 40:
                    DD = xres - 40
                start_regen = time.time()
            else:
                HIT = False

            screen.blit(i.image, (i.x, i.y))
            i.x += i.xvelo
            i.y += i.yvelo
            if i.y > yres or i.y < 0 or time.time() - i.time > mg_tl or HIT:
                mg_bullets.remove(i)
            if i.x > xres:
                i.x -= xres
            if i.x < 0:
                i.x += xres

        if time.time() - start_regen > regen_time and start_regen != 0:
            if DD > 0:
                DD -= regen_amm
                if time.time() - start_regen > greater_regen_time:
                    DD -= greater_regen_amm
        pygame.draw.rect(screen, RED, pygame.Rect(20, 20, DD, 20))

        if len(mg_bullets) > max_mg:
            del mg_bullets[0]

        """if xres -40 - DD <= 0 :
            level_change_start = time.time()
            level += 1
            DD = xres-40

            if time.time() - level_change_start < level_t_time :
                screen.blit(label, (970, 440))


                continue
            DD = 0
    """

        pygame.draw.circle(screen, WHITE, (player.center_x, player.center_y), 5)

        pygame.display.update()

        clock.tick(60)

class Bullets:
    def __init__(self, pos_x, pos_y,angle,time):
        img = pygame.image.load("mgbullets.png").convert_alpha()
        self.image = pygame.transform.rotate(img, angle)
        self.x = pos_x
        self.y = pos_y
        self.time = time

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

class Fighters:
    def __init__(self, center_x, center_y, png,xvelo,yvelo,size):
        self.center_x = center_x
        self.center_y = center_y
        self.img = pygame.image.load(f"{png}.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (size))
        self.xvelo = xvelo
        self.yvelo = yvelo



player = Fighters(500,500,"XO",0,0,(34,50))
enemy = Fighters(400,400,"eneymy",0,0,(50,50))






StartMenu()

#game()
pygame.quit()

