import pygame
from random import randint
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LINE_COLOR = (50, 50, 50)
font = pygame.font.SysFont("Verdana", 20)

HEIGHT = 500
WIDTH = 500
WIDTHSCREEN = 700

BLOCK_SIZE = 20


class Point:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        
class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.location = Point(self.x, self.y)
        
    def draw(self):
        point = self.location
        rect = pygame.Rect(BLOCK_SIZE * point.x, BLOCK_SIZE * point.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, (0, 255, 0), rect)
        
    def respawn(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.location = Point(self.dx, self.dy)
        
class Speed:
    def __init__(self):
        self.x = randint(2, 22)
        self.y = randint(2, 22)
        self.location = Point(self.x, self.y)
    
    def draw(self):
        point = self.location
        rect = pygame.Rect(BLOCK_SIZE * point.x, BLOCK_SIZE * point.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, (255, 255, 0), rect)

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.location = Point(self.x, self.y)
        
    def draw(self):
        point = self.location
        rect = pygame.Rect(BLOCK_SIZE * point.x, BLOCK_SIZE * point.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, (0, 0, 255), rect)

        
        

class Snake:
    def __init__(self):
        self.body = [Point(10, 11)]
        self.dx = 0
        self.dy = 0

    def move(self):    
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i-1].x
            self.body[i].y = self.body[i-1].y

        self.body[0].x += self.dx 
        self.body[0].y += self.dy 

        if self.body[0].x * BLOCK_SIZE > WIDTH:
            self.body[0].x = 0
        
        if self.body[0].y * BLOCK_SIZE > HEIGHT:
            self.body[0].y = 0

        if self.body[0].x < 0:
            self.body[0].x = WIDTH / BLOCK_SIZE
        
        if self.body[0].y < 0:
            self.body[0].y = HEIGHT / BLOCK_SIZE

    def draw(self):
        point = self.body[0]
        rect = pygame.Rect(BLOCK_SIZE * point.x, BLOCK_SIZE * point.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, (255, 0, 0), rect)


        for point in self.body[1:]:
            rect = pygame.Rect(BLOCK_SIZE * point.x, BLOCK_SIZE * point.y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, (0, 255, 0), rect)

    def check_collision(self, food, block, speeds):
        if self.body[0].x == food.location.x:
            if self.body[0].y == food.location.y:
                global SCORE, count
                count = 0
                
                SCORE+=randint(1, 3)
                self.body.append(Point(food.location.x, food.location.y))
                if food.location.x != block.x and food.location.y != block.y:
                    food.location.x, food.location.y = randint(2, 22), randint(2, 22)
        if self.body[0].x == speeds.location.x:
            if self.body[0].y == speeds.location.y:
                global LEVEL, FPS, level
                level+=1
                level%=2
                LEVEL+=1
                if speeds.location.x != block.x and speeds.location.y != block.y:
                    speeds.location.x, speeds.location.y = randint(2, 22), randint(2, 22)
restart = True

def drawGrid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, LINE_COLOR, rect, 1)
            
level = 0
LEVEL = 0
SCORE = 0


while restart:
    global SCREEN, FPS
    SCREEN = pygame.display.set_mode((WIDTHSCREEN, HEIGHT))
    pygame.display.set_caption("Snake")
    CLOCK = pygame.time.Clock()
    FPS = 5
    DICT = {}
    count = 0
    block = Block(0, 0)
    snake = Snake()
    food = Food(randint(1, 25), randint(1, 25))
    speeds = Speed()
    running = True
    lose = False
    while running: 
        CLOCK.tick(FPS)
        SCREEN.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                restart = not restart
                running = not running
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                snake.dx = 1
                snake.dy = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                snake.dx = -1
                snake.dy = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = 1


        wallsCoor = open(f"level{level}.txt", 'r').readlines()
        walls = []
        for i, line in enumerate(wallsCoor):
            for j, each in enumerate(line):
                if each == "#":
                    walls.append(Block(j, i))
        
        
        drawGrid()
        for block in walls:
            block.draw()
            if snake.body[0].x == block.x and snake.body[0].y == block.y:
                restart = not restart
                running = not running
            if food.x != block.x and food.y != block.y:
                food.draw()
            if SCORE >= 5 and level != 1:
                if speeds.x != block.x and speeds.y != block.y:
                    speeds.draw()
        
        
        
            
        
            
        snake.move()

        snake.check_collision(food, block, speeds)
        snake.draw()
        
        if SCORE > 0 and SCORE % 5 == 0:
            SCORE+=1
            LEVEL+=1
            FPS+=5
            
        count += (FPS % 3)
        if count % 100 == 0 and count > 0:
            food.respawn(randint(2, 22), randint(2, 22))
        
        #Text------------------------------
        score_img = font.render(f"{SCORE}", True, BLACK)
        coins_cnt = font.render(f"{LEVEL}", False, False)
        SCREEN.blit(font.render(f"SCORE", True, BLACK), (565, 25))
        SCREEN.blit(font.render("LEVEL", True, BLACK), (570, 135))
        SCREEN.blit(score_img, score_img.get_rect(center=(600, 65)))
        SCREEN.blit(coins_cnt, coins_cnt.get_rect(center=(600, 170)))
        

        pygame.display.flip()
    pygame.display.flip()
pygame.quit()