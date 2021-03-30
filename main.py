import pygame
import os

pygame.font.init()         # for font
pygame.mixer.init()        # for sound effect

# window initialized and other parameter defined
width, height = 900, 500
win = pygame.display.set_mode((width,height))
spaceship_width, spaceship_heigth = 55, 40          # object sizing
border = pygame.Rect(width//2 -5, 0, 20, height)    # for middle border

# sound effect
bullet_hit_sound = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
bullet_fire_sound = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))
# color and font initialized
white = (255,255,255)
black = (0,0,0)
RED = (255,0,0)
YELLOW =(255,255,0)
health_font = pygame.font.SysFont("comicsans", 40)
winner_font = pygame.font.SysFont("comicsans", 110)

# other parameter
FPS = 60                           # windows refresh rate per seconds
vel = 4                            # velocity for movement of object per key pressed
bullet_vel = 7                     # velocity of bullets
bullet_num = 2                     # bullet fire per control
yellow_hit = pygame.USEREVENT + 1  # for player 1st
red_hit = pygame.USEREVENT + 2     # for player 2nd

# for title and icon set
pygame.display.set_caption('ROCKET GAME')
icon = pygame.image.load(os.path.join('Assets','rocket.png'))
pygame.display.set_icon(icon)

# bg- image and object image uploading
yellow_spaceship_image = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(yellow_spaceship_image,(spaceship_width, spaceship_heigth)),90)

red_spaceship_image = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
red_spaceship = pygame.transform.rotate(pygame.transform.scale(red_spaceship_image,(spaceship_width, spaceship_heigth)),270)

space = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')),(width,height))

# window update function --to avoid writing repeatation syntax for update.window()
def update_window(red,yellow,red_bullets, yellow_bullets, red_health, yellow_health):
    win.blit(space,(0,0))
    pygame.draw.rect(win,black,border)
    red_health_text = health_font.render("Health: "+str(red_health),1,white)
    yellow_health_text = health_font.render("Health: "+str(yellow_health),1,white)
    win.blit(red_health_text,(width-red_health_text.get_width()-10,10))
    win.blit(yellow_health_text, (10, 10))

    win.blit(yellow_spaceship,(yellow.x,yellow.y))
    win.blit(red_spaceship, (red.x,red.y))

    for bullet in red_bullets:
        pygame.draw.rect(win,RED,bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(win,YELLOW,bullet)

    pygame.display.update()

# movement control for yellow rockets
def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - vel > 0:             # left
        yellow.x -= vel
    if keys_pressed[pygame.K_d] and yellow.x + vel < border.x-40:   # right
        yellow.x += vel
    if keys_pressed[pygame.K_w] and yellow.y - vel > 0:             # up
        yellow.y -= vel
    if keys_pressed[pygame.K_s] and yellow.y + vel < height-50:      # down
        yellow.y += vel

# movement control for red rockets
def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - vel > border.x+20:    # left
        red.x -= vel
    if keys_pressed[pygame.K_RIGHT] and red.x + vel < width-40:       # right
        red.x += vel
    if keys_pressed[pygame.K_UP] and red.y - vel > 0:                 # up
        red.y -= vel
    if keys_pressed[pygame.K_DOWN] and red.y + vel < height-50:       # down
        red.y += vel

# bullets parameter
def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)
        elif bullet.x > width:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

# for winning text
def winner(text):
    draw_text = winner_font.render(text, 1, white)
    win.blit(draw_text, (width/2 -draw_text.get_width()/2, height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(6000)

#main function
def main():
    red = pygame.Rect(700, 300, spaceship_width, spaceship_heigth)
    yellow = pygame.Rect(100, 300, spaceship_width, spaceship_heigth)
    yellow_bullets = []
    red_bullets = []
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run= True
    while run:
        clock.tick(FPS)
        # quit function
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # bullets controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < bullet_num:
                    bullet = pygame.Rect(yellow.x + yellow.width , yellow.y + yellow.height//2 -2,10,5)
                    yellow_bullets.append(bullet)
                    bullet_fire_sound.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < bullet_num:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    bullet_fire_sound.play()

            if event.type == red_hit:
                red_health -= 1
                bullet_hit_sound.play()
            if event.type == yellow_hit:
                yellow_health -= 1
                bullet_hit_sound.play()

        # winning text
        winner_text = ""
        if red_health <= 0:
            winner_text ="Yellow wins...!"
        if yellow_health <= 0:
            winner_text = "Red wins...!"
        if winner_text != "":
            winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed,yellow)
        red_movement(keys_pressed, red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)

        update_window(red, yellow, red_bullets, yellow_bullets, red_health,yellow_health)

    main()      # to restart the game after winning

# for continuing game window
if __name__ == "__main__":
    main()