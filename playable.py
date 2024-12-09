#Used GeeksForGeeks tutorial to get started
#https://www.geeksforgeeks.org/snake-game-in-python-using-pygame-module/

import pygame
import time
import random 

# choose difficulty 0 or 1 or 2: easy, medium or hard
# easy: Just Apples
# medium: Higer Speed, Mines + Apples in tougher places
# hard: Even higher Speed, Up to 5 mines at a time + disappearing apples after a few seconds
# Diffculty: {0, 1, 2}
# Rules: don't pass a wall or bite the snake

def main_menu(): 
    global difficulty_level
    pygame.init()
    menu_font = pygame.font.SysFont("times new roman", 30)

    while True:
        game_window.fill(black)

        # Display menu
        title = menu_font.render("Snake Game - Choose Difficulty", True, white)
        game_window.blit(title, (window_x // 4, window_y // 6))

        easy_mode_text = menu_font.render("1. Easy Mode: Slower speed, just random fruits.", True, green)
        medium_mode_text = menu_font.render("2. Medium Mode: Faster speed, includes mines!", True, blue)
        hard_mode_text = menu_font.render("2. Hard Mode: Faster speed and multiple mines!", True, red)
        rules_text = menu_font.render("Rules: Avoid walls, don't bite yourself!", True, white)

        game_window.blit(easy_mode_text, (window_x // 6, window_y // 3))
        game_window.blit(medium_mode_text, (window_x // 6, window_y // 3 + 40))
        game_window.blit(hard_mode_text, (window_x // 6, window_y // 3 + 80))
        game_window.blit(rules_text, (window_x // 6, window_y // 3 + 120))

        pygame.display.flip()

        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                print(f"Key pressed: {event.key}")  # Debugging output
                if event.key == pygame.K_1 or event.key == 49: 
                    difficulty_level = 0
                    print("Difficulty set to Easy")
                    return
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2 or event.key == 50: 
                    difficulty_level = 1
                    print("Difficulty set to Medium")
                    return
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3 or event.key == 50: 
                    difficulty_level = 2
                    print("Difficulty set to Hard")
                    return
                else:
                    print(f"Unrecognized key: {event.key}")  # Debugging for other keys

        pygame.time.delay(100)


def generate_mine():  
    global difficulty_level, fruit_position, mine_position, snake_body
    #generate a mine not on the snake body or the fruit
    while True and difficulty_level == 1:
        mine = [
            random.randrange(1, window_x // 10) * 10, 
            random.randrange(1, window_y // 10) * 10
            ]
        if mine not in snake_body and mine != fruit_position:
            return mine

    while True and difficulty_level == 2:
        mine = []
        for i in range(random.randint(1, 10)):
            oneMine = [
                    random.randrange(1, window_x // 10) * 10, 
                    random.randrange(1, window_y // 10) * 10
                ]
            if oneMine not in snake_body and oneMine != fruit_position:
                mine.append(oneMine)
        return mine

def generate_fruit() -> [int]:
    global difficulty_level, snake_position, fruit_position, mine_position, snake_body
    #generates an apple according to difficulty level
    #and snake length and position
    if difficulty_level == 0 or len(snake_body) < 10:
        return [
            random.randrange(2, window_x // 10 - 1) * 10, 
            random.randrange(2, window_y // 10 - 1) * 10
            ]

    if difficulty_level >= 1: 
        randInt = random.randint(0, 7)
        #randInt will be between 0 and 7
        #if it's smaller or equal to 5: generate apple randomly
        #if it's 6: generate apple near the snake body
        #if it's 7: generate the snake near the border
        if randInt <= 5:
            return [
                random.randrange(2, window_x // 10 - 1) * 10,
                random.randrange(2, window_y // 10 - 1) * 10
                ]

        if randInt == 6:
            #Get middle of snake's body
            middle_square = snake_body[len(snake_body)//2]
            #Return position within 7 steps from the snake's body
            return [
                random.randrange((middle_square[0] - 70)//10, (middle_square[0] + 70)//10)*10,
                random.randrange((middle_square[1] - 70)//10, (middle_square[1] + 70)//10)*10,
            ]

        if randInt == 7:
            #get a random number between 0 and 3:
            #0: generate near bottom x axis
            #1: generate near top x axis
            #2: generate near right y axis
            #3: generate near left y axis
            randInt = random.randint(0,3)
            if randInt == 0:
                return [
                    random.randrange(2, 6) * 10,
                    random.randrange(2, window_y // 10 - 1) * 10
                ]
            if randInt == 1:
                return [
                    random.randrange(window_x // 10 - 6, window_x // 10 - 1) * 10,
                    random.randrange(2, window_y // 10) * 10
                ]
            if randInt == 2:
                return [
                    random.randrange(2, window_x // 10 - 1) * 10,
                    random.randrange(2, 6) * 10
                ]
            if randInt == 3:
                return [
                    random.randrange(2, (window_x // 10) - 1) * 10,
                    random.randrange(window_y // 10 - 6, window_y // 10 - 1) * 10
                ]

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

def play_time():
    global mine_spawn, change_to, direction, window_x, window_y, snake_body, snake_position, snake_speed, fruit_position, fruit_spawn, score, mine_position, difficulty_level
    while True:
        # handling key events
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

        # if two keys pressed simultaneously
        # we don't want the snake to move to different directions simultaneously
        if change_to == "UP" and direction != "DOWN":
            direction = "UP"
        if change_to == "DOWN" and direction != "UP":
            direction = "DOWN"
        if change_to == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        if change_to == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"

        # moving the snake
        if direction == "UP":
            snake_position[1] -= 10
        if direction == "DOWN":
            snake_position[1] += 10
        if direction == "LEFT":
            snake_position[0] -= 10
        if direction == "RIGHT":
            snake_position[0] += 10

        # growing mechanism
        # if fruits and snake collide: score increments by 10
        possible_positions = [
            fruit_position,
            [fruit_position[0] + 10, fruit_position[1]],
            [fruit_position[0] + 10, fruit_position[1] + 10],
            [fruit_position[0], fruit_position[1] + 10]
        ]
        snake_body.insert(0, list(snake_position))
        if snake_position in possible_positions:
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = generate_fruit()
            while fruit_position[0]//10 >= window_x//10 - 1 or fruit_position[0]//10 <= 1 or fruit_position[1]//10 >= window_y//10 - 1 or fruit_position[1]//10 <= 1:
                fruit_position = generate_fruit()
            if difficulty_level >= 1:
                mine_position = generate_mine()
                mine_spawn = True

        fruit_spawn = True
        game_window.fill(black)

        if difficulty_level == 1 and mine_spawn:
            pygame.draw.rect(game_window, red, pygame.Rect(mine_position[0], mine_position[1], 10, 10))
        
        if difficulty_level == 2 and mine_spawn:
            for mine in mine_position:
                pygame.draw.rect(game_window, red, pygame.Rect(mine[0], mine[1], 10, 10))


        # draw snake
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # draw fruit & mine
        pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], 20, 20))


        # game over conditions
        # over the perimeter 
        if snake_position[0] < 0 or snake_position[0] > window_x - 10:
            game_over()
        if snake_position[1] < 0 or snake_position[1] > window_y - 10:
            game_over()

        #snake bites itself
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()

        #snake lands on mine
        if difficulty_level == 1:
            if snake_position == mine_position:
                game_over()

        if difficulty_level == 2:
            for mine in mine_position:
                if snake_position == mine:
                    game_over()

        show_score(1, white, "times new roman", 20)
        pygame.display.update()
        fps.tick(snake_speed[difficulty_level])

if __name__ == "__main__":
    #speed
    snake_speed = [15, 20, 25]

    #GUI Dimensions
    window_x = 720
    window_y = 480
    
    #RGB Colors
    black = pygame.Color(0, 0, 0)
    red = pygame.Color(255, 0, 0)
    white = pygame.Color(255, 255, 255)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)

    pygame.init()
    pygame.display.set_caption("Snake Game")
    game_window = pygame.display.set_mode((window_x, window_y))
    
    #FPS controller
    fps = pygame.time.Clock()
    
    #default snake position
    snake_position = [100, 50]

    #mine position variable
    #mine isn't there byEasy default unless diffculty is 1 or 2
    mine_position = [-1, -1]
    mine_spawn = False
    
    #first 4 blocks of snake's body
    #initial snake's position
    snake_body = [
        [100, 50],
        [90, 50],
        [80, 50],
        [70, 50]
        ]
        
    # fruit position initialization
    fruit_position = [
        random.randrange(1, window_x//10) * 10,
        random.randrange(1, window_y//10) * 10
        ]
    fruit_spawn = True

    #default snake direction
    direction = "RIGHT"
    change_to = direction

    #difficulty level initialized as 0
    difficulty_level = 0
    
    # initial score 
    score = 0
    
    main_menu()
    play_time()