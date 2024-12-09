import pygame
import random
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from queue import PriorityQueue

# game-play functions
def generate_mine():
    global difficulty_level, fruit_position, mine_position, snake_body

    if difficulty_level == 0:
        return None

    if difficulty_level == 1:
        while True:
            mine = [
                random.randrange(1, window_x // 10) * 10,
                random.randrange(1, window_y // 10) * 10,
            ]
            if mine not in snake_body and mine != fruit_position:
                return mine

    if difficulty_level == 2:
        mines = []
        for _ in range(random.randint(1, 5)):  # Up to 5 mines
            while True:
                mine = [
                    random.randrange(1, window_x // 10) * 10,
                    random.randrange(1, window_y // 10) * 10,
                ]
                if mine not in snake_body and mine != fruit_position:
                    mines.append(mine)
                    break

        return mines

def generate_fruit():
    while True:
        fruit = [
            random.randrange(2, window_x // 10 - 1) * 10,
            random.randrange(2, window_y // 10 - 1) * 10,
        ]
        if fruit not in snake_body:
            return fruit

def show_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(f"Score: {score}", True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

def calculate_reward():
    global snake_position, fruit_position, mine_position

    reward = -0.1  #small step penalty
    
    #fruit eating reward
    if snake_position == fruit_position:
        return reward + 20, True
    
    #penalties for colliding with walls, mines or self(snake)
    if (snake_position in snake_body[1:] or 
        snake_position[0] < 0 or 
        snake_position[1] < 0 or 
        snake_position[0] >= window_x or 
        snake_position[1] >= window_y or 
        (mine_position and snake_position in (mine_position if isinstance(mine_position, list) else [mine_position]))):
        return -10, False

    #mine proximity penalty if there are mines
    if isinstance(mine_position, list):
        for mine in mine_position:
            if abs(snake_position[0] - mine[0]) < 20 and abs(snake_position[1] - mine[1]) < 20:
                reward -= 5  #penalty for going near mine
    
    return reward, False

#state transfer
def get_state():
    global snake_position, fruit_position, mine_position
    
    state = [
        snake_position[0] < fruit_position[0],  # Is snake to the left of the fruit?
        snake_position[0] > fruit_position[0],  # Is snake to the right of the fruit?
        snake_position[1] < fruit_position[1],  # Is snake above the fruit?
        snake_position[1] > fruit_position[1],  # Is snake below the fruit?
        snake_position[0] <= 0,  # Is snake at the left boundary?
        snake_position[0] >= window_x - 10,  # Is snake at the right boundary?
        snake_position[1] <= 0,  # Is snake at the top boundary?
        snake_position[1] >= window_y - 10,  # Is snake at the bottom boundary?
        any(block == [snake_position[0] - 10, snake_position[1]] for block in snake_body),  # Is there a body block to the left?
        any(block == [snake_position[0] + 10, snake_position[1]] for block in snake_body),  # Is there a body block to the right?
        any(block == [snake_position[0], snake_position[1] - 10] for block in snake_body),  # Is there a body block above?
        any(block == [snake_position[0], snake_position[1] + 10] for block in snake_body),  # Is there a body block below?
    ]
    
    # Check if any mine exists within proximity
    if isinstance(mine_position, list):
        # Check if snake is near any mine
        near_mine = any(abs(snake_position[0] - mine[0]) < 20 and abs(snake_position[1] - mine[1]) < 20 for mine in mine_position)
        state.append(near_mine)  # Add 1 if near a mine, 0 otherwise
    else:
        state.append(0)  # No mines, so no need for proximity checks
    
    # Ensure the state is a fixed length of 12
    return np.array(state[:12], dtype=int)

def make_move(action):
    global direction
    directions = ["UP", "DOWN", "LEFT", "RIGHT"]
    new_direction = directions[action]

    if (direction == "UP" and new_direction != "DOWN") or \
       (direction == "DOWN" and new_direction != "UP") or \
       (direction == "LEFT" and new_direction != "RIGHT") or \
       (direction == "RIGHT" and new_direction != "LEFT"):
        direction = new_direction

def a_star_pathfinding(start, goal):
    """ A* pathfinding algorithm """
    
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance
    
    open_set = PriorityQueue()
    open_set.put((0, start))
    
    came_from = {}
    
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while not open_set.empty():
        current = open_set.get()[1]
        
        if current == goal:
            # Reconstruct path
            total_path = [current]
            while current in came_from:
                current = came_from[current]
                total_path.append(current)
            return total_path[::-1]  # Return reversed path
        
        neighbors = [(current[0]+dx, current[1]+dy) for dx, dy in [(10,0), (-10,0), (0,-10), (0,10)]]
        
        for neighbor in neighbors:
            # Check boundaries, walls, and mines
            if (neighbor not in snake_body and 
                neighbor != fruit_position and 
                (not isinstance(mine_position, list) or neighbor not in mine_position) and 
                neighbor[0] >= 0 and neighbor[0] < window_x and 
                neighbor[1] >= 0 and neighbor[1] < window_y):
                
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    open_set.put((f_score[neighbor], neighbor))
    
    return []  # Return empty if no path found

def play_game(action):
    global snake_position, snake_body, fruit_position, score, fruit_spawn, mine_position

    make_move(action)

    # Move the snake head
    if direction == "UP":
        snake_position[1] -= 10
    elif direction == "DOWN":
        snake_position[1] += 10
    elif direction == "LEFT":
        snake_position[0] -= 10
    elif direction == "RIGHT":
        snake_position[0] += 10

    # Handle collisions and rewards
    reward, apple_eaten = calculate_reward()
    done = reward == -10

    if not done:
        # Update the body of the snake
        snake_body.insert(0, list(snake_position))
        
        if apple_eaten:
            global apples_eaten
            apples_eaten += 1   # Increment apples eaten count
            fruit_spawn = False
            
            return get_state(), reward, done
        
        else:
            # Remove the last segment of the body unless an apple was eaten
            snake_body.pop()
    
        if not fruit_spawn:
            fruit_position = generate_fruit()
            fruit_spawn = True

    return get_state(), reward, done


def reset_game():
    global snake_position, snake_body, fruit_position, direction, score, fruit_spawn, apples_eaten, mine_position
    snake_position = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = "RIGHT"
    fruit_position = generate_fruit()
    fruit_spawn = True
    if difficulty_level > 0:
        mine_position = generate_mine()
    score = 0
    apples_eaten = 0
    mine_position = generate_mine()


def train_step(model, state, action, reward, next_state, done):
    state = np.array(state).reshape(1,-1)  
    next_state = np.array(next_state).reshape(1,-1)  

    target = model.predict(state)
    
    target_next = model.predict(next_state)

    target[0][action] = reward + (0 if done else 0.95 * np.max(target_next))

    model.fit(state,target ,verbose=0)

def train_model(model, episodes=10000, epsilon=1.0, epsilon_decay=0.99):
    
   global score
   
   for episode in range(episodes):
       reset_game()
       
       total_reward=0
        
       done=False
        
       while not done:
           state=get_state()
           
           # Use A* pathfinding to get direction towards the apple
           path_to_fruit=a_star_pathfinding(tuple(snake_body[0]),tuple(fruit_position))
           
           if len(path_to_fruit) > 1:  
               next_move=path_to_fruit[1]
               action=None
            
               # Determine action based on next move coordinates relative to current position 
               if next_move == (snake_body[0][0],snake_body[0][1]-10):  
                   action=0   # UP
               elif next_move == (snake_body[0][0],snake_body[0][1]+10):  
                   action=1   # DOWN 
               elif next_move == (snake_body[0][0]-10,snake_body[0][1]):  
                   action=2   # LEFT 
               elif next_move == (snake_body[0][0]+10,snake_body[0][1]):  
                   action=3   # RIGHT 
           else:  
               if np.random.rand() < epsilon:  
                   action=random.randint(0 ,action_space-1)
               else:  
                   action=np.argmax(model.predict(state.reshape(1,-1)))
            
           next_state,reward ,done=play_game(action)
           
           total_reward+=reward
            
           train_step(model,state ,action,reward,next_state ,done)

       print(f"Episode {episode + 1}/{episodes} - Total Reward: {total_reward}, Apples Eaten: {apples_eaten}")
       
       epsilon=max(epsilon * epsilon_decay ,epsilon_min)

if __name__ == "__main__":
    
    pygame.init()
    window_x, window_y = (720, 480)
    game_window = pygame.display.set_mode((window_x, window_y))
    pygame.display.set_caption("AI Snake Game")

    fps = pygame.time.Clock()
    difficulty_level = 2
    black, red, white, green = (0, 0, 0), (255, 0, 0), (255, 255, 255), (0, 255, 0)

    reset_game()
    state_shape = (12,)
    action_space = 4

    # Initialize epsilon for exploration strategy
    epsilon = 1.0        # Exploration rate
    epsilon_decay = 0.99 # Decay factor for epsilon
    epsilon_min = 0.1   # Minimum value for epsilon

    model = Sequential([
        Input(shape=state_shape),
        Dense(128, activation="relu"),
        Dense(128, activation="relu"),
        Dense(action_space, activation="linear"),
    ])
    model.compile(optimizer="adam", loss="mse")

    train_model(model, episodes=10000)
    model.save("snake_ai_model.h5")
    print("Training complete. Model saved.")
