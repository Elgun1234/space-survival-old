import pip
pip.main(["install", "--user", "Pygame"])
import pygame
import math
import time

pygame.font.init()

button_font = pygame.font.Font("ShortBaby-Mg2w.ttf", 30)
TITLE_font = pygame.font.Font("ChrustyRock-ORLA.ttf", 100)
detail_font = pygame.font.Font("FontsFree-Net-calibri-regular.ttf", 30)

button_gap = 30

width, height = 1820, 980
screen = pygame.display.set_mode((width, height))

stars = pygame.image.load("star_sky.jpg")
stars = pygame.transform.scale(stars, (width, height))

up_key = pygame.K_w
down_key = pygame.K_s
right_key = pygame.K_d
left_key = pygame.K_a

shoot_key=0 #m1

pygame.display.set_caption("gods gift to gamers")
TITLE = "SPACE FLY SHOOT AI GAME"

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (170, 255, 0)

FPS = 60

speed = 1
vert_max = 12
hor_max = 12
friction = 0.93  # higher = more slide

mg_speed = 7
mg_bullets = []
mg_tl = 7
mg_dmg = 5
max_mg = 200

DD = 0  # dmg dealt

regen_time = 3  # regen after 3 secs
greater_regen_time = 1.5  # more regen after 5
greater_regen_amm = 2  # 0.5 + 2 per frame
regen_amm = 2
time_last_damaged = 0  # time of last hit

DEAD = pygame.USEREVENT + 1
NEXT_LEVEL = pygame.USEREVENT + 2
HIT = pygame.USEREVENT + 3
MENU = pygame.USEREVENT + 4
SETTINGS = pygame.USEREVENT + 5
LOGIN = pygame.USEREVENT + 6
SIGNUP = pygame.USEREVENT + 7
START = pygame.USEREVENT + 8
PLAY = pygame.USEREVENT + 9


class Bullets:
    def __init__(self, pos_x, pos_y, angle, time):
        img = pygame.image.load("mgbullets.png").convert_alpha()
        self.image = pygame.transform.rotate(img, angle)
        self.x = pos_x
        self.y = pos_y
        self.time = time

        self.angle = angle + 90
        self.xvelo = math.cos(2 * math.pi * (self.angle / 360)) * mg_speed
        self.yvelo = math.sin(2 * math.pi * (self.angle / 360)) * mg_speed
        if self.angle < -90:
            self.xvelo = self.xvelo
            self.yvelo = -self.yvelo
        if self.angle < 0 and self.angle > -90:
            self.yvelo = -self.yvelo
        if angle > -90:
            self.yvelo = -self.yvelo


