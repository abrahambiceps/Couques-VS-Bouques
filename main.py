import pygame
import os
pygame.font.init()

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Couques VS Bouques")

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0,0,0)
PISS = (225, 225, 20)
SHIT = (122, 89, 1)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 92)

FPS = 60
VEL = 5
BULLET_VEL = 20
MAX_BULLETS = 3
PLAYER_WIDTH, PLAYER_HEIGHT = 100, 100

PLAYER1_HIT = pygame.USEREVENT + 1
PLAYER2_HIT = pygame.USEREVENT + 2

PLAYER1_IMAGE = pygame.image.load(os.path.join('assets', 'player.png'))
PLAYER1 = pygame.transform.scale(PLAYER1_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))
PLAYER2_IMAGE = pygame.image.load(os.path.join('assets', 'player2.png'))
PLAYER2 = pygame.transform.scale(PLAYER2_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT))

def draw_window(player1, player2, player1_bullets, player2_bullets, player2_health, player1_health):
    WIN.fill(GRAY)
    pygame.draw.rect(WIN, BLACK, BORDER)

    player2_health_text = HEALTH_FONT.render("Health: "+str(player2_health), 1, WHITE)
    player1_health_text = HEALTH_FONT.render("Health: "+str(player1_health), 1, WHITE)
    WIN.blit(player2_health_text, (WIDTH - player2_health_text.get_width() -10, 10))
    WIN.blit(player1_health_text, (10, 10))

    WIN.blit(PLAYER1_IMAGE, (player1.x, player1.y))
    WIN.blit(PLAYER2_IMAGE, (player2.x, player2.y))


    for bullet in player1_bullets:
        pygame.draw.rect(WIN, PISS, bullet)
    for bullet in player2_bullets:
        pygame.draw.rect(WIN, SHIT, bullet)
    pygame.display.update()

def player1_handle_movement(keys_pressed, player1):
    if keys_pressed[pygame.K_a] and player1.x -VEL > 0: # LEFT
        player1.x -= VEL
    if keys_pressed[pygame.K_d] and player1.x +VEL + player1.width <BORDER.x: # RIGHT
        player1.x += VEL
    if keys_pressed[pygame.K_w] and player1.y +VEL > 0: # UP
        player1.y -= VEL
    if keys_pressed[pygame.K_s] and player1.y +VEL + player1.height < HEIGHT: # DOWN
        player1.y += VEL

def player2_handle_movement(keys_pressed, player2):
    if keys_pressed[pygame.K_LEFT] and player2.x -VEL > BORDER.x + BORDER.width: # LEFT
        player2.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and player2.x +VEL + player2.width < WIDTH: # RIGHT
        player2.x += VEL
    if keys_pressed[pygame.K_UP] and player2.y -VEL > 0: # UP
        player2.y -= VEL
    if keys_pressed[pygame.K_DOWN] and player2.y +VEL + player2.height < HEIGHT: # DOWN
        player2.y += VEL

def handle_bullets(player1_bullets, player2_bullets, player1, player2):
    for bullet in player1_bullets:
        bullet.x += BULLET_VEL
        if player2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYER2_HIT))
            player1_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            player1_bullets.remove(bullet)

    for bullet in player2_bullets:
        bullet.x -= BULLET_VEL
        if player1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PLAYER1_HIT))
            player2_bullets.remove(bullet)
        elif bullet.x < 0:
            player2_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT //2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(1000 *5)

def main():
    player1 = pygame.Rect(100, 300, PLAYER_WIDTH, PLAYER_HEIGHT)
    player2 = pygame.Rect(700, 300, PLAYER_WIDTH, PLAYER_HEIGHT)

    player1_bullets = []
    player2_bullets = []

    player2_health = 10
    player1_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(player1_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(player1.x + player1.width, player1.y + player1.height//2 -2, 10, 5)
                    player1_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(player2_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(player2.x, player2.y + player2.height//2 -2, 10, 5)
                    player2_bullets.append(bullet)

            if event.type == PLAYER2_HIT:
                player2_health -=1

            if event.type == PLAYER1_HIT:
                player1_health -=1

        winner_text = ""
        if player2_health <=0:
            winner_text = "Couques PISSED ON Bouques!"
        if player1_health <=0:
            winner_text = "Bouques SHAT ON Couques!"

        if winner_text != "":
            draw_winner(winner_text)
            break
        keys_pressed = pygame.key.get_pressed()
        player1_handle_movement(keys_pressed, player1)
        player2_handle_movement(keys_pressed, player2)

        handle_bullets(player1_bullets, player2_bullets, player1, player2)

        draw_window(player1, player2, player1_bullets, player2_bullets, player2_health, player1_health)
    
    main()

if __name__ == "__main__":
    main()