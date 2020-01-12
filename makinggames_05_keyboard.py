import sys
import pygame

pygame.init()

# frames per second
FPS = 30
fps_clock = pygame.time.Clock()

# Set up the display window dimensions:
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 500
DISPLAYSURF = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), 0, 32)
pygame.display.set_caption("Robot!")

WHITE = (255, 255, 255)

# Here we load our robot character image and detect its dimensions.
robot_img = pygame.image.load("assets/robot/character_robot_idle.png")
robot_rect = robot_img.get_rect()
robot_width = robot_rect.width
robot_height = robot_rect.height

# Here we intialize the robot's starting location.  We'll change these values
# when we react to user input.
robotx = 10
roboty = 10

# VELOCITY represents how fast the character moves.  The number it is set to
# is the number of pixels that the character can move during a single frame.
# Try changing the velocity and see what happens.
VELOCITY = 5

# Main game loop that is executed FPS times per second.
# Each time through the loop is one frame in the game.
while True:
    # Each time we execute a frame, we ask pygame to tell us the state of
    # all the keyboard keys:
    pressed_keys = pygame.key.get_pressed()
    # The pressed_keys variable above is now an array contain True/False
    # values for every key on the keyboard.  To tell if a key is pressed,
    # we look up that key's value by accessing it with a pygame-provided
    # constant.
    if pressed_keys[pygame.K_RIGHT]:
        # the value of pressed_keys[pygame.K_RIGHT] is True, which means the
        # user has pressed the right arrow key on the keyboard.  To react to
        # their input, we change increase the robotx value so on the next
        # redraw the robot will be drawn slightly to the right.
        robotx += VELOCITY

    # TODO: add handling for other keyboard keys:
    # K_LEFT, K_DOWN, K_UP, any others (a, s, d, f)?
    
    # Process events that have happened since the last frame:
    for event in pygame.event.get():
        # print(pygame.event.event_name(event.type))
        # print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update the display
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(robot_img, (robotx, roboty))
    pygame.display.update()
    # Use the FPS clock to maintain smooth animation
    fps_clock.tick(FPS)
