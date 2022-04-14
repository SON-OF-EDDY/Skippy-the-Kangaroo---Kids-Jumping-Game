import pygame

pygame.mixer.init()
pygame.font.init()

pygame.display.set_caption("SKIPPY!")

WIDTH = 700
HEIGHT = 500

WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))

KANGAROO_WIDTH_RECTANGLE = 60
KANGAROO_WIDTH_IMAGE = 80
KANGAROO_HEIGHT_IMAGE = 80
KANGAROO_HEIGHT_RECTANGLE = 60

ECHIDNA_WIDTH = 40
ECHIDNA_HEIGHT_RECTANGLE = 40
ECHIDNA_HEIGHT_IMAGE = 55

SNAKE_WIDTH = 100
SNAKE_HEIGHT_RECTANGLE = 48
SNAKE_HEIGHT_IMAGE = 58

MAGPIE_WIDTH = 65
MAGPIE_HEIGHT = 35

HELO_WIDTH = 170
HELO_HEIGHT = 60

CLOUD_WIDTH = 150
CLOUD_HEIGHT = 75

KANGAROO = pygame.image.load("kangaroo_transparent.png")
ECHINDNA = pygame.image.load("echindna_transparent.png")
SNAKE = pygame.image.load("snake_transparent.png")
MAGPIE = pygame.image.load("magpie_transparent.png")
HELO = pygame.image.load("helicopter_transparent.png")
CLOUD_1 = pygame.image.load("cloud_1_transparent.png")
CLOUD_2 = pygame.image.load("cloud_2_transparent.png")

SCALED_KANGAROO = pygame.transform.scale(KANGAROO,(KANGAROO_WIDTH_IMAGE,KANGAROO_HEIGHT_IMAGE))
SCALED_ECHIDNA = pygame.transform.scale(ECHINDNA,(ECHIDNA_WIDTH,ECHIDNA_HEIGHT_IMAGE))
SCALED_SNAKE = pygame.transform.scale(SNAKE,(SNAKE_WIDTH,SNAKE_HEIGHT_IMAGE))
SCALED_MAGPIE = pygame.transform.scale(MAGPIE,(MAGPIE_WIDTH,MAGPIE_HEIGHT))
SCALED_HELO = pygame.transform.scale(HELO,(HELO_WIDTH,HELO_HEIGHT))
SCALED_CLOUD_1 = pygame.transform.scale(CLOUD_1,(CLOUD_WIDTH,CLOUD_HEIGHT))
SCALED_CLOUD_2 = pygame.transform.scale(CLOUD_2,(CLOUD_WIDTH,CLOUD_HEIGHT))

BLACK = (0,0,0)

GAME_OVER_FONT = pygame.font.SysFont('comicsans',50)
SCORE_FONT = pygame.font.SysFont('comicsans',25)

FPS = 60

COLLISION = pygame.USEREVENT + 1
WIN_CONDITION = pygame.USEREVENT + 2

high_score = 0
score = 0

frame = 1
start = True
stop = False
cycle = 1
play_magpie = True

BASE_VELOCITY = 6
VELOCITY_INCREMENT = 2

# update_screen

def draw_update_window(kangaroo,echidna,snake,magpie,helo,cloud_1,cloud_2):

    global high_score
    global score

    background_original = pygame.image.load("DESERT.png")

    background = pygame.transform.scale(background_original, (WIDTH, HEIGHT))

    WINDOW.blit(background,(0,0))

    WINDOW.blit(SCALED_KANGAROO,(kangaroo.x,kangaroo.y))
    WINDOW.blit(SCALED_ECHIDNA,(echidna.x,echidna.y))
    WINDOW.blit(SCALED_SNAKE,(snake.x,snake.y))
    WINDOW.blit(SCALED_MAGPIE,(magpie.x,magpie.y))

    WINDOW.blit(SCALED_HELO,(helo.x,helo.y))
    WINDOW.blit(SCALED_CLOUD_1,(cloud_1.x,cloud_1.y))
    WINDOW.blit(SCALED_CLOUD_2, (cloud_2.x, cloud_2.y))

    str_score = "SCORE: " + str(score)

    if score > high_score:
        str_high_score = "HIGH SCORE: "+str(score)
    else:
        str_high_score = "HIGH SCORE: "+str(high_score)

    draw_score = SCORE_FONT.render(str_score,1,BLACK)
    draw_high_score = SCORE_FONT.render(str_high_score,1,BLACK)

    WINDOW.blit(draw_score,(500,150))
    WINDOW.blit(draw_high_score,(500,180))

    pygame.display.update()

