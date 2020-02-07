import sys
import pygame


pygame.init()

# frames per second
FPS = 30
FPS_CLOCK = pygame.time.Clock()
JUMP_START_VELOCITY = 10


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

# Left-walking images are just flipped versions of the right-walking versions.
# We can use pygame.transform.flip to achieve this.
PLAYER_WALKING_LEFT = []
for img in PLAYER_WALKING_RIGHT:
    PLAYER_WALKING_LEFT.append(pygame.transform.flip(img, True, False))


# A "class" in Python and many other programming languages represents a type
# of object that we manipulate through programming.  In this case, the Player
# class defines what a Player can do and what state it can carry.
class Player:
    IDLE = 0
    MOVE_RIGHT = 1
    MOVE_LEFT = 2
    JUMP = 3
    
    def __init__(self, display: Display):
        self.player_img = PLAYER_IDLE_IMG
        self.player_rect = self.player_img.get_rect()
        self.player_width = self.player_rect.width
        self.player_height = self.player_rect.height
        self.max_y = display.height - self.player_height
        self.x = 10
        self.y = self.max_y
        self.velocity = 5
        # The last move the user
        self.last_move = self.IDLE
        # The number of frames in a row that the most recent move has been made
        self.last_move_repeat_count = 0
        # If the player is jumping, we manage the y position using our jumping
        # algorithm.
        self.is_jumping = False
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
        return int(self.last_move_repeat_count // 4) % 8

    # Update to be called during each frame
    def update(self, movements):
        if len(movements) == 0:
            self.change_last_move(self.IDLE)
        for movement in movements:
            if movement == self.MOVE_RIGHT:
                self.move_right()
            elif movement == self.MOVE_LEFT:
                self.move_left()
            elif movement == self.JUMP:
                self.jump()
        if self.is_jumping:
            # Calculate force which is how fast and in what direction the jump is happening.
            force = self.jumping_mass * self.jumping_velocity
            self.y = self.y - force
            # jumping_velocity starts positive and will end negative
            self.jumping_velocity = self.jumping_velocity - 1
            if self.last_move == self.MOVE_LEFT:
                self.player_img = PLAYER_JUMP_LEFT
            else:
                self.player_img = PLAYER_JUMP_RIGHT

            # If we reach the bottom, then we stop the jump
            # TODO: we will add platforms that we can jump on.
            #       When that happens we'll need to detect landing on a platform
            if self.y >= self.max_y:
                self.y = self.max_y
                self.is_jumping = False
                self.jumping_velocity = JUMP_START_VELOCITY
        else:
            if self.last_move == self.IDLE:
                self.player_img = PLAYER_IDLE_IMG
            elif self.last_move == self.MOVE_LEFT:
                self.player_img = PLAYER_WALKING_LEFT[self.walking_img_index()]
            else:
                self.player_img = PLAYER_WALKING_RIGHT[self.walking_img_index()]

    def render(self, display: Display):
        display.surface.blit(self.player_img, (self.x, self.y))

display = Display()
player = Player(display)

# Main game loop that is executed FPS times per second.
# Each time through the loop is one frame in the game.
while True:
    # Each time we execute a frame, we ask pygame to tell us the state of
    # all the keyboard keys:
    pressed_keys = pygame.key.get_pressed()

    # During each frame, the user may have pressed several keys.  We collect
    # each movement that the user indicated, and will pass those on to the
    # player instance so it may update accordingly.
    movements = []
    if pressed_keys[pygame.K_RIGHT]:
        movements.append(player.MOVE_RIGHT)
    if pressed_keys[pygame.K_LEFT]:
        # If both right and left keys are pressed, we just ignore both.
        # We know that if right has been pressed, then the movements
        # list will have a size of 1 element
        if len(movements) == 1:
            movements = []
        else:
            movements.append(player.MOVE_LEFT)
    if pressed_keys[pygame.K_SPACE]:
        movements.append(player.JUMP)

    # Process events that have happened since the last frame:
    for event in pygame.event.get():
        # print(pygame.event.event_name(event.type))
        # print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the display
    display.clear()
    player.update(movements)
    player.render(display)
    pygame.display.update()
    # Use the FPS clock to maintain smooth animation
    FPS_CLOCK.tick(FPS)
