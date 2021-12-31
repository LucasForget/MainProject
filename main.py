import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1800, 900 # the width and height of the screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Preston / Dad Starship Game!")

WHITE = (255, 255, 255) # the colour white
BLACK = (0, 0, 0) # the colour black
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/ZAP.mp3')
EXPLODE_SOUND = pygame.mixer.Sound('Assets/KABOOM.mp3')
ADESTROY_SOUND = pygame.mixer.Sound('Assets/A_DESTROY.mp3')
AHIT_SOUND = pygame.mixer.Sound('Assets/A_HIT.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 150)

FPS = 60 #Frames per second -> number of times the computer draws the screen
VEL = 5
ASTRIOD_NUMBER = 5
ASTRIOD_VEL = 5
BULLET_VEL = 30
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 100, 100
ASTRIOD_WIDTH, ASTRIOD_HEIGHT = 100, 100

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
ASTRIOD_HIT = pygame.USEREVENT + 3
A_HIT = pygame.USEREVENT + 4
R_HIT = pygame.USEREVENT + 5
Y_HIT = pygame.USEREVENT + 6

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png')) # Load Red Spaceship Picture
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90) # Strech Red Spaceship Picture

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

KABOOM_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'EXPLOSION-2.png'))
KABOOM_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    KABOOM_SPACESHIP_IMAGE, (SPACESHIP_WIDTH+150, SPACESHIP_HEIGHT+150)), 0)

ASTRIOD_IMAGE = pygame.image.load(
    os.path.join('Assets', 'astroid.png'))
ASTRIOD = pygame.transform.rotate(pygame.transform.scale(
    ASTRIOD_IMAGE, (ASTRIOD_WIDTH, ASTRIOD_HEIGHT)), 90)

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, astriods):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE) # text for the red health
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE) # text for the yellow health
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10)) # draw red health
    WIN.blit(yellow_health_text, (10, 10)) # draw yellow health

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for astriod in astriods:
        WIN.blit(ASTRIOD, (astriod.x, astriod.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red, astriods):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
        for astriod in astriods:
            if bullet.colliderect(astriod):
                pygame.event.post(pygame.event.Event(ASTRIOD_HIT))
                yellow_bullets.remove(bullet)
                astriod.y = -200
                astriod.x = random.random() * (WIDTH - ASTRIOD_WIDTH)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
        for astriod in astriods:
            if bullet.colliderect(astriod):
                pygame.event.post(pygame.event.Event(ASTRIOD_HIT))
                red_bullets.remove(bullet)
                astriod.y = -200
                astriod.x = random.random() * (WIDTH - ASTRIOD_WIDTH)

def handle_astroid(astriods, yellow, red):
    for astriod in astriods:
        if astriod.y >= HEIGHT:
            astriod.y = -200
            astriod.x = random.random() * (WIDTH - ASTRIOD_WIDTH)
        astriod.y += ASTRIOD_VEL
        if astriod.colliderect(red):
            pygame.event.post(pygame.event.Event(A_HIT))
            red.y += 150
            pygame.event.post(pygame.event.Event(R_HIT))
            if red.y.real >= HEIGHT:
                red.y = HEIGHT - SPACESHIP_HEIGHT
            astriod.y = -200
            astriod.x = random.random() * (WIDTH - ASTRIOD_WIDTH)
        if astriod.colliderect(yellow):
            pygame.event.post(pygame.event.Event(A_HIT))
            yellow.y += 150
            pygame.event.post(pygame.event.Event(Y_HIT))
            if yellow.y >= HEIGHT:
                yellow.y = HEIGHT - SPACESHIP_HEIGHT
            astriod.y = -200
            astriod.x = random.random() * (WIDTH - ASTRIOD_WIDTH)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    red = pygame.Rect(WIDTH - 200, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    astriods = []
    for i in range(1,ASTRIOD_NUMBER):
        astriod = pygame.Rect(random.random() * WIDTH, random.random() * HEIGHT, ASTRIOD_WIDTH, ASTRIOD_HEIGHT)
        astriods.append(astriod)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 30, 10)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 30, 10)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == ASTRIOD_HIT:
                ADESTROY_SOUND.play()

            if event.type == A_HIT:
                ADESTROY_SOUND.play()

            if event.type == Y_HIT:
                yellow_health -= 1

            if event.type == R_HIT:
                red_health -= 1

        winner_text = ""
        if red_health <= 0:
            EXPLODE_SOUND.play()
            WIN.blit(KABOOM_SPACESHIP, (red.x-100, red.y-100))
            winner_text = "DADDY Wins!"

        if yellow_health <= 0:
            EXPLODE_SOUND.play()
            WIN.blit(KABOOM_SPACESHIP, (yellow.x-100, yellow.y-100))
            winner_text = "PRESTON Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_astroid(astriods, yellow, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red, astriods)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health,astriods)

    main()


if __name__ == "__main__":
    main()
