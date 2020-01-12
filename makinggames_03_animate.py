import sys
import pygame

pygame.init()

# frames per second
FPS = 30
fps_clock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption("Animation")

WHITE = (255, 255, 255)
cat_img = pygame.image.load("assets/cat.png")
catx = 10
caty = 10
direction = "right"

# Main game loop
while True:
    DISPLAYSURF.fill(WHITE)

    if direction == "right":
        catx += 5
        if catx == 280:
            direction = "down"
    elif direction == "down":
        caty += 5
        if caty == 220:
            direction = "left"
    elif direction == "left":
        catx -= 5
        if catx == 10:
            direction = "up"
    elif direction == "up":
        caty -= 5
        if caty == 10:
            directon = "right"

    DISPLAYSURF.blit(cat_img, (catx, caty))

    # process events that have happened since the last frame:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fps_clock.tick(FPS)
