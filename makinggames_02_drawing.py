import sys
import pygame

pygame.init()
DISPLAYSURF = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption("Drawing")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DISPLAYSURF.fill(WHITE)

# Green pentagon (5 sides)
pygame.draw.polygon(DISPLAYSURF, GREEN, (
    (146, 0),
    (291, 106),
    (236, 277),
    (56, 277),
    (0, 106)))

# Blue Z
pygame.draw.line(DISPLAYSURF, BLUE, (60, 60), (120, 60), 4)
pygame.draw.line(DISPLAYSURF, BLUE, (120, 60), (60, 120))
pygame.draw.line(DISPLAYSURF, BLUE, (60, 120), (120, 120), 4)

# Blue small circle
pygame.draw.circle(DISPLAYSURF, BLUE, (300, 250), 20, 0)

# Red ellipse
pygame.draw.ellipse(DISPLAYSURF, RED, (300, 250, 40, 80), 1)

# Red rectangle
pygame.draw.rect(DISPLAYSURF, RED, (200, 150, 100, 50))

# Diagonal black dotted line
pix_obj = pygame.PixelArray(DISPLAYSURF)
pix_obj[480][380] = BLACK
pix_obj[482][382] = BLACK
pix_obj[484][384] = BLACK
pix_obj[486][386] = BLACK
pix_obj[488][388] = BLACK
del pix_obj

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
