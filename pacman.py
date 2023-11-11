import pygame
from board import boards
import math

pygame.init()

# Environment Variables -------------------------------
WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = boards
color = 'blue'
PI = math.pi
playerImages = []
for i in range(1, 5):
    playerImages.append(pygame.transform.scale(pygame.image.load(f'assets/PlayerImages/{i}.png'), (45, 45)))
playerX = 450
playerY = 663
direction = 0
counter = 0
flicker = False
#-------------------------------

def drawBoard():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            elif level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            elif level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            elif level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            elif level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, i * num1 + (0.5 * num1), num2, num1], 0, PI / 2, 3)
            elif level[i][j] == 6:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.6)) - 3, i * num1 + (0.5 * num1), num2, num1], PI / 2, PI, 3)
            elif level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), i * num1 - (0.4 * num1), num2, num1], PI, 3 * PI / 2, 3)
            elif level[i][j] == 8:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, i * num1 - (0.4 * num1), num2, num1], 3 * PI / 2, 2 * PI, 3)
            elif level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

def drawPlayer():
    # 0-Right, 1-Left, 2-up, 3-down
    match direction:
        case 0:
            screen.blit(playerImages[counter // 5], (playerX, playerY))
        case 1:
            screen.blit(pygame.transform.flip(playerImages[counter // 5], True, False), (playerX, playerY))
        case 2:
            screen.blit(pygame.transform.rotate(playerImages[counter // 5], 90), (playerX, playerY))
        case 3:
            screen.blit(pygame.transform.rotate(playerImages[counter // 5], -90), (playerX, playerY))
            
run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
        
    screen.fill('black')
    drawBoard()
    drawPlayer()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_RIGHT:
                    direction = 0
                case pygame.K_LEFT:
                    direction = 1
                case pygame.K_UP:
                    direction = 2
                case pygame.K_DOWN:
                    direction = 3    
                
        
    pygame.display.flip()
pygame.quit()