#Used GeeksForGeeks tutorial
#https://www.geeksforgeeks.org/snake-game-in-python-using-pygame-module/

import pygame
import time
import random 

#Array for different snake speeds depending on difficulty
snake_speed = 15

#GUI dimensions
window_x = 720 #1920
window_y = 480 #1080

#RGB colors
black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
white = pygame.Color(255, 255, 255)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

pygame.init()
#Inialize game window
pygame.display.set_caption("Snake Game")
game_window = pygame.display.set_mode((window_x, window_y))

#FPS controller
fps = pygame.time.Clock()

#default snake position
snake_position = [100, 50]

#first 4 blocks of snake's body
#initial snake's position
snake_body = [
    [100, 50],
    [90, 50],
    [80, 50],
    [70, 50]
]

# fruit position
fruit_position = [
    random.randrange(1, (window_x//10) * 10),
    random.randrange(1, 10 * (window_y//10))
    ]
fruit_spawn = True

#default snake direction
direction = "RIGHT"
change_to = direction

# initial score 
score = 0

def show_score(choice, color, font, size):
    #font object score_font
    score_font = pygame.font.SysFont(font, size)

    #display surface object
    score_surface = score_font.render("Score: " + str(score), True, color)

    #text rectangle surface object
    score_rect = score_surface.get_rect()

    #display text
    game_window.blit(score_surface, score_rect)

def game_over():
    my_font = pygame.font.SysFont("times new roamn", 50)
    game_over_surface = my_font.render("Your Score is: " + str(score), True, red)

    #surface rectangle object
    game_over_rect = game_over_surface.get_rect()

    #position
    game_over_rect.midtop = (window_x/2 , window_y/4)

    #draw text
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    #quit after 2 seconds
    time.sleep(2)
    pygame.quit() #deactivate pygame
    quit() #quit program

#main function
while True:
    #handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = "UP"
            if event.key == pygame.K_DOWN:
                change_to = "DOWN"
            if event.key == pygame.K_LEFT:
                change_to = "LEFT"
            if event.key == pygame.K_RIGHT:
                change_to = "RIGHT"

    #if two keys pressed simultaenously
    #we dont want the snake to move to different directions simultaenously

    if change_to == "UP" and direction != "DOWN":
        direction = "UP"
    if change_to == "DOWN" and direction != "UP":
        direction = "DOWN"
    if change_to == "LEFT" and direction != "RIGHT":
        direction = "LEFT"
    if change_to == "RIGHT" and direction != "LEFT":
        direction = "RIGHT"

    #moving the snake
    if direction == "UP":
        snake_position[1] -= 10
    if direction == "DOWN":
        snake_position[1] += 10
    if direction == "LEFT":
        snake_position[0] -= 10
    if direction == "RIGHT":
        snake_position[0] += 10

    #growing mechanism
    #if fruits and snake collide: score increments by 10
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [
            random.randrange(1, (window_x//10) * 10),
            random.randrange(1 , (window_y//10)*10)
            ]
    fruit_spawn = True
    game_window.fill(black)


    #draw snake
    for pos in snake_body[1:]:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
    
    #draw fruit
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    #game over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    show_score(1, white, "time new roman", 20)
    pygame.display.update()
    fps.tick(snake_speed)
    

    





