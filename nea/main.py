import pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 1000))
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255,255,255)
screen.fill(BLACK)
dt = 0
speed = 1
friction = 0.8
"""
class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width, pos_x , pos_y):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x , pos_y)




"""
player = pygame.image.load("player2.png").convert_alpha()
player = pygame.transform.scale(player, (50, 48))
player_x = 100
player_y = 100
xvelo = 0
yvelo = 0

square = pygame.Surface(player.get_size())
square.fill(BLACK)
"""
sprite_group = pygame.sprite.Group()

square = Sprite(RED,100,100,player_x,player_y)
"""
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        yvelo -= speed
    if keys[pygame.K_s]:
        yvelo += speed
    if keys[pygame.K_d]:
        xvelo += speed
    if keys[pygame.K_a]:
        xvelo -= speed
    if keys[pygame.K_w] == False and keys[pygame.K_s] == False:
        yvelo = yvelo * friction

    if keys[pygame.K_d] == False and keys[pygame.K_a] == False:
        xvelo = xvelo * friction

    player_y += yvelo
    player_x += xvelo



    pygame.display.flip()
    screen.blit(square, (player_x,player_y))
    screen.blit(player, (player_x,player_y))
    dt=clock.tick(60) * .001



pygame.quit()
