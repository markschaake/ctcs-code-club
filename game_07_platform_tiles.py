import sys
import pygame
from typing import List


pygame.init()

# frames per second
FPS = 30
FPS_CLOCK = pygame.time.Clock()
JUMP_START_VELOCITY = 10

# Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BROWN = (165, 42, 42)

# When rendering the player, we use images saved in our assets directory
PLAYER_IDLE_IMG = pygame.image.load("assets/robot/character_robot_idle.png")
PLAYER_JUMP_RIGHT = pygame.image.load("assets/robot/character_robot_jump.png")
PLAYER_JUMP_LEFT = pygame.transform.flip(PLAYER_JUMP_RIGHT, True, False)
PLAYER_WALKING_RIGHT = [
    pygame.image.load("assets/robot/character_robot_walk0.png"),
    pygame.image.load("assets/robot/character_robot_walk1.png"),
    pygame.image.load("assets/robot/character_robot_walk2.png"),
    pygame.image.load("assets/robot/character_robot_walk3.png"),
    pygame.image.load("assets/robot/character_robot_walk4.png"),
    pygame.image.load("assets/robot/character_robot_walk5.png"),
    pygame.image.load("assets/robot/character_robot_walk6.png"),
    pygame.image.load("assets/robot/character_robot_walk7.png")
]

GROUND_TILE_HEIGHT = 20

# Left-walking images are just flipped versions of the right-walking versions.
# We can use pygame.transform.flip to achieve this.
PLAYER_WALKING_LEFT = []
for img in PLAYER_WALKING_RIGHT:
    PLAYER_WALKING_LEFT.append(pygame.transform.flip(img, True, False))


class Display:
    WHITE = (255, 255, 255)
    def __init__(self):
        self.width = 800
        self.height = 500
        self.surface = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption("Robot!")

    def clear(self):
        self.surface.fill(self.WHITE)

    def render(self):
        pygame.display.update()


class Tile:
    WIDTH = 50
    HEIGHT = GROUND_TILE_HEIGHT

    def __init__(self, x: int, y: int, color: (int, int, int)):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
        self.color = color

    def render(self, display: Display):
        pygame.draw.rect(display.surface, self.color, self.rect)