def handle_collision(kangaroo,echidna,snake,magpie):

    if kangaroo.colliderect(echidna):
        pygame.event.post(pygame.event.Event(COLLISION))
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('hedgehog_collide.mp3'))
        pygame.mixer.Channel(0).set_volume(0.25)
    elif kangaroo.colliderect(snake):
        pygame.event.post(pygame.event.Event(COLLISION))
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('snake_collision.mp3'))
        pygame.mixer.Channel(1).set_volume(0.5)
    elif kangaroo.colliderect(magpie):
        pygame.event.post(pygame.event.Event(COLLISION))
        pygame.mixer.Channel(4).play(pygame.mixer.Sound('hurt_effect.mp3'))
        pygame.mixer.Channel(4).set_volume(0.8)

def draw_loser_text(text):
    draw_text = GAME_OVER_FONT.render(text,1,BLACK)
    WINDOW.blit(draw_text,((WIDTH-draw_text.get_width())//2,(HEIGHT-draw_text.get_height())//2))
    pygame.display.update()
    pygame.time.delay(3000)

def handle_win_condition():
    if score == 8400:
        pygame.event.post(pygame.event.Event(WIN_CONDITION))

def draw_winner_text(text):
    draw_text = GAME_OVER_FONT.render(text, 1, BLACK)
    pygame.mixer.Channel(6).play(pygame.mixer.Sound('crikey.mp3'))
    pygame.mixer.Channel(6).set_volume(0.8)
    WINDOW.blit(draw_text, ((WIDTH - draw_text.get_width()) // 2, (HEIGHT - draw_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(10000)

#main_game_loop
def main():

    pygame.mixer.Channel(7).play(pygame.mixer.Sound('crash_theme.mp3'))
    pygame.mixer.Channel(7).set_volume(1)

    global high_score
    global score

    global start
    global frame
    global cycle
    global play_magpie

    #load_in_music

    run = True

    ECHIDNA_START = 700

    SNAKE_START = 1100

    MAGPIE_START = 7600

    HELO_START = 2100

    CLOUD_1_START = 700

    CLOUD_2_START = 700

    kangaroo = pygame.Rect(50,HEIGHT-KANGAROO_HEIGHT_IMAGE,KANGAROO_WIDTH_RECTANGLE,KANGAROO_HEIGHT_RECTANGLE)
    echidna = pygame.Rect(ECHIDNA_START,HEIGHT-ECHIDNA_HEIGHT_IMAGE,ECHIDNA_WIDTH,ECHIDNA_HEIGHT_IMAGE)
    snake = pygame.Rect(SNAKE_START,HEIGHT-SNAKE_HEIGHT_IMAGE,SNAKE_WIDTH,SNAKE_HEIGHT_IMAGE)
    magpie = pygame.Rect(MAGPIE_START,HEIGHT-75,MAGPIE_WIDTH,MAGPIE_HEIGHT)

    helo = pygame.Rect(750,25,HELO_WIDTH,HELO_HEIGHT)
    cloud_1 = pygame.Rect(150,50,CLOUD_WIDTH,CLOUD_HEIGHT)
    cloud_2 = pygame.Rect(550,70,CLOUD_WIDTH,CLOUD_HEIGHT)

    clock = pygame.time.Clock()

    jump = False

    HELO_VELOCITY = 6

    CLOUD_VELOCITY = 1

    GRAVITY = 1

    ORIGINAL_VELOCITY = 25

    jump_velocity = ORIGINAL_VELOCITY

    if helo.x == 750:
        pygame.mixer.Channel(5).play(pygame.mixer.Sound('choppa_passing.mp3'))
        pygame.mixer.Channel(5).set_volume(0.2)

    while run:

        clock.tick(FPS)

        handle_win_condition()

        handle_collision(kangaroo,echidna,snake,magpie)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == COLLISION:
                draw_loser_text("GAME OVER, MATE!!!")
                if score > high_score:
                    high_score = score
                score = 0
                frame = 1
                cycle = 1
                main()

            if event.type == WIN_CONDITION:
                draw_winner_text("TRU BLUE WINNER,YOU BEAUTY!!!")
                exit()
                pygame.quit()

        userInput = pygame.mouse.get_pressed(num_buttons=3)
        if jump == False and userInput[0]:
            jump = True
            pygame.mixer.Channel(3).play(pygame.mixer.Sound('jump.mp3'))
            pygame.mixer.Channel(3).set_volume(0.8)

        if jump == True:
            kangaroo.y = kangaroo.y - jump_velocity
            jump_velocity = jump_velocity - GRAVITY
            if jump_velocity < - ORIGINAL_VELOCITY:
                jump = False
                jump_velocity = ORIGINAL_VELOCITY

        #snake and echidna movement

        echidna_start = 700

        snake_start = SNAKE_WIDTH + 700 + 300

        magpie_start = 700

        if cycle < 3:
            base_velocity = BASE_VELOCITY
        elif cycle < 5:
            base_velocity = BASE_VELOCITY + 1
        elif cycle < 7:
            base_velocity = BASE_VELOCITY + 2
        else:
            base_velocity = BASE_VELOCITY + 3

        if frame == 1:
            if start == True:
                start = False
                echidna.x = echidna_start
                snake.x = snake_start
            elif start == False:
                velocity = base_velocity
                echidna.x = echidna.x - velocity
                snake.x = snake.x - velocity
                if snake.x < -SNAKE_WIDTH:
                    frame = frame + 1
                    score = score + 100
                    start = True

        if frame == 2:
            if start == True:
                echidna_start = 700
                snake_start = SNAKE_WIDTH + 700 + 50
                start = False
                echidna.x = echidna_start
                snake.x = snake_start
            elif start == False:
                velocity = base_velocity + (VELOCITY_INCREMENT*1)
                echidna.x = echidna.x - velocity
                snake.x = snake.x - velocity
                if snake.x < -SNAKE_WIDTH:
                    frame = frame + 1
                    score = score + 100
                    start = True

        if frame == 3:
            if start == True:
                echidna_start = 700
                snake_start = SNAKE_WIDTH + 700 + 400
                start = False
                echidna.x = echidna_start
                snake.x = snake_start
            elif start == False:
                velocity = base_velocity + (VELOCITY_INCREMENT*2)
                echidna.x = echidna.x - velocity
                snake.x = snake.x - velocity

                if snake.x < -SNAKE_WIDTH:
                    frame = frame + 1
                    score = score + 100
                    start = True

        if frame == 4:
            if start == True:
                start = False
                magpie.x = magpie_start
                pygame.mixer.Channel(2).play(pygame.mixer.Sound('hawk_attack.mp3'))
                pygame.mixer.Channel(2).set_volume(0.8)
            elif start == False:
                velocity = base_velocity + (VELOCITY_INCREMENT*4)
                magpie.x = magpie.x - velocity

                if magpie.x < -MAGPIE_WIDTH:
                    frame = frame + 1
                    score = score + 50
                    start = True

        if frame == 5:
            if start == True:
                echidna_start = 700
                magpie_start = MAGPIE_WIDTH + 700 + 700
                start = False
                echidna.x = echidna_start
                magpie.x = magpie_start
            elif start == False:
                if play_magpie == True and magpie.x < 650:
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('hawk_attack.mp3'))
                    pygame.mixer.Channel(2).set_volume(0.8)
                    play_magpie = False
                velocity = base_velocity + (VELOCITY_INCREMENT*3)
                echidna.x = echidna.x - velocity
                magpie.x = magpie.x - velocity

                if magpie.x < -MAGPIE_WIDTH:
                    frame = frame + 1
                    score = score + 100
                    play_magpie = True
                    start = True

        if frame == 6:
            if start == True:
                echidna_start = 700
                magpie_start = MAGPIE_WIDTH + 700 + 300
                snake_start = SNAKE_WIDTH + 700 + 700
                start = False
                echidna.x = echidna_start
                magpie.x = magpie_start
                snake.x = snake_start
            elif start == False:
                if play_magpie == True and magpie.x < 700:
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound('hawk_attack.mp3'))
                    pygame.mixer.Channel(2).set_volume(0.8)
                    play_magpie = False
                velocity = base_velocity + VELOCITY_INCREMENT
                echidna.x = echidna.x - velocity
                magpie.x = magpie.x - velocity
                snake.x = snake.x - velocity

                if snake.x < -SNAKE_WIDTH:
                    cycle = cycle + 1
                    frame = 1
                    play_magpie = True

                    score = score + 150
                    start = True

        # helo movement

        if helo.x > -HELO_WIDTH and helo.x == 750:
            pygame.mixer.Channel(5).play(pygame.mixer.Sound('choppa_passing.mp3'))
            pygame.mixer.Channel(5).set_volume(0.1)
            helo.x = helo.x - HELO_VELOCITY
        elif helo.x > -HELO_WIDTH:
            helo.x = helo.x - HELO_VELOCITY
        else:
            helo.x = HELO_START

        # cloud_1 movement
        if cloud_1.x > -CLOUD_WIDTH:
            cloud_1.x = cloud_1.x - CLOUD_VELOCITY
        else:
            cloud_1.x = CLOUD_1_START

        # cloud_2 movement
        if cloud_2.x > -CLOUD_WIDTH:
            cloud_2.x = cloud_2.x - CLOUD_VELOCITY
        else:
            cloud_2.x = CLOUD_2_START

        draw_update_window(kangaroo,echidna,snake,magpie,helo,cloud_1,cloud_2)

    exit()
    pygame.quit()

main()

