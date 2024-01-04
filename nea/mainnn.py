import pip

pip.main(["install", "--user", "Pygame"])
import pygame
import math
import time
import socket
import pickle
import datetime
#import sympy as sym

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("127.0.0.1", 3100)

pygame.font.init()

button_font = pygame.font.Font("ShortBaby-Mg2w.ttf", 30)
TITLE_font = pygame.font.Font("ChrustyRock-ORLA.ttf", 100)
detail_font = pygame.font.Font("FontsFree-Net-calibri-regular.ttf", 30)

logged_username = ""

width, height = 1820, 980
screen = pygame.display.set_mode((width, height))

up_key = pygame.K_w  # this is just a number in unicode use chr() to go get actual letter
down_key = pygame.K_s
right_key = pygame.K_d
left_key = pygame.K_a

config = "2,119,97,115,100"

stars = pygame.image.load("star_sky.jpg")
stars = pygame.transform.scale(stars, (width, height))

pygame.display.set_caption("gods gift to gamers")
TITLE = "SPACE FLY SHOOT AI GAME"

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (170, 255, 0)



speed = 1
vert_max = 12
hor_max = 12
friction = 0.93  # higher = more slide

mg_speed = 7
mg_bullets = []
mg_tl = 7
mg_dmg = 5
max_mg = 200

enemy_bullets = []
eb_speed = 2
eb_dmg = 5


DD = 0  # dmg dealt

regen_time = 3  # regen after 3 secs
greater_regen_time = 1.5  # more regen after 5
greater_regen_amm = 2  # 0.5 + 2 per frame
regen_amm = 2
time_last_damaged = 0  # time of last hit
'''
DEAD = pygame.USEREVENT + 1
NEXT_LEVEL = pygame.USEREVENT + 2
HIT = pygame.USEREVENT + 3
MENU = pygame.USEREVENT + 4
SETTINGS = pygame.USEREVENT + 5
LOGIN = pygame.USEREVENT + 6
SIGNUP = pygame.USEREVENT + 7
START = pygame.USEREVENT + 8
PLAY = pygame.USEREVENT + 9
'''
EVENT = ""


class Bullets:
    def __init__(self, pos_x, pos_y, angle, time,bullet_speed):
        img = pygame.image.load("mgbullets.png").convert_alpha()
        self.image = pygame.transform.rotate(img, angle)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.time = time

        self.angle = angle + 90
        self.xvelo = math.cos(2 * math.pi * (self.angle / 360)) * bullet_speed
        self.yvelo = math.sin(2 * math.pi * (self.angle / 360)) * bullet_speed
        if self.angle < -90:
            self.xvelo = self.xvelo
            self.yvelo = -self.yvelo
        if self.angle < 0 and self.angle > -90:
            self.yvelo = -self.yvelo
        if angle > -90:
            self.yvelo = -self.yvelo


