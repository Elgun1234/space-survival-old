import pygame
import math
import time

width, height = 1820 , 980
screen = pygame.display.set_mode((width, height))

bg= pygame.image.load("bg.png")
bg = pygame.transform.scale(bg, (1820, 980))
pygame.display.set_caption("gods gift to gamers")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255,255,255)
GREEN = (170, 255, 0)

FPS = 60

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

regen_time = 3 # regen after 3 secs
greater_regen_time = 1.5 # more regen after 5
greater_regen_amm = 2 # 0.5 + 2 per frame
regen_amm = 2
time_last_damaged = 0 # time of last hit

DEAD = pygame.USEREVENT + 1
NEXT_LEVEL = pygame.USEREVENT + 2
HIT = pygame.USEREVENT + 3
MENU = pygame.USEREVENT + 4
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

player = Fighters(500, 500, "XO", 0, 0, (34, 50))
enemy = Fighters(400, 400, "eneymy", 0, 0, (50, 50))

def menu():
    click = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        mx, my = pygame.mouse.get_pos()
        button1 = pygame.Rect(890, 440, 100, 50)
        if button1.collidepoint((mx, my)):
            if click:
                break

        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True


        menu_draw(button1)

def menu_draw(button1):
    pygame.draw.rect(screen, WHITE, button1)
    pygame.display.update()


def player_movement(keys, player):

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

def keep_on_screeen(player):
    if player.center_x - 25 > width:
        player.center_x -= (25 + width)
    if player.center_x + 25 < 0:
        player.center_x += width
    if player.center_y + 25 >= height:
        player.center_y = height - 25
    if player.center_y - 25 <= 0:
        player.center_y = 25

def shooting(buttons,mg_bullets,angle):
    if buttons[0]:
        mg_bullets.append(Bullets(player.center_x, player.center_y, angle, time.time()))
def bullet_stuff(mg_bullets):
    global DD,time_last_damaged
    for i in mg_bullets:
        if i.x < enemy.center_x + 25 and i.x > enemy.center_x - 45 and i.y < enemy.center_y + 25 and i.y > enemy.center_y - 45:
            HIT = True
            DD += mg_dmg
            if DD >= width - 40:
                DD = width - 40
                pygame.event.post(pygame.event.Event(NEXT_LEVEL))
            time_last_damaged = time.time()
        else:
            HIT = False

        i.x += i.xvelo
        i.y += i.yvelo
        if i.y > height or i.y < 0 or time.time() - i.time > mg_tl or HIT:
            mg_bullets.remove(i)
        if i.x > width:
            i.x -= width
        if i.x < 0:
            i.x += width
    if len(mg_bullets) > max_mg:
        del mg_bullets[0]
    return time_last_damaged

def regen(time_last_damaged):
    global DD
    if time.time() - time_last_damaged > regen_time and time_last_damaged != 0:
        if DD > 0:
            DD -= regen_amm
            if time.time() - time_last_damaged > greater_regen_time:
                DD -= greater_regen_amm
def draw(rot_image,rot_image_rect,mg_bullets,DD):

    screen.fill(BLACK)

    screen.blit(enemy.img, (enemy.center_x - 25, enemy.center_y - 25))

    screen.blit(rot_image, rot_image_rect.topleft)

    for i in mg_bullets:
        screen.blit(i.image, (i.x, i.y))

    pygame.draw.rect(screen, GREEN, pygame.Rect(20 + DD, 20, width - 40 - DD, 20))

    pygame.draw.rect(screen, RED, pygame.Rect(20, 20, DD, 20))

    pygame.draw.circle(screen, WHITE, (player.center_x, player.center_y), 5)

    pygame.display.update()
def main():
    clock = pygame.time.Clock()
    pygame.event.post(pygame.event.Event(MENU))
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == NEXT_LEVEL:
                pass
            if event.type == MENU:
                menu()

        keys = pygame.key.get_pressed()
        buttons = pygame.mouse.get_pressed()

        enemy.center_x += 2



        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - player.center_x, my - player.center_y
        angle = math.degrees(math.atan2(-dy, dx)) - 90

        rot_image = pygame.transform.rotate(player.img, angle)
        rot_image_rect = rot_image.get_rect(center=(player.center_x, player.center_y))


        keep_on_screeen(player)
        keep_on_screeen(enemy)

        shooting(buttons, mg_bullets,angle)
        time_last_damaged=bullet_stuff(mg_bullets)

        regen(time_last_damaged)

        draw(rot_image,rot_image_rect,mg_bullets,DD)
        player_movement(keys,player)


if __name__ == "__main__":
    main()
