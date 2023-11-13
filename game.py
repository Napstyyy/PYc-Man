import pygame
from board import boards
import math
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.__WIDTH = 900
        self.__HEIGHT = 950
        self.screen = pygame.display.set_mode([self.__WIDTH, self.__HEIGHT])
        self.timer = pygame.time.Clock()
        self.fps = 60
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.level = boards
        self.color = 'blue'
        self.PI = math.pi
        self.player = Player(450, 663)
        self.flicker = False
        self.turns_allowed = [False, False, False, False]
        self.score = 0
        self.powerUp = True
        self.powerCount = 0
        self.eatenGhosts = [False, False, False, False]
        self.moving = False
        self.startUpCounter = 0

    def draw_misc(self):
        score_text = self.font.render(f'Score: {self.score}', True, 'white')
        self.screen.blit(score_text, (10, 920))

    def check_collisions(self, centerX, centerY):
        num1 = ((self.__HEIGHT - 50) // 32)
        num2 = (self.__WIDTH // 30)
        if 0 < self.player.x < 870:
            if self.level[centerY // num1][centerX // num2] == 1:
                self.level[centerY // num1][centerX // num2] = 0
                self.score += 10
            if self.level[centerY // num1][centerX // num2] == 2:
                self.level[centerY // num1][centerX // num2] = 0
                self.score += 50
                self.powerUp = True
                self.powerCount = 0
                self.eatenGhosts = [False, False, False, False]               
        return self.score
    
    def draw_board(self):
        num1 = ((self.__HEIGHT - 50) // 32)
        num2 = (self.__WIDTH // 30)

        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                if self.level[i][j] == 1:
                    pygame.draw.circle(self.screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
                elif self.level[i][j] == 2 and not self.flicker:
                    pygame.draw.circle(self.screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
                elif self.level[i][j] == 3:
                    pygame.draw.line(self.screen, self.color, (j * num2 + (0.5 * num2), i * num1),
                                     (j * num2 + (0.5 * num2), i * num1 + num1), 3)
                elif self.level[i][j] == 4:
                    pygame.draw.line(self.screen, self.color, (j * num2, i * num1 + (0.5 * num1)),
                                     (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
                elif self.level[i][j] == 5:
                    pygame.draw.arc(self.screen, self.color, [(j * num2 - (num2 * 0.4)) - 2, i * num1 + (0.5 * num1),
                                                               num2, num1], 0, self.PI / 2, 3)
                elif self.level[i][j] == 6:
                    pygame.draw.arc(self.screen, self.color, [(j * num2 + (num2 * 0.6)) - 3, i * num1 + (0.5 * num1),
                                                               num2, num1], self.PI / 2, self.PI, 3)
                elif self.level[i][j] == 7:
                    pygame.draw.arc(self.screen, self.color, [(j * num2 + (num2 * 0.5)), i * num1 - (0.4 * num1),
                                                               num2, num1], self.PI, 3 * self.PI / 2, 3)
                elif self.level[i][j] == 8:
                    pygame.draw.arc(self.screen, self.color, [(j * num2 - (num2 * 0.4)) - 2, i * num1 - (0.4 * num1),
                                                               num2, num1], 3 * self.PI / 2, 2 * self.PI, 3)
                elif self.level[i][j] == 9:
                    pygame.draw.line(self.screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                     (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

    def check_position(self, centerX, centerY):
        turns = [False, False, False, False]
        num1 = (self.__HEIGHT - 50) // 32
        num2 = (self.__WIDTH // 30)
        num3 = 15

        if centerX // 30 < 29:
            if self.player.direction == 0:
                if self.level[centerY // num1][(centerX - num3) // num2] < 3:
                    turns[1] = True
            if self.player.direction == 1:
                if self.level[centerY // num1][(centerX + num3) // num2] < 3:
                    turns[0] = True
            if self.player.direction == 2:
                if self.level[(centerY + num3) // num1][centerX // num2] < 3:
                    turns[3] = True
            if self.player.direction == 3:
                if self.level[(centerY - num3) // num1][centerX // num2] < 3:
                    turns[2] = True

            if self.player.direction == 2 or self.player.direction == 3:
                if 12 <= centerX % num2 <= 18:
                    if self.level[(centerY + num3) // num1][centerX // num2] < 3:
                        turns[3] = True
                    if self.level[(centerY - num3) // num1][centerX // num2] < 3:
                        turns[2] = True
                if 12 <= centerY % num1 <= 18:
                    if self.level[centerY // num1][(centerX - num2) // num2] < 3:
                        turns[1] = True
                    if self.level[centerY // num1][(centerX + num2) // num2] < 3:
                        turns[0] = True

            if self.player.direction == 0 or self.player.direction == 1:
                if 12 <= centerX % num2 <= 18:
                    if self.level[(centerY + num3) // num1][centerX // num2] < 3:
                        turns[3] = True
                    if self.level[(centerY - num3) // num1][centerX // num2] < 3:
                        turns[2] = True
                if 12 <= centerY % num1 <= 18:
                    if self.level[centerY // num1][(centerX - num3) // num2] < 3:
                        turns[1] = True
                    if self.level[centerY // num1][(centerX + num3) // num2] < 3:
                        turns[0] = True
        else:
            turns[0] = True
            turns[1] = True
        return turns

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.direction_command = 0
                elif event.key == pygame.K_LEFT:
                    self.player.direction_command = 1
                elif event.key == pygame.K_UP:
                    self.player.direction_command = 2
                elif event.key == pygame.K_DOWN:
                    self.player.direction_command = 3
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and self.player.direction_command == 0:
                    self.player.direction_command = self.player.direction
                elif event.key == pygame.K_LEFT and self.player.direction_command == 1:
                    self.player.direction_command = self.player.direction
                elif event.key == pygame.K_UP and self.player.direction_command == 2:
                    self.player.direction_command = self.player.direction
                elif event.key == pygame.K_DOWN and self.player.direction_command == 3:
                    self.player.direction_command = self.player.direction
                    
        for i in range(4):
            if  self.player.direction_command == i and  self.turns_allowed[i]:
                self.player.direction = i
                
        if self.player.x > 900:
            self.player.x = -47
        elif self.player.x < -50:
            self.player.x = 897
            
        return True

    def run_game(self):
        run = True
        while run:
            self.timer.tick(self.fps)
            
            if self.player.counter < 19:
                self.player.counter += 1
                if self.player.counter > 3:
                    self.flicker = False
            else:
                self.player.counter = 0
                self.flicker = True
                
            if self.powerUp and self.powerCount < 600:
                self.powerCount += 1
            elif self.powerUp and self.powerCount >= 600:
                self.powerCount = 0
                self.powerUp = False
                self.eatenGhosts = [False, False, False, False]
                
            if self.startUpCounter < 180:
                self.moving = False
                self.startUpCounter += 1
            else:
                self.moving = True
                
            
            self.screen.fill('black')
            self.draw_board()
            self.player.draw(self.screen)
            self.draw_misc()
            centerX = self.player.x + 23
            centerY = self.player.y + 24
            self.turns_allowed = self.check_position(centerX, centerY)
            if self.moving:
                self.player.x, self.player.y = self.player.move_player(self.turns_allowed)
            self.score = self.check_collisions(centerX, centerY)

            run = self.handle_events()

            pygame.display.flip()

        pygame.quit()
        


if __name__ == "__main__":
    game = Game()
    game.run_game()