class Fighters:
    def __init__(self, center_x, center_y, png, xvelo, yvelo, size):
        self.center_x = center_x
        self.center_y = center_y
        self.img = pygame.image.load(f"{png}.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (size))
        self.xvelo = xvelo
        self.yvelo = yvelo


player = Fighters(500, 500, "XO", 0, 0, (34, 50))
enemy = Fighters(400, 400, "eneymy", 0, 0, (50, 50))


def login_menu():
    click = False
    username = ""
    password = ""
    username_collection = False
    password_collection = False
    button_text = []
    while True:
        username_input_box_text = detail_font.render(username, 1, BLACK)
        password_input_box_text = detail_font.render(password, 1, BLACK)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == MENU:
                menu()
            if event.type == pygame.KEYDOWN:
                if username_collection == True:
                    if event.key == pygame.K_RETURN:
                        username = ""
                        username_collection = False
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        if username_input_box_text.get_width()<400:
                            username += event.unicode
                if password_collection== True:
                    if event.key == pygame.K_RETURN:
                        password = ""
                        password_collection = False
                    elif event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        if password_input_box_text.get_width()<400:
                            password += "•"


        mx, my = pygame.mouse.get_pos()

        log_in_text = TITLE_font.render("Log In", 1, WHITE)

        login_button_text = button_font.render("Login", 1, WHITE)
        login_button = pygame.Rect(width//2+200-(login_button_text.get_width()+20),600,login_button_text.get_width()+20,login_button_text.get_height()+20)

        back_button_text = button_font.render("Back", 1, WHITE)
        back_button = pygame.Rect(width // 2 - 200,600,back_button_text.get_width()+20,back_button_text.get_height()+20)

        username_input_box_text = detail_font.render(username, 1, BLACK)
        username_input_box = pygame.Rect(width//2-200,400,400,37)

        password_input_box_text = detail_font.render(password, 1, BLACK)
        password_input_box = pygame.Rect(width // 2 - 200, 500, 400, 37)

        username_text = button_font.render("Username",1,WHITE)
        password_text = button_font.render("Password",1,WHITE)


        button_text.append(login_button_text)
        button_text.append(back_button_text)

        if click:
            if login_button.collidepoint((mx, my)):
                pygame.event.post(pygame.event.Event(MENU))
            elif back_button.collidepoint((mx, my)):
                    break
            elif username_input_box.collidepoint((mx, my)):
                username_collection = True
                password_collection = False
            elif password_input_box.collidepoint((mx, my)):
                password_collection = True
                username_collection = False



        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True

        login_menu_draw(button_text, log_in_text,username_input_box,username_input_box_text,password_input_box_text,password_input_box,username_text,password_text, login_button, back_button)

def login_menu_draw(button_text, log_in_text,username_input_box, username_input_box_text,password_input_box_text,password_input_box,username_text,password_text,*args):
    buttons = list(args)
    screen.blit(stars, (0, 0))
    for i in range(len(buttons)):
        if i == len(buttons):
            break
        pygame.draw.rect(screen, WHITE, buttons[i], 3, 1)
        screen.blit(button_text[i], (buttons[i].x + buttons[i].width // 2 - button_text[i].get_width() // 2,buttons[i].y + buttons[i].height // 2 - button_text[i].get_height() // 2))
    screen.blit(log_in_text, (width // 2 - log_in_text.get_width() // 2, height // 5))
    pygame.draw.rect(screen, WHITE, username_input_box)
    screen.blit(username_input_box_text,(username_input_box.x,username_input_box.y))

    pygame.draw.rect(screen, WHITE, password_input_box)
    screen.blit(password_input_box_text, (password_input_box.x, password_input_box.y))

    screen.blit(username_text, (password_input_box.x, username_input_box.y-username_text.get_height()))
    screen.blit(password_text, (password_input_box.x, password_input_box.y-password_text.get_height()))

    pygame.display.update()


def signup_menu():
    click = False
    username = ""
    password = ""
    confirm_password = ""
    username_collection = False
    password_collection = False
    confirm_password_collection = False
    button_text = []
    while True:
        username_input_box_text = detail_font.render(username, 1, BLACK)
        password_input_box_text = detail_font.render(password, 1, BLACK)
        confirm_password_input_box_text = detail_font.render(confirm_password, 1, BLACK)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == MENU:
                menu()
            if event.type == pygame.KEYDOWN:
                if username_collection == True:
                    if event.key == pygame.K_RETURN:
                        username = ""
                        username_collection = False
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        if username_input_box_text.get_width() < 400:
                            username += event.unicode
                if password_collection == True:
                    if event.key == pygame.K_RETURN:
                        password = ""
                        password_collection = False
                    elif event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    else:
                        if password_input_box_text.get_width() < 400:
                            password += "•"
                if confirm_password_collection == True:
                    if event.key == pygame.K_RETURN:
                        confirm_password = ""
                        password_collection = False
                    elif event.key == pygame.K_BACKSPACE:
                        confirm_password = confirm_password[:-1]
                    else:
                        if confirm_password_input_box_text.get_width() < 400:
                            confirm_password += "•"

        mx, my = pygame.mouse.get_pos()

        sign_up_text = TITLE_font.render("Sign Up", 1, WHITE)

        signup_button_text = button_font.render("Sign Up", 1, WHITE)
        signup_button = pygame.Rect(width//2+200-(signup_button_text.get_width()+20),650,signup_button_text.get_width()+20,signup_button_text.get_height()+20)

        back_button_text = button_font.render("Back", 1, WHITE)
        back_button = pygame.Rect(width // 2 - 200,650,back_button_text.get_width()+20,back_button_text.get_height()+20)

        username_input_box_text = detail_font.render(username, 1, BLACK)
        username_input_box = pygame.Rect(width // 2 - 200, 400, 400, 37)

        password_input_box_text = detail_font.render(password, 1, BLACK)
        password_input_box = pygame.Rect(width // 2 - 200, 500, 400, 37)

        confirm_password_input_box_text = detail_font.render(confirm_password, 1, BLACK)
        confirm_password_input_box = pygame.Rect(width // 2 - 200, 600, 400, 37)

        username_text = button_font.render("Username", 1, WHITE)
        password_text = button_font.render("Password", 1, WHITE)
        confirm_password_text = button_font.render("Confirm password", 1, WHITE)

        button_text.append(signup_button_text)
        button_text.append(back_button_text)

        if click:
            if signup_button.collidepoint((mx, my)):
                pygame.event.post(pygame.event.Event(MENU))
            elif back_button.collidepoint((mx, my)):
                break
            elif username_input_box.collidepoint((mx, my)):
                username_collection = True
                password_collection = False
                confirm_password_collection = False
            elif password_input_box.collidepoint((mx, my)):
                password_collection = True
                username_collection = False
                confirm_password_collection = False
            elif confirm_password_input_box.collidepoint((mx, my)):
                password_collection = False
                username_collection = False
                confirm_password_collection = True

        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True

        signup_menu_draw(button_text, sign_up_text,username_input_box,username_input_box_text,password_input_box_text,password_input_box,confirm_password_input_box,confirm_password_input_box_text,confirm_password_text,username_text,password_text, signup_button, back_button)

def signup_menu_draw(button_text, sign_up_text,username_input_box,username_input_box_text,password_input_box_text,password_input_box,confirm_password_input_box,confirm_password_input_box_text,confirm_password_text,username_text,password_text, *args):
    buttons = list(args)
    screen.blit(stars, (0, 0))
    for i in range(len(buttons)):
        if i == len(buttons):
            break
        pygame.draw.rect(screen, WHITE, buttons[i], 3, 1)
        screen.blit(button_text[i], (buttons[i].x + buttons[i].width // 2 - button_text[i].get_width() // 2,buttons[i].y + buttons[i].height // 2 - button_text[i].get_height() // 2))
    screen.blit(sign_up_text, (width // 2 - sign_up_text.get_width() // 2, height // 5))

    pygame.draw.rect(screen, WHITE, username_input_box)
    screen.blit(username_input_box_text, (username_input_box.x, username_input_box.y))

    pygame.draw.rect(screen, WHITE, password_input_box)
    screen.blit(password_input_box_text, (password_input_box.x, password_input_box.y))

    pygame.draw.rect(screen, WHITE, confirm_password_input_box)
    screen.blit(confirm_password_input_box_text, (password_input_box.x, confirm_password_input_box.y))

    screen.blit(username_text, (password_input_box.x, username_input_box.y - username_text.get_height()))
    screen.blit(password_text, (password_input_box.x, password_input_box.y - password_text.get_height()))
    screen.blit(confirm_password_text, (password_input_box.x, confirm_password_input_box.y - confirm_password_text.get_height()))

    pygame.display.update()

def login_signup_menu():
    click = False

    button_text = []
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == PLAY:
                break
            if event.type == LOGIN:
                login_menu()
            if event.type == SIGNUP:
                signup_menu()

        mx, my = pygame.mouse.get_pos()

        Title_text = TITLE_font.render(TITLE, 1, WHITE)

        login_button_text = button_font.render("Login", 1, WHITE)
        login_button = pygame.Rect((width // 2) - ((login_button_text.get_width() + 20) // 2),(height // 2) - ((login_button_text.get_height() + 20) // 2),login_button_text.get_width() + 20, login_button_text.get_height() + 20)

        sign_up_button_text = button_font.render("Sign Up", 1, WHITE)
        sign_up_button = pygame.Rect((width // 2) - ((sign_up_button_text.get_width() + 20) // 2),(height // 2) - ((login_button_text.get_height() + 20) // 2) + sign_up_button_text.get_height() + 20 + button_gap,sign_up_button_text.get_width() + 20,sign_up_button_text.get_height() + 20)

        button_text.append(login_button_text)
        button_text.append(sign_up_button_text)

        if login_button.collidepoint((mx, my)):
            if click:
                pygame.event.post(pygame.event.Event(LOGIN))
        elif sign_up_button.collidepoint((mx, my)):
            if click:
                pygame.event.post(pygame.event.Event(SIGNUP))

        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True

        login_signup_menu_draw(button_text, Title_text, login_button, sign_up_button)

def login_signup_menu_draw(button_text, Title_text, *args):
    buttons = list(args)
    screen.blit(stars, (0, 0))
    screen.blit(Title_text, (width // 2 - Title_text.get_width() // 2, height // 5))
    for i in range(len(buttons)):
        if i == len(buttons):
            break
        pygame.draw.rect(screen, WHITE, buttons[i], 3, 1)
        screen.blit(button_text[i], (buttons[i].x + buttons[i].width // 2 - button_text[i].get_width() // 2,buttons[i].y + buttons[i].height // 2 - button_text[i].get_height() // 2))

    pygame.display.update()

def menu():
    click = False

    button_text = []
    while True:
        if pygame.mouse.get_pressed()[0]:
            click = True




        mx, my = pygame.mouse.get_pos()
        Title_text = TITLE_font.render(TITLE, 1, WHITE)

        play_button_text = button_font.render("PLAY", 1, WHITE)
        play_button = pygame.Rect((width // 2) - ((play_button_text.get_width() + 20) // 2),(height // 2) - ((play_button_text.get_height() + 20) // 2),play_button_text.get_width() + 20, play_button_text.get_height() + 20)

        Settings_button_text = button_font.render("SETTINGS", 1, WHITE)
        Settings_button = pygame.Rect((width // 2) - ((Settings_button_text.get_width() + 20) // 2),(height // 2) - ((play_button_text.get_height() + 20) // 2) + play_button_text.get_height() + 20 + button_gap,Settings_button_text.get_width() + 20,Settings_button_text.get_height() + 20)

        button_text.append(play_button_text)
        button_text.append(Settings_button_text)

        if play_button.collidepoint((mx, my)):
            if click:
                pygame.event.post(pygame.event.Event(PLAY))

        elif Settings_button.collidepoint((mx, my)):
            if click:
                pygame.event.post(pygame.event.Event(SETTINGS))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == SETTINGS:
                settings_menu()
            if event.type == PLAY:
                main(PLAY)

        click = False


        menu_draw(button_text, Title_text, play_button, Settings_button)

def menu_draw(button_text, Title_text, *args):
    buttons = list(args)
    screen.blit(stars, (0, 0))
    for i in range(len(buttons)):
        if i == len(buttons):
            break
        pygame.draw.rect(screen, WHITE, buttons[i], 3, 1)
        screen.blit(button_text[i], (buttons[i].x + buttons[i].width // 2 - button_text[i].get_width() // 2,buttons[i].y + buttons[i].height // 2 - button_text[i].get_height() // 2))
    screen.blit(Title_text, (width // 2 - Title_text.get_width() // 2, height // 5))

    pygame.display.update()

def settings_menu():
    global width,height,screen,stars,TITLE_font

    click = False
    button_text = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == MENU:
                break

        mx, my = pygame.mouse.get_pos()

        x_button_text = button_font.render("X", 1, WHITE)
        x_button = pygame.Rect(width - 100 - (x_button_text.get_width() + 20), 100,x_button_text.get_width() + 20, x_button_text.get_height() + 20)

        Window_Size_text = button_font.render("Window Size", 1, WHITE)
        Window_Size_1_button_text = button_font.render("1920x1080", 1, WHITE)
        Window_Size_1_button = pygame.Rect(100,100+Window_Size_text.get_height(),Window_Size_1_button_text.get_width()+20,Window_Size_1_button_text.get_height()+20)

        Window_Size_2_button_text = button_font.render("1820x980", 1, WHITE)
        Window_Size_2_button = pygame.Rect(100 + Window_Size_1_button_text.get_width() +20 +20, 100 + Window_Size_text.get_height(), Window_Size_2_button_text.get_width() + 20, Window_Size_2_button_text.get_height() + 20)

        Window_Size_3_button_text = button_font.render("1080x720", 1, WHITE)
        Window_Size_3_button = pygame.Rect(100+Window_Size_2_button_text.get_width()+20 +Window_Size_1_button_text.get_width()+60, 100 + Window_Size_text.get_height(), Window_Size_3_button_text.get_width() + 20, Window_Size_3_button_text.get_height() + 20)



        button_text.append(x_button_text)
        button_text.append(Window_Size_1_button_text)
        button_text.append(Window_Size_2_button_text)
        button_text.append(Window_Size_3_button_text)

        if click:
            if x_button.collidepoint((mx, my)):
                break
            if Window_Size_1_button.collidepoint((mx, my)):
                width=1920
                height=1080
                screen = pygame.display.set_mode((width, height))
                stars = pygame.transform.scale(stars, (width, height))
            if Window_Size_2_button.collidepoint((mx, my)):
                width=1820
                height=980
                screen = pygame.display.set_mode((width, height))
                stars = pygame.transform.scale(stars, (width, height))
            if Window_Size_3_button.collidepoint((mx, my)):
                width=1080
                height=720
                screen = pygame.display.set_mode((width, height))
                stars = pygame.transform.scale(stars, (width, height))
                TITLE_font = pygame.font.Font("ChrustyRock-ORLA.ttf", 70)


        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True

        settings_menu_draw(button_text,Window_Size_text, x_button,Window_Size_1_button,Window_Size_2_button,Window_Size_3_button)

def settings_menu_draw(button_text, Window_Size_text,*args):
    buttons = list(args)
    screen.blit(stars, (0, 0))
    pygame.draw.rect(screen, BLACK, (100, 100, width - 200, height - 200))
    for i in range(len(buttons)):
        if i == len(buttons):
            break
        pygame.draw.rect(screen, WHITE, buttons[i], 3, 1)
        screen.blit(button_text[i], (buttons[i].x + buttons[i].width // 2 - button_text[i].get_width() // 2,buttons[i].y + buttons[i].height // 2 - button_text[i].get_height() // 2))
    screen.blit(Window_Size_text,(100,100))
    pygame.display.update()

def player_movement(player):
    keys = pygame.key.get_pressed()

    if keys[up_key]:
        if -player.yvelo <= vert_max:
            player.yvelo -= speed
    if keys[down_key]:
        if player.yvelo <= vert_max:
            player.yvelo += speed
    if keys[right_key]:
        if player.xvelo <= hor_max:
            player.xvelo += speed
    if keys[left_key]:
        if -player.xvelo <= hor_max:
            player.xvelo -= speed
    if keys[up_key] == False and keys[down_key] == False:
        player.yvelo = player.yvelo * friction

    if keys[right_key] == False and keys[left_key] == False:
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

def shooting(mg_bullets, angle):
    buttons = pygame.mouse.get_pressed()
    if buttons[shoot_key]:
        mg_bullets.append(Bullets(player.center_x, player.center_y, angle, time.time()))

def bullet_stuff(mg_bullets):
    global DD, time_last_damaged
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

def draw(rot_image, rot_image_rect, mg_bullets, DD):

    screen.fill(BLACK)

    screen.blit(enemy.img, (enemy.center_x - 25, enemy.center_y - 25))

    screen.blit(rot_image, rot_image_rect.topleft)

    for i in mg_bullets:
        screen.blit(i.image, (i.x, i.y))

    pygame.draw.rect(screen, GREEN, pygame.Rect(20 + DD, 20, width - 40 - DD, 20))

    pygame.draw.rect(screen, RED, pygame.Rect(20, 20, DD, 20))

    pygame.draw.circle(screen, WHITE, (player.center_x, player.center_y), 5)

    pygame.display.update()

def main(STATE):
    clock = pygame.time.Clock()
    pygame.event.post(pygame.event.Event(STATE))
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == START:
                login_signup_menu()




        enemy.center_x += 2

        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - player.center_x, my - player.center_y
        angle = math.degrees(math.atan2(-dy, dx)) - 90

        rot_image = pygame.transform.rotate(player.img, angle)
        rot_image_rect = rot_image.get_rect(center=(player.center_x, player.center_y))

        keep_on_screeen(player)
        keep_on_screeen(enemy)

        shooting(mg_bullets, angle)
        time_last_damaged = bullet_stuff(mg_bullets)

        regen(time_last_damaged)

        draw(rot_image, rot_image_rect, mg_bullets, DD)
        player_movement(player)

if __name__ == "__main__":
    main(START)