class Player:
    IDLE = 0
    MOVE_RIGHT = 1
    MOVE_LEFT = 2
    JUMP = 3
    GRAVITY = 15
    MAX_FORCE = 20
    # How fast the player moves in each frame
    VELOCITY = 8

    def __init__(self, display: Display, move_left_key, move_right_key, jump_key):
        self.player_img = PLAYER_IDLE_IMG
        self.move_left_key = move_left_key
        self.move_right_key = move_right_key
        self.jump_key = jump_key
        img_rect = self.player_img.get_rect()
        self.player_width = img_rect.width
        self.feet_width = self.player_width - 54
        self.player_height = img_rect.height
        self.x = 10
        self.y = 10
        self.velocity = self.VELOCITY
        # The last move the user
        self.last_move = self.IDLE
        # The number of frames in a row that the most recent move has been made
        self.last_move_repeat_count = 0
        # If the player is jumping, we manage the y position using our jumping
        # algorithm.
        self.is_jumping = False
        self.is_falling = False
        self.jumping_velocity = JUMP_START_VELOCITY
        self.jumping_mass = 2

    def change_last_move(self, last_move):
        if self.last_move == last_move:
            self.last_move_repeat_count = self.last_move_repeat_count + 1
        else:
            self.last_move = last_move
            self.last_move_repeat_count = 0

    def move_right(self):
        self.x = self.x + self.velocity
        self.change_last_move(self.MOVE_RIGHT)

    def move_left(self):
        self.x = self.x - self.velocity
        self.change_last_move(self.MOVE_LEFT)

    def jump(self):
        self.is_jumping = True

    def walking_img_index(self):
        return int(self.last_move_repeat_count // 2) % 8

    def player_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.player_width, self.player_height)

    def player_collide_rect(self) -> pygame.Rect:
        width = self.player_width - 25
        edge_buffer = (self.player_width - width)/2
        top_buffer = 35
        height = self.player_height - top_buffer
        return pygame.Rect(self.x + edge_buffer, self.y + top_buffer, width, height)
    
    def feet_rect(self) -> pygame.Rect:
        edge_buffer = (self.player_width - self.feet_width) / 2
        return pygame.Rect(self.x + edge_buffer, self.y + self.player_height, self.feet_width, 1)

    # Update to be called during each frame
    def update(self, pressed_keys, tiles: List[Tile]):
        movements = []
        if pressed_keys[self.move_right_key]:
            movements.append(self.MOVE_RIGHT)
        if pressed_keys[self.move_left_key]:
            if len(movements) == 1:
                movements = []
            else:
                movements.append(self.MOVE_LEFT)
        if pressed_keys[self.jump_key]:
            movements.append(self.JUMP)

        if len(movements) == 0:
            self.change_last_move(self.IDLE)
        for movement in movements:
            if movement == self.MOVE_RIGHT:
                self.move_right()
            elif movement == self.MOVE_LEFT:
                self.move_left()
            elif movement == self.JUMP and not self.is_falling:
                self.jump()

        if self.is_jumping:
            # Calculate force which is how fast and in what direction the jump is happening.
            force = self.jumping_mass * self.jumping_velocity
            if force + self.MAX_FORCE < 0:
                force = -self.MAX_FORCE
            self.y = self.y - force
            # jumping_velocity starts positive and will end negative
            self.jumping_velocity = self.jumping_velocity - 1
            if self.last_move == self.MOVE_LEFT:
                self.player_img = PLAYER_JUMP_LEFT
            else:
                self.player_img = PLAYER_JUMP_RIGHT
            if force < 0:
                collide_idx = self.feet_rect().collidelist(tiles)
                if collide_idx > -1:
                    self.y = tiles[collide_idx].y - self.player_height
                    self.is_jumping = False
                    self.jumping_velocity = JUMP_START_VELOCITY
        else:
            if self.last_move == self.IDLE:
                self.player_img = PLAYER_IDLE_IMG
            elif self.last_move == self.MOVE_LEFT:
                self.player_img = PLAYER_WALKING_LEFT[self.walking_img_index()]
            else:
                self.player_img = PLAYER_WALKING_RIGHT[self.walking_img_index()]
            collide_idx = self.feet_rect().collidelist(tiles)
            if collide_idx == -1:
                # Player is falling since there is no ground below
                self.is_falling = True
                self.y = self.y + self.GRAVITY
            else:
                self.is_falling = False
                self.y = tiles[collide_idx].y - self.player_height

    def render(self, display: Display):
        #pygame.draw.rect(display.surface, YELLOW, self.player_collide_rect())
        display.surface.blit(self.player_img, (self.x, self.y))
        #pygame.draw.rect(display.surface, RED, self.feet_rect())


display = Display()
player1 = Player(display, pygame.K_a, pygame.K_d, pygame.K_w)
player2 = Player(display, pygame.K_k, pygame.K_SEMICOLON, pygame.K_o)
player2.x = display.width - player2.player_width

def generate_tiles(display: Display):
    tiles = []
    # Add the floor tiles
    for x in range(0, display.width, 50):
        tiles.append(Tile(x, display.height - GROUND_TILE_HEIGHT, BROWN))
    # Add some tiles to jump up onto
    tiles.append(Tile(200, display.height - 100, BLUE))
    tiles.append(Tile(300, display.height - 200, BLUE))
    tiles.append(Tile(400, display.height - 300, BLUE))
    return tiles

# Main game loop that is executed FPS times per second.
# Each time through the loop is one frame in the game.
while True:
    # Each time we execute a frame, we ask pygame to tell us the state of
    # all the keyboard keys:
    pressed_keys = pygame.key.get_pressed()

    # Process events that have happened since the last frame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the display
    display.clear()
    tiles = generate_tiles(display)
    for tile in tiles:
        tile.render(display)
    player1.update(pressed_keys, tiles)
    player1.render(display)
    player2.update(pressed_keys, tiles)
    player2.render(display)
    pygame.display.update()
    # Use the FPS clock to maintain smooth animation
    FPS_CLOCK.tick(FPS)
