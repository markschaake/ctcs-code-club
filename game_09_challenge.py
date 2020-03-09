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
        self.width = 1200
        self.height = 800
        self.surface = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption("Robot!")

    def clear(self):
        self.surface.fill(self.WHITE)

    def render(self):
        pygame.display.update()


# A Block can be used to build ground, walls, and platforms
class Block:
    def __init__(self, x: int, y: int, height: int, width: int, color: (int, int, int)):
        self.x = x
        self.y = y - height
        self.height = height
        self.width = width
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
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
        self.display = display
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

    def move_right(self, rects):
        self.set_x(self.x + self.velocity, rects)
        self.change_last_move(self.MOVE_RIGHT)

    def move_left(self, rects):
        self.set_x(self.x - self.velocity, rects)
        self.change_last_move(self.MOVE_LEFT)

    def jump(self):
        self.is_jumping = True
        self.jumping_velocity = JUMP_START_VELOCITY

    def walking_img_index(self):
        return int(self.last_move_repeat_count // 2) % 8

    def player_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.player_width, self.player_height)

    def player_collide_rect(self) -> pygame.Rect:
        width = self.player_width - 26
        edge_buffer = (self.player_width - width)/2
        top_buffer = 35
        height = self.player_height - top_buffer
        return pygame.Rect(self.x + edge_buffer, self.y + top_buffer, width, height)
    
    def feet_rect(self) -> pygame.Rect:
        edge_buffer = (self.player_width - self.feet_width) / 2
        return pygame.Rect(self.x + edge_buffer, self.y + self.player_height, self.feet_width, 1)

    def set_y(self, y, rects):
        """Sets y ensuring that no collisions exist after the setting."""
        self.y = y
        collide_idx = self.feet_rect().collidelist(rects)
        if collide_idx is not -1:
            self.y = rects[collide_idx].rect.top - self.player_height
            self.is_jumping = False
            self.is_falling = False
        else:
            self.is_falling = True

    def set_x(self, x, rects):
        """Sets x ensuring no collisions exist after setting"""
        self.x = x
        player_collide_rect = self.player_collide_rect()
        player_rect = self.player_rect()
        collisions = player_collide_rect.collidelistall(rects)
        max_right = player_collide_rect.right
        min_left = player_collide_rect.left
        for idx in collisions:
            rect = rects[idx].rect
            if rect.collidepoint(player_collide_rect.topright):
                if rect.left < max_right:
                    max_right = rect.left
            if rect.collidepoint(player_collide_rect.bottomright):
                if rect.left < max_right:
                    max_right = rect.left
            if rect.collidepoint(player_collide_rect.midright):
                if rect.left < max_right:
                    max_right = rect.left
            if player_collide_rect.collidepoint(rect.midleft):
                if rect.left < max_right:
                    max_right = rect.left
            if rect.collidepoint(player_collide_rect.topleft):
                if rect.right > min_left:
                    min_left = rect.right
            if rect.collidepoint(player_collide_rect.bottomleft):
                if rect.right > min_left:
                    min_left = rect.right
            if rect.collidepoint(player_collide_rect.midleft):
                if rect.right > min_left:
                    min_left = rect.right
            if player_collide_rect.collidepoint(rect.midright):
                if rect.right > min_left:
                    min_left = rect.right
        if max_right < player_collide_rect.right:
            right_buffer = player_rect.right - player_collide_rect.right
            self.x = max_right - player_rect.width + right_buffer
        elif min_left > player_collide_rect.left:
            left_buffer = player_collide_rect.left - player_rect.left
            self.x = min_left - left_buffer
            
    # Update to be called during each frame
    def update(self, pressed_keys, rects):
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
                self.move_right(rects)
            elif movement == self.MOVE_LEFT:
                self.move_left(rects)
            elif movement == self.JUMP and not self.is_falling and not self.is_jumping:
                self.jump()

        if self.is_jumping:
            # Calculate force which is how fast and in what direction the jump is happening.
            force = self.jumping_mass * self.jumping_velocity
            if force + self.MAX_FORCE < 0:
                force = -self.MAX_FORCE
            self.set_y(self.y - force, rects)
            # jumping_velocity starts positive and will end negative
            self.jumping_velocity = self.jumping_velocity - 1
            if self.last_move == self.MOVE_LEFT:
                self.player_img = PLAYER_JUMP_LEFT
            else:
                self.player_img = PLAYER_JUMP_RIGHT
            if force > 0: # going up
                player_rect = self.player_collide_rect()
                collisions = player_rect.collidelistall(rects)
                has_top_collision = False
                for idx in collisions:
                    rect = rects[idx].rect
                    if rect.collidepoint(player_rect.topright):
                        has_top_collision = True
                        break
                    if rect.collidepoint(player_rect.topleft):
                        has_top_collision = True
                        break
                    if rect.collidepoint(player_rect.midtop):
                        has_top_collision = True
                        break
                    if player_rect.collidepoint(rect.midbottom):
                        has_top_collision = True
                        break
                if has_top_collision:
                    self.jumping_velocity = 0
        else:
            if self.last_move == self.IDLE:
                self.player_img = PLAYER_IDLE_IMG
            elif self.last_move == self.MOVE_LEFT:
                self.player_img = PLAYER_WALKING_LEFT[self.walking_img_index()]
            else:
                self.player_img = PLAYER_WALKING_RIGHT[self.walking_img_index()]
            collide_idx = self.feet_rect().collidelist(rects)
            if collide_idx == -1:
                # Player is falling since there is no ground below
                self.set_y(self.y + self.GRAVITY, rects)

    def render(self):
        pygame.draw.rect(self.display.surface, YELLOW, self.player_collide_rect())
        self.display.surface.blit(self.player_img, (self.x, self.y))
        #pygame.draw.rect(display.surface, RED, self.feet_rect())


display = Display()
player1 = Player(display, pygame.K_a, pygame.K_d, pygame.K_w)
player2 = Player(display, pygame.K_k, pygame.K_SEMICOLON, pygame.K_o)
player2.x = display.width - player2.player_width


def generate_blocks(display: Display):
    blocks = []
    floor_y = display.height - GROUND_TILE_HEIGHT
    
    # Add the floor
    blocks.append(Block(x=0, y=display.height, width=display.width, height=20, color=BROWN))

    # Add a barrier wall
    blocks.append(Block(x=display.width/2, y=display.height, width=20, height=600, color=BROWN))

    # Left and right edges to prevent player from falling to infinity
    blocks.append(Block(x=-100, y=display.height, height=display.height, width=100, color=BLUE))
    blocks.append(Block(x=display.width, y=display.height, height=display.height, width=100, color=BLUE))

    # Callenge: add some blocks so that player1 and player2 can get over the middle wall
    
    return blocks


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
    player1.rect = player1.player_collide_rect()
    player2.rect = player2.player_collide_rect()
    blocks = generate_blocks(display)
    player1_rects = [player2]
    player2_rects = [player1]
    for block in blocks:
        block.render(display)
        player1_rects.append(block)
        player2_rects.append(block)

    player1.update(pressed_keys, player1_rects)
    player1.render()
    player2.update(pressed_keys, player2_rects)
    player2.render()
    pygame.display.update()
    # Use the FPS clock to maintain smooth animation
    FPS_CLOCK.tick(FPS)
