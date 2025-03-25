import pygame
from random import randint
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

finished = False

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def drawRect(color, pos, width, height):
    pygame.draw.rect(screen, color, (pos[0], pos[1], width, height), 4)
    
def drawTriangle(color, pos, width, height):
    pygame.draw.polygon(screen, color, [pos, [pos[0] - width, pos[1] + height], [pos[0] + width, pos[1] + height]], 4)
    
def drawTrueTriangle(color, pos, width):
    pygame.draw.polygon(screen, color, [pos, [pos[0] - width, pos[1] + width], [pos[0] + width, pos[1] + width]], 4)

def drawRhombus(color, pos, width):
    pygame.draw.polygon(screen, color, [pos, [pos[0] + width, pos[1] + width], [pos[0] + 2 * width, pos[1]], [pos[0] + width, pos[1] - width]], 4)

    
    
def drawSqr(color, pos, width):
    pygame.draw.rect(screen, color, (pos[0], pos[1], width, width), 4)

def drawCircle(color, pos, RAD):
    pygame.draw.circle(screen, color, pos, RAD, 4)
    

def eraser(pos, RAD):
    pygame.draw.circle(screen, WHITE, pos, RAD)
RAD = 30

drawing = False
color = BLACK

screen.fill(pygame.Color('white'))

start_pos = 0
end_pos = 0

mode = 0

all_colors = []

for _ in range(20):
    all_colors.append((randint(0,255), randint(0,255), randint(0,255)))



while not finished:
    clock.tick(FPS)

    

    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = pos
            if pos[0] > 20 and pos[0] < 720 and pos[1] > 20 and pos[1] < 40:
                color = screen.get_at(pos)
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = pos
            rect_x = abs(start_pos[0] - end_pos[0])
            rect_y = abs(start_pos[1] - end_pos[1])
            
            
            if mode == 0:
                drawRect(color, start_pos, rect_x, rect_y)
            elif mode == 1:
                drawCircle(color, start_pos, rect_x)
            elif mode == 3:
                drawSqr(color, start_pos, rect_x)
            elif mode == 4:
                drawTriangle(color, start_pos, rect_x, rect_y)
            elif mode == 5:
                drawTrueTriangle(color, start_pos, rect_x)
            elif mode == 6:
                drawRhombus(color, start_pos, rect_x)
                
            
        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == 2:
                eraser(pos, RAD)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mode += 1
                mode %= 7
            if event.key == pygame.K_BACKSPACE:
                screen.fill(WHITE)


    

    each = 35
    for i, col in enumerate(all_colors):
        pygame.draw.rect(screen, col, (20 + i * each, 20, each, 20))
    pygame.display.flip()
pygame.quit()