class Fighters:
    def __init__(self, center_x, center_y, png, xvelo, yvelo, size):
        self.img = pygame.image.load(f"{png}.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (size))
        self.rect = self.img.get_rect()
        self.rect.x = center_x
        self.rect.y = center_y
        self.xvelo = xvelo
        self.yvelo = yvelo


player = Fighters(500, 500, "XO", 0, 0, (34, 50))
enemy = Fighters(400, 400, "eneymy", 0, 0, (50, 50))


def login_menu():
    click = False
    global EVENT, logged_username,config
    password_dots = ""
    password = ""
    username = ""
    username_collection = False
    password_collection = False
    button_text = []
    wrong_userpass_text = button_font.render("", 1, RED)
    running = True
    while running:
        username_input_box_text = detail_font.render(username, 1, BLACK)
        password_input_box_text = detail_font.render(password_dots, 1, BLACK)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

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
                        password_dots = ""
                        password_collection = False
                    elif event.key == pygame.K_BACKSPACE:
                        password_dots = password_dots[:-1]
                        password = password[:-1]
                    else:
                        if password_input_box_text.get_width() < 400:
                            password_dots += "•"
                            password += event.unicode

        if EVENT == "START":
            running = False
        if EVENT == "MENU":
            menu()
        if EVENT == "PLAY":
            running = False

        mx, my = pygame.mouse.get_pos()

        log_in_text = TITLE_font.render("Log In", 1, WHITE)

        login_button_text = button_font.render("Login", 1, WHITE)
        login_button = pygame.Rect(width // 2 + 200 - (login_button_text.get_width() + 20), 600, login_button_text.get_width() + 20, login_button_text.get_height() + 20)

        back_button_text = button_font.render("Back", 1, WHITE)
        back_button = pygame.Rect(width // 2 - 200, 600, back_button_text.get_width() + 20, back_button_text.get_height() + 20)

        username_input_box_text = detail_font.render(username, 1, BLACK)
        username_input_box = pygame.Rect(width // 2 - 200, 400, 400, 37)

        password_input_box_text = detail_font.render(password_dots, 1, BLACK)
        password_input_box = pygame.Rect(width // 2 - 200, 500, 400, 37)

        username_text = button_font.render("Username", 1, WHITE)
        password_text = button_font.render("Password", 1, WHITE)

        button_text.append(login_button_text)
        button_text.append(back_button_text)

        if click:
            if login_button.collidepoint((mx, my)) and username != "":
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(server_address)
                    data = pickle.dumps(["login", username, password])
                    s.send(data)
                    data = s.recv(2000)  # Receive up to 1024 bytes of data
                    received_data = pickle.loads(data)
                    s.close()
                    if received_data[0] == "True":
                        print(received_data)
                        # print("received")
                        EVENT = "MENU"
                        logged_username = username
                        apply_config(received_data[1])
                        config = received_data[1]

                    else:
                        wrong_userpass_text = detail_font.render("Wrong user or pass", 1, RED)
                except:
                    pass
            elif back_button.collidepoint((mx, my)):
                running = False
                EVENT = "START"
            elif username_input_box.collidepoint((mx, my)):
                username_collection = True
                password_collection = False
            elif password_input_box.collidepoint((mx, my)):
                password_collection = True
                username_collection = False

        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True

        login_menu_draw(button_text, log_in_text, username_input_box, username_input_box_text, password_input_box_text, password_input_box, username_text, password_text, wrong_userpass_text, login_button, back_button)


def login_menu_draw(button_text, log_in_text, username_input_box, username_input_box_text, password_input_box_text, password_input_box, username_text, password_text, wrong_userpass_text, *args):
    buttons = list(args)
    screen.blit(stars, (0, 0))
    for i in range(len(buttons)):
        if i == len(buttons):
            break
        pygame.draw.rect(screen, WHITE, buttons[i], 3, 1)
        screen.blit(button_text[i], (buttons[i].x + buttons[i].width // 2 - button_text[i].get_width() // 2, buttons[i].y + buttons[i].height // 2 - button_text[i].get_height() // 2))
    screen.blit(log_in_text, (width // 2 - log_in_text.get_width() // 2, height // 5))
    pygame.draw.rect(screen, WHITE, username_input_box)
    screen.blit(username_input_box_text, (username_input_box.x, username_input_box.y))

    pygame.draw.rect(screen, WHITE, password_input_box)
    screen.blit(password_input_box_text, (password_input_box.x, password_input_box.y))

    screen.blit(username_text, (password_input_box.x, username_input_box.y - username_text.get_height()))
    screen.blit(password_text, (password_input_box.x, password_input_box.y - password_text.get_height()))

    screen.blit(wrong_userpass_text, (password_input_box.x, password_input_box.y + password_input_box_text.get_height() + 20))

    pygame.display.update()


def signup_validation(username, password, confirm_password):
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    if password != "":
        if confirm_password != "":
            if username != "":
                if len(password) >= 5:
                    if any(i in password for i in numbers):
                        if password == confirm_password:
                            return True
                        else:
                            return False, detail_font.render("Passwords don't match", 1, RED)
                    else:
                        return False, detail_font.render("Passwords has no numbers", 1, RED)
                else:
                    return False, detail_font.render("Password is less than 5 characters", 1, RED)
            else:

                return False, detail_font.render("username is empty", 1, RED)
        else:
            return False, detail_font.render("Confirm Password is empty", 1, RED)
    else:
        return False, detail_font.render("Password is empty", 1, RED)


def signup_menu():
    global EVENT, logged_username
    click = False
    username = ""
    password = ""
    confirm_password = ""
    password_dots = ""
    confirm_password_dots = ""

    username_collection = False
    password_collection = False
    confirm_password_collection = False
    button_text = []
    user_taken_text = detail_font.render("", 1, RED)
    not_match_passwords_text = detail_font.render("", 1, RED)
    running = True
    while running:
        username_input_box_text = detail_font.render(username, 1, BLACK)
        password_input_box_text = detail_font.render(password_dots, 1, BLACK)
        confirm_password_input_box_text = detail_font.render(confirm_password_dots, 1, BLACK)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

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
                        password_dots = ""
                        password_collection = False
                    elif event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                        password_dots = password_dots[:-1]
                    else:
                        if password_input_box_text.get_width() < 400:
                            password += event.unicode
                            password_dots += "•"
                if confirm_password_collection == True:
                    if event.key == pygame.K_RETURN:
                        confirm_password = ""
                        confirm_password_dots = ""
                        password_collection = False
                    elif event.key == pygame.K_BACKSPACE:
                        confirm_password = confirm_password[:-1]
                        confirm_password_dots = confirm_password_dots[:-1]

                    else:
                        if confirm_password_input_box_text.get_width() < 400:
                            confirm_password += event.unicode
                            confirm_password_dots += "•"

        if EVENT == "MENU":
            menu()
        elif EVENT == "PLAY":
            running = False
        elif EVENT == "START":
            running = False

        mx, my = pygame.mouse.get_pos()

        sign_up_text = TITLE_font.render("Sign Up", 1, WHITE)

        signup_button_text = button_font.render("Sign Up", 1, WHITE)
        signup_button = pygame.Rect(width // 2 + 200 - (signup_button_text.get_width() + 20), 750, signup_button_text.get_width() + 20, signup_button_text.get_height() + 20)

        back_button_text = button_font.render("Back", 1, WHITE)
        back_button = pygame.Rect(width // 2 - 200, 750, back_button_text.get_width() + 20, back_button_text.get_height() + 20)

        username_input_box_text = detail_font.render(username, 1, BLACK)
        username_input_box = pygame.Rect(width // 2 - 200, 400, 400, 37)

        password_input_box_text = detail_font.render(password_dots, 1, BLACK)
        password_input_box = pygame.Rect(width // 2 - 200, 500, 400, 37)

        confirm_password_input_box_text = detail_font.render(confirm_password_dots, 1, BLACK)
        confirm_password_input_box = pygame.Rect(width // 2 - 200, 600, 400, 37)

        username_text = button_font.render("Username", 1, WHITE)
        password_text = button_font.render("Password", 1, WHITE)
        confirm_password_text = button_font.render("Confirm password", 1, WHITE)

        button_text.append(signup_button_text)
        button_text.append(back_button_text)

        if click:
            if signup_button.collidepoint((mx, my)):
                result = signup_validation(username, password, confirm_password)

                if result:
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.connect(server_address)
                        print("connected")
                        data = pickle.dumps(["signup", username, password, config, 0])
                        s.send(data)
                        print("sent")
                        data = s.recv(1024)  # Receive up to 1024 bytes of data
                        received_data = data.decode('utf-8')
                        s.close()
                        if received_data == "True":
                            print("received")
                            EVENT = "MENU"
                            logged_username = username
                            print("menu")
                        else:
                            user_taken_text = detail_font.render("Username Taken", 1, RED)
                    except:
                        pass

                else:
                    not_match_passwords_text = result[1]
            elif back_button.collidepoint((mx, my)):
                running = False
                EVENT = "START"
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

        signup_menu_draw(button_text, sign_up_text, username_input_box, username_input_box_text, password_input_box_text, password_input_box, confirm_password_input_box, confirm_password_input_box_text, confirm_password_text, username_text, password_text, user_taken_text, not_match_passwords_text, signup_button, back_button)


def signup_menu_draw(button_text, sign_up_text, username_input_box, username_input_box_text, password_input_box_text, password_input_box, confirm_password_input_box, confirm_password_input_box_text, confirm_password_text, username_text, password_text, user_taken_text, not_match_passwords_text, *args):
    buttons = list(args)
    screen.blit(stars, (0, 0))
    for i in range(len(buttons)):
        if i == len(buttons):
            break
        pygame.draw.rect(screen, WHITE, buttons[i], 3, 1)
        screen.blit(button_text[i], (buttons[i].x + buttons[i].width // 2 - button_text[i].get_width() // 2, buttons[i].y + buttons[i].height // 2 - button_text[i].get_height() // 2))
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

    screen.blit(user_taken_text, (password_input_box.x, confirm_password_input_box.y + confirm_password_input_box_text.get_height() + 20))
    screen.blit(not_match_passwords_text, (password_input_box.x, confirm_password_input_box.y + confirm_password_input_box_text.get_height() + 20 + user_taken_text.get_height() + 10))

    pygame.display.update()


def login_signup_menu():
    click = False
    global EVENT, logged_username
    logged_username = ""
    button_text = []
    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

        mx, my = pygame.mouse.get_pos()

        Title_text = TITLE_font.render(TITLE, 1, WHITE)

        login_button_text = button_font.render("Login", 1, WHITE)
        login_button = pygame.Rect((width // 2) - ((login_button_text.get_width() + 20) // 2), (height // 2) - ((login_button_text.get_height() + 20) // 2), login_button_text.get_width() + 20, login_button_text.get_height() + 20)

        sign_up_button_text = button_font.render("Sign Up", 1, WHITE)
        sign_up_button = pygame.Rect((width // 2) - ((sign_up_button_text.get_width() + 20) // 2), (height // 2) - ((login_button_text.get_height() + 20) // 2) + sign_up_button_text.get_height() + 20 + 30, sign_up_button_text.get_width() + 20, sign_up_button_text.get_height() + 20)

        button_text.append(login_button_text)
        button_text.append(sign_up_button_text)
        if click:
            if EVENT == "PLAY":
                pass
            else:
                if login_button.collidepoint((mx, my)):

                    EVENT = "LOGIN"

                elif sign_up_button.collidepoint((mx, my)):
                    EVENT = "SIGNUP"

        if EVENT == "PLAY":
            running = False
        if EVENT == "LOGIN":
            login_menu()

        if EVENT == "SIGNUP":
            signup_menu()
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
        screen.blit(button_text[i], (buttons[i].x + buttons[i].width // 2 - button_text[i].get_width() // 2, buttons[i].y + buttons[i].height // 2 - button_text[i].get_height() // 2))

    pygame.display.update()


def menu():
    click = False
    global EVENT
    button_text = []

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server_address)
        data = pickle.dumps(["fetch", logged_username])
        s.send(data)
        data = s.recv(1024)
        received_data = data.decode('utf-8')
        s.close()
    except:
        received_data = "didnt work :/"
        pass

    running = True
    while running:
        if pygame.mouse.get_pressed()[0]:
            click = True

        mx, my = pygame.mouse.get_pos()
        Title_text = TITLE_font.render(TITLE, 1, WHITE)

        play_button_text = button_font.render("PLAY", 1, WHITE)
        play_button = pygame.Rect((width // 2) - ((play_button_text.get_width() + 20) // 2), (height // 2) - ((play_button_text.get_height() + 20) // 2), play_button_text.get_width() + 20, play_button_text.get_height() + 20)

        Settings_button_text = button_font.render("SETTINGS", 1, WHITE)
        Settings_button = pygame.Rect((width // 2) - ((Settings_button_text.get_width() + 20) // 2), (height // 2) - ((play_button_text.get_height() + 20) // 2) + play_button_text.get_height() + 20 + 30, Settings_button_text.get_width() + 20, Settings_button_text.get_height() + 20)

        Signout_button_text = button_font.render("Sign Out", 1, WHITE)
        Signout_button = pygame.Rect(width - Signout_button_text.get_width() - 20, height - Signout_button_text.get_height() - 20, Signout_button_text.get_width() + 20, Signout_button_text.get_height() + 20)

        account_text = button_font.render(f"Username: {logged_username} , hours:{received_data}", 1, WHITE)  # fetch date creted to make hrs palyed and fetch highest score

        button_text.append(play_button_text)
        button_text.append(Settings_button_text)
        button_text.append(Signout_button_text)

        if click:

            if play_button.collidepoint((mx, my)):

                EVENT = "PLAY"

            elif Settings_button.collidepoint((mx, my)):

                EVENT = "SETTINGS"
            elif Signout_button.collidepoint((mx, my)):

                EVENT = "START"
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

        if EVENT == "SETTINGS":
            settings_menu()
        if EVENT == "PLAY":
            running = False
        if EVENT == "START":
            running = False
        click = False

        menu_draw(button_text, Title_text, account_text, play_button, Settings_button, Signout_button)


def menu_draw(button_text, Title_text, account_text, *args):
    buttons = list(args)
    screen.blit(stars, (0, 0))
    for i in range(len(buttons)):
        if i == len(buttons):
            break
        pygame.draw.rect(screen, WHITE, buttons[i], 3, 1)
        screen.blit(button_text[i], (buttons[i].x + buttons[i].width // 2 - button_text[i].get_width() // 2, buttons[i].y + buttons[i].height // 2 - button_text[i].get_height() // 2))
    screen.blit(Title_text, (width // 2 - Title_text.get_width() // 2, height // 5))
    screen.blit(account_text, (width - button_text[2].get_width() - 20 - account_text.get_width(), height - account_text.get_height()))

    pygame.display.update()


def apply_config(config):
    global width, height, screen, stars, TITLE_font, up_key, left_key, down_key, right_key
    print(config)
    choices = config.split(",")
    if choices[0] == "1":
        width = 1920
        height = 1080
        screen = pygame.display.set_mode((width, height))
        stars = pygame.image.load("star_sky.jpg")
        stars = pygame.transform.scale(stars, (width, height))
    elif choices[0] == "2":
        width = 1820
        height = 980
        screen = pygame.display.set_mode((width, height))
        stars = pygame.image.load("star_sky.jpg")
        stars = pygame.transform.scale(stars, (width, height))
    elif choices[0] == "3":
        width = 1080
        height = 720
        screen = pygame.display.set_mode((width, height))
        stars = pygame.image.load("star_sky.jpg")
        stars = pygame.transform.scale(stars, (width, height))
    elif choices[0] == "4":
        width = 1920
        height = 1080
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        stars = pygame.image.load("star_sky.jpg")
        stars = pygame.transform.scale(stars, (width, height))
    up_key = int(choices[1])
    left_key = int(choices[2])
    down_key = int(choices[3])
    right_key = int(choices[4])


def settings_menu():
    global width, height, screen, stars, TITLE_font, up_key, left_key, down_key, right_key, EVENT, config
    up_key_collection = False
    left_key_collection = False
    down_key_collection = False
    right_key_collection = False
    click = False
    button_text = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if up_key_collection:
                    up_key = event.key
                    up_key_collection = False
                    config = config.split(",")
                    config[1] = str(up_key)
                    config = ",".join(config)
                if left_key_collection:
                    left_key = event.key
                    left_key_collection = False
                    config = config.split(",")
                    config[2] = str(left_key)
                    config = ",".join(config)
                if down_key_collection:
                    down_key = event.key
                    down_key_collection = False
                    config = config.split(",")
                    config[3] = str(down_key)
                    config = ",".join(config)
                if right_key_collection:
                    right_key = event.key
                    right_key_collection = False
                    config = config.split(",")
                    config[4] = str(right_key)
                    config = ",".join(config)

        mx, my = pygame.mouse.get_pos()

        x_button_text = button_font.render("X", 1, WHITE)
        x_button = pygame.Rect(width - 100 - (x_button_text.get_width() + 20), 100, x_button_text.get_width() + 20, x_button_text.get_height() + 20)

        Window_Size_text = button_font.render("Window Size", 1, WHITE)
        Window_Size_1_button_text = button_font.render("1920x1080", 1, WHITE)
        Window_Size_1_button = pygame.Rect(100, 100 + Window_Size_text.get_height(), Window_Size_1_button_text.get_width() + 20, Window_Size_1_button_text.get_height() + 20)

        Window_Size_2_button_text = button_font.render("1820x980", 1, WHITE)
        Window_Size_2_button = pygame.Rect(100 + Window_Size_1_button_text.get_width() + 20 + 20, 100 + Window_Size_text.get_height(), Window_Size_2_button_text.get_width() + 20, Window_Size_2_button_text.get_height() + 20)

        Window_Size_3_button_text = button_font.render("1080x720", 1, WHITE)
        Window_Size_3_button = pygame.Rect(100 + Window_Size_2_button_text.get_width() + 20 + Window_Size_1_button_text.get_width() + 60, 100 + Window_Size_text.get_height(), Window_Size_3_button_text.get_width() + 20, Window_Size_3_button_text.get_height() + 20)

        fullscreen_button_text = button_font.render("Fullscreen", 1, WHITE)
        fullscreen_button = pygame.Rect(100 + Window_Size_2_button_text.get_width() + 20 + Window_Size_1_button_text.get_width() + 80 + Window_Size_3_button_text.get_width() + 20, 100 + Window_Size_text.get_height(), fullscreen_button_text.get_width() + 20, fullscreen_button_text.get_height() + 20)

        reset_config_button_text = button_font.render("Reset To Default", 1, WHITE)
        reset_config_button = pygame.Rect(width - 100 - (reset_config_button_text.get_width() + 20), height - 100 - (reset_config_button_text.get_height() + 20), reset_config_button_text.get_width() + 20, reset_config_button_text.get_height() + 20)

        save_button_text = button_font.render("Save", 1, WHITE)
        save_config_button = pygame.Rect(width - 100 - (reset_config_button_text.get_width() + 20), height - 100 - (reset_config_button_text.get_height() + 20) - (reset_config_button_text.get_height() + 20) - 30, save_button_text.get_width() + 20, save_button_text.get_height() + 20)

        up_key_text = button_font.render("Up:", 1, WHITE)
        left_key_text = button_font.render("Left:", 1, WHITE)
        down_key_text = button_font.render("Down:", 1, WHITE)
        right_key_text = button_font.render("Right:", 1, WHITE)

        up_key_input_box = pygame.Rect(110 + up_key_text.get_width(), 100 + Window_Size_text.get_height() + Window_Size_1_button_text.get_height() + 30, 50, 35)
        left_key_input_box = pygame.Rect(110 + left_key_text.get_width(), 100 + Window_Size_text.get_height() + Window_Size_1_button_text.get_height() + 32 + 40, 50, 35)
        down_key_input_box = pygame.Rect(110 + down_key_text.get_width(), 100 + Window_Size_text.get_height() + Window_Size_1_button_text.get_height() + 64 + 50, 50, 35)
        right_key_input_box = pygame.Rect(110 + right_key_text.get_width(), 100 + Window_Size_text.get_height() + Window_Size_1_button_text.get_height() + 96 + 60, 50, 35)

        up_key_input_box_text = detail_font.render(chr(up_key).upper(), 1, BLACK)
        left_key_input_box_text = detail_font.render(chr(left_key).upper(), 1, BLACK)
        down_key_input_box_text = detail_font.render(chr(down_key).upper(), 1, BLACK)
        right_key_input_box_text = detail_font.render(chr(right_key).upper(), 1, BLACK)

        button_text.append(x_button_text)
        button_text.append(Window_Size_1_button_text)
        button_text.append(Window_Size_2_button_text)
        button_text.append(Window_Size_3_button_text)
        button_text.append(fullscreen_button_text)
        button_text.append(reset_config_button_text)
        button_text.append(save_button_text)

        if click:
            if x_button.collidepoint((mx, my)):
                running = False
                EVENT = ""
            if reset_config_button.collidepoint((mx, my)):
                apply_config("2,119,97,115,100")
                config = "2,119,97,115,100"
            if save_config_button.collidepoint((mx, my)):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect(server_address)
                    data = pickle.dumps(["config", logged_username, config])
                    s.send(data)
                    data = s.recv(1024)
                    received_data = data.decode('utf-8')
                    if received_data == "True":
                        print("received")
                        print(config)
                    s.close()
                except:
                    pass

            if Window_Size_1_button.collidepoint((mx, my)):
                width = 1920
                height = 1080
                screen = pygame.display.set_mode((width, height))
                stars = pygame.image.load("star_sky.jpg")
                stars = pygame.transform.scale(stars, (width, height))
                config = config.split(",")
                config[0] = "1"
                config = ",".join(config)

            if Window_Size_2_button.collidepoint((mx, my)):
                width = 1820
                height = 980
                screen = pygame.display.set_mode((width, height))
                stars = pygame.image.load("star_sky.jpg")
                stars = pygame.transform.scale(stars, (width, height))
                config = config.split(",")
                config[0] = "2"
                config = ",".join(config)
            if Window_Size_3_button.collidepoint((mx, my)):
                width = 1080
                height = 720
                screen = pygame.display.set_mode((width, height))
                stars = pygame.image.load("star_sky.jpg")
                stars = pygame.transform.scale(stars, (width, height))
                TITLE_font = pygame.font.Font("ChrustyRock-ORLA.ttf", 70)
                config = config.split(",")
                config[0] = "3"
                config = ",".join(config)
            if fullscreen_button.collidepoint((mx, my)):
                width = 1920
                height = 1080
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                stars = pygame.image.load("star_sky.jpg")
                stars = pygame.transform.scale(stars, (width, height))
                config = config.split(",")
                config[0] = "4"
                config = ",".join(config)
            if up_key_input_box.collidepoint((mx, my)):
                up_key_collection = True
                left_key_collection = False
                down_key_collection = False
                right_key_collection = False
            if left_key_input_box.collidepoint((mx, my)):
                up_key_collection = False
                left_key_collection = True
                down_key_collection = False
                right_key_collection = False
            if down_key_input_box.collidepoint((mx, my)):
                up_key_collection = False
                left_key_collection = False
                down_key_collection = True
                right_key_collection = False
            if right_key_input_box.collidepoint((mx, my)):
                up_key_collection = False
                left_key_collection = False
                down_key_collection = False
                right_key_collection = True

        click = False
        if pygame.mouse.get_pressed()[0]:
            click = True

        settings_menu_draw(button_text, Window_Size_text, up_key_text, left_key_text, down_key_text, right_key_text, up_key_input_box_text, left_key_input_box_text, down_key_input_box_text, right_key_input_box_text, up_key_input_box, left_key_input_box, down_key_input_box, right_key_input_box, x_button, Window_Size_1_button, Window_Size_2_button, Window_Size_3_button, fullscreen_button, reset_config_button, save_config_button)


def settings_menu_draw(button_text, Window_Size_text, up_key_text, left_key_text, down_key_text, right_key_text, up_key_input_box_text, left_key_input_box_text, down_key_input_box_text, right_key_input_box_text, up_key_input_box, left_key_input_box, down_key_input_box, right_key_input_box, *args):
    buttons = list(args)
    screen.blit(stars, (0, 0))
    pygame.draw.rect(screen, BLACK, (100, 100, width - 200, height - 200))
    for i in range(len(buttons)):
        if i == len(buttons):
            break
        pygame.draw.rect(screen, WHITE, buttons[i], 3, 1)
        screen.blit(button_text[i], (buttons[i].x + buttons[i].width // 2 - button_text[i].get_width() // 2, buttons[i].y + buttons[i].height // 2 - button_text[i].get_height() // 2))
    screen.blit(Window_Size_text, (100, 100))
    screen.blit(up_key_text, (100, 100 + Window_Size_text.get_height() + button_text[1].get_height() + 30))
    screen.blit(left_key_text, (100, 100 + Window_Size_text.get_height() + 32 + button_text[1].get_height() + 40))
    screen.blit(down_key_text, (100, 100 + Window_Size_text.get_height() + 64 + button_text[1].get_height() + 50))
    screen.blit(right_key_text, (100, 100 + Window_Size_text.get_height() + 96 + button_text[1].get_height() + 60))

    pygame.draw.rect(screen, WHITE, up_key_input_box)
    pygame.draw.rect(screen, WHITE, left_key_input_box)
    pygame.draw.rect(screen, WHITE, down_key_input_box)
    pygame.draw.rect(screen, WHITE, right_key_input_box)

    screen.blit(up_key_input_box_text, (up_key_input_box.x + 10, up_key_input_box.y))
    screen.blit(left_key_input_box_text, (left_key_input_box.x + 10, left_key_input_box.y))
    screen.blit(down_key_input_box_text, (down_key_input_box.x + 10, down_key_input_box.y))
    screen.blit(right_key_input_box_text, (right_key_input_box.x + 10, right_key_input_box.y))

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

    player.rect.y += player.yvelo
    player.rect.x += player.xvelo


def keep_on_screeen(player):
    if player.rect.x - 25 > width:
        player.rect.x -= (25 + width)
    if player.rect.x + 25 < 0:
        player.rect.x += width
    if player.rect.y + 25 >= height:
        player.rect.y = height - 25
    if player.rect.y - 25 <= 0:
        player.rect.y = 25


def shooting(mg_bullets, angle,player):
    buttons = pygame.mouse.get_pressed()
    if buttons[0]:
        mg_bullets.append(Bullets(player.rect.x, player.rect.y, angle, time.time(),mg_speed))


def bullet_stuff(mg_bullets,enemy_bullets):
    global DD, time_last_damaged, EVENT
    for i in mg_bullets:
        if i.rect.colliderect(enemy.rect):  # i.rect.x < enemy.rect.x  + 25 and i.rect.x > enemy.rect.x  - 45 and i.rect.y < enemy.rect.y + 25 and i.rect.y > enemy.rect.y - 45:
            enemy_HIT = True
            DD += mg_dmg
            if DD >= width - 40:
                DD = width - 40
                EVENT = "NEXTLEVEL"
            time_last_damaged = time.time()
        else:
            enemy_HIT = False


        i.rect.x += i.xvelo
        i.rect.y += i.yvelo
        if i.rect.y > height or i.rect.y < 0 or time.time() - i.time > mg_tl or enemy_HIT:
            mg_bullets.remove(i)
        if i.rect.x > width:
            i.rect.x -= width
        if i.rect.x < 0:
            i.rect.x += width
    for i in enemy_bullets:
        i.rect.x += i.xvelo
        i.rect.y += i.yvelo
        if i.rect.colliderect(player.rect):  # i.rect.x < enemy.rect.x  + 25 and i.rect.x > enemy.rect.x  - 45 and i.rect.y < enemy.rect.y + 25 and i.rect.y > enemy.rect.y - 45:
            player_HIT = True
            DD += mg_dmg
            if DD >= width - 40:
                DD = width - 40
                EVENT = "NEXTLEVEL"
            time_last_damaged = time.time()
        else:
            player_HIT = False
        if i.rect.y > height or i.rect.y < 0 or i.rect.x<0 or i.rect.x>width or player_HIT:
            enemy_bullets.remove(i)


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


def draw(rot_image, rot_image_rect, mg_bullets,enemy_bullets, DD):
    screen.fill(BLACK)

    screen.blit(enemy.img, (enemy.rect.x, enemy.rect.y))

    screen.blit(rot_image, rot_image_rect.topleft)

    for i in mg_bullets:
        screen.blit(i.image, (i.rect.x, i.rect.y))
    for i in enemy_bullets:
        screen.blit(i.image, (i.rect.x, i.rect.y))

    pygame.draw.rect(screen, GREEN, pygame.Rect(20 + DD, 20, width - 40 - DD, 20))

    pygame.draw.rect(screen, RED, pygame.Rect(20, 20, DD, 20))

    pygame.draw.circle(screen, WHITE, (player.rect.x, player.rect.y), 5)

    pygame.display.update()

def cross_shooting(enemy_bullets,enemy,x):
    if x%60 == 0:
        enemy_bullets.append(Bullets(enemy.rect.x, enemy.rect.y, 0,0,eb_speed))
        enemy_bullets.append(Bullets(enemy.rect.x, enemy.rect.y, 90,0,eb_speed))
        enemy_bullets.append(Bullets(enemy.rect.x, enemy.rect.y, 180,0,eb_speed))
        enemy_bullets.append(Bullets(enemy.rect.x, enemy.rect.y, 270,0,eb_speed))

def main():
    global EVENT
    clock = pygame.time.Clock()
    #login_signup_menu()
    run = True

    x = 0
    while run:

        x += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if x == 3600:  # 1 min
            x = 0
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(server_address)
                data = pickle.dumps(["hours", logged_username])
                s.send(data)
                s.close()
            except:
                pass

        #enemy.rect.x += 2
        cross_shooting(enemy_bullets, enemy, x)

        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - player.rect.x, my - player.rect.y
        angle = math.degrees(math.atan2(-dy, dx)) - 90

        rot_image = pygame.transform.rotate(player.img, angle)
        rot_image_rect = rot_image.get_rect(center=(player.rect.x, player.rect.y))

        keep_on_screeen(player)
        keep_on_screeen(enemy)

        shooting(mg_bullets, angle,player)
        time_last_damaged = bullet_stuff(mg_bullets,enemy_bullets)

        regen(time_last_damaged)

        draw(rot_image, rot_image_rect, mg_bullets,enemy_bullets, DD)
        player_movement(player)


if __name__ == "__main__":
    main()
