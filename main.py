""""
This game is normal ping Pong Game with a Catch that the player needs to play from both the sides and maintain their balance.

W and S key to move left Player, Up and down respectively.
Up arrow and Down arrow to move right player, Up and Down Respectively.
END KEY can be used to reset the score.

In the code The left player is referred as Hero and the right player is referred as Devil, and I don't know why? So be carefull of confusions.

And, and! it encrypts the highScore so as to avoid the cheating.

Code by twitter.com/Ishant_Sh | github.com/techishant
"""

import pygame,sys,random,time
from cryptography.fernet import Fernet
random.seed(time.gmtime())

# Encryption Rituals
key = 'GiBu1VzEDKN6iLdkSY0YpYa8Q9zreFhZMNxI_dUNnyc='
fernet = Fernet(key)

# Getting Scores
with open('highScore', 'rb') as file:
    enc_file = file.read()
OhiScore = int(fernet.decrypt(enc_file).decode())
hiScore = OhiScore

# Magician's Secret
app = True
pygame.init()
clock = pygame.time.Clock()

# Some sreen customisations
screen_height = 680
screen_width = 1280
grey = (200,200,200)
light_grey = (246,246,246)
bg_color = pygame.color.Color("#2B6B00")
vic_color = pygame.color.Color('grey11')
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ding Dong")

# Some Sprites 
Scorefont = pygame.font.Font(None,72)
HiScorefont = pygame.font.Font(None,32)
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 -15, 30 , 30)
devil = pygame.Rect(screen_width-20, screen_height / 2 -70, 10 , 140)
hero = pygame.Rect(10, screen_height / 2 -70, 10 , 140)

# Logics:-
# Game Reset
def resetScore():
    """
    This function resets the High Score to 0, encrypts and save it to 'highScore' file.
    And also closes the game.
    """
    global hiScore, app
    hiScore = 0
    with open('highscore', 'wb') as file:
        encryptedScore = fernet.encrypt("0".encode())
        file.write(encryptedScore)
    app = False

def scores():
    """
    This function deals with the Score increment and displaying it on the Screen.
    """
    dis_score = Scorefont.render(str(score), True, light_grey, bg_color)
    dis_score_rect = dis_score.get_rect(center = (screen_width/2, 50))
    screen.blit(dis_score, dis_score_rect)
    dis_hiscore = HiScorefont.render(f"High Score: {str(hiScore)}", True, light_grey, bg_color)
    screen.blit(dis_hiscore, (20, 20))

def ballMechanics():
    """I personally call This function as 'Ball's Neural Network' as it controls the behaviour and almost everything of the ball."""
    global ball_speed_x, ball_speed_y, score, hiScore
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.x >= screen_width or ball.x <= 0:
        ball_speed_x *= -1
    if ball.y >= screen_height or ball.y <= 0:
        ball_speed_y *= -1
    if ball.colliderect(hero) or ball.colliderect(devil):
        score += 1
        ball_speed_x *= -1
        if score > OhiScore:
            hiScore = score

def heroMechanics():
    """
    It controls the behaviour of the hero.
    """
    hero.y += hero_speed
    if hero.top <= 0:
        hero.top = 0
    if hero.bottom >= screen_height:
        hero.bottom = screen_height

def devilMechanics():
    """
    It controls the behaviour of the devil.
    """
    devil.y += devil_speed
    if devil.top <= 0:
        devil.top = 0
    if devil.bottom >= screen_height:
        devil.bottom = screen_height

def loseLogic():
    global app
    """It checks when the game needs to be overed. :("""
    if ball.left <= 0 or ball.right >= screen_width:
        app = False
    
def incDifficulty():
    """It increases the difficulty each time when the player hits the ball. Still not implemented."""
    global ball_speed_y, ball_speed_x
    ball_speed_y += 0.35
    ball_speed_x += 0.35


# Witch's Wise customisations
ball_speed_x,ball_speed_y = 5 * random.choice((1,-1)), 5 * random.choice((1,-1))
player_speed = 7
hero_speed = 0
devil_speed = 0
score = 0

pygame.display.update()

# Main Loop
while app:
    # Sherlock's Code
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          app = False  
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                app = False
                
            # Devil input mechanic's
            if event.key == pygame.K_UP:
                devil_speed -= player_speed
            if event.key == pygame.K_DOWN:
                devil_speed += player_speed

            # Player input mechanic's
            if event.key == pygame.K_w:
                hero_speed -= player_speed
            if event.key == pygame.K_s:
                hero_speed += player_speed
            if event.key == pygame.K_END:
                resetScore()

        if event.type == pygame.KEYUP:

            # Devil input mechanic's
            if event.key == pygame.K_UP:
                devil_speed += player_speed
            if event.key == pygame.K_DOWN:
                devil_speed -= player_speed

            # Player input mechanic's
            if event.key == pygame.K_w:
                hero_speed += player_speed
            if event.key == pygame.K_s:
                hero_speed -= player_speed

    # Screen's makeup
    if OhiScore < hiScore and bg_color == pygame.color.Color("#2B6B00"):
        bg_color = pygame.color.Color("grey11")
    else:
        screen.fill(bg_color)

    # Pasting Sprites
    pygame.draw.rect(screen, grey, hero)
    pygame.draw.rect(screen, grey, devil)
    pygame.draw.circle(screen, grey, [0, screen_height/2], screen_height/2, 1)
    pygame.draw.circle(screen, grey, [screen_width, screen_height/2], screen_height/2, 1)
    pygame.draw.ellipse(screen, grey, ball)
    pygame.draw.aaline(screen, grey, (screen_width / 2, 0), (screen_width /2, screen_height))

    # Scores related stuffs. :)
    scores()

    # Balls Neural Network 
    ballMechanics()    

    # Hero's mechanics
    heroMechanics()
    
    # Devil's mechanics
    devilMechanics()
     
    # Game's Catch
    loseLogic()
    
    # Update Rituals
    pygame.display.flip()
    clock.tick(60)

# Saving Scores
with open('highScore', 'wb') as file:
    encodedHiSc = str(hiScore).encode()
    encryptedScore = fernet.encrypt(encodedHiSc)
    file.write(encryptedScore)

# Ending game
pygame.quit()
sys.exit()