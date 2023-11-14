import pygame
from board import boards
import math
from player import Player
from ghosts import *

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
        #Caracters --------------------------------------
        self.player = Player(450, 663)
        self.blinky = blinky()
        self.pinky = pinky()
        self.inky = inky()
        self.clyde = clyde()
        self.spooked = spooked()
        self.dead = deadGhost()
        # ------------------------------------------
        self.flicker = False
        self.turns_allowed = [False, False, False, False]
        self.score = 0
        self.powerUp = False
        self.powerCount = 0
        self.eatenGhosts = [False, False, False, False]
        self.ghost_speeds = [2, 2, 2, 2]
        self.targets = [(self.player.x, self.player.y), (self.player.x, self.player.y), (self.player.x, self.player.y), (self.player.x, self.player.y)]
        self.moving = False
        self.startUpCounter = 0
        self.game_over = False

    def draw_misc(self):
        score_text = self.font.render(f'Score: {self.score}', True, 'white')
        self.screen.blit(score_text, (10, 920))
        if self.powerUp:
            pygame.draw.circle(self.screen, 'blue', (140, 930), 15)
        for i in range(self.player.lives):
            self.screen.blit(pygame.transform.scale(self.player.images[0], (30, 30)), (650 + i * 40, 915))

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
        return self.score, self.powerUp, self.powerCount, self.eatenGhosts
    
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

    def get_targets(self, blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
        if self.player.x < 450:
            runaway_x = 900
        else:
            runaway_x = 0
        if self.player.y < 450:
            runaway_y = 900
        else:
            runaway_y = 0
        return_target = (380, 400)
        if self.powerUp:
            if not self.blinky.dead and not self.eatenGhosts[0]:
                blink_target = (runaway_x, runaway_y)
            elif not self.blinky.dead and self.eatenGhosts[0]:
                if 340 < blink_x < 560 and 340 < blink_y < 500:
                    blink_target = (400, 100)
                else:
                    blink_target = (self.player.x, self.player.y)
            else:
                blink_target = return_target
            if not self.inky.dead and not self.eatenGhosts[1]:
                ink_target = (runaway_x, self.player.y)
            elif not self.inky.dead and self.eatenGhosts[1]:
                if 340 < ink_x < 560 and 340 < ink_y < 500:
                    ink_target = (400, 100)
                else:
                    ink_target = (self.player.x, self.player.y)
            else:
                ink_target = return_target
            if not self.pinky.dead and not self.eatenGhosts[2]:
                pink_target = (self.player.x, runaway_y)
            elif not self.pinky.dead and self.eatenGhosts[2]:
                if 340 < pink_x < 560 and 340 < pink_y < 500:
                    pink_target = (400, 100)
                else:
                    pink_target = (self.player.x, self.player.y)
            else:
                pink_target = return_target
            if not self.clyde.dead and self.eatenGhosts[3]:
                clyd_target = (450, 450)
            elif not self.clyde.dead and self.eatenGhosts[3]:
                if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                    clyd_target = (400, 100)
                else:
                    clyd_target = (self.player.x, self.player.y)
            else:
                clyd_target = return_target
        else:
            if not self.blinky.dead:
                if 340 < blink_x < 560 and 340 < blink_y < 500:
                    blink_target = (400, 100)
                else:
                    blink_target = (self.player.x, self.player.y)
            else:
                blink_target = return_target
            if not self.inky.dead:
                if 340 < ink_x < 560 and 340 < ink_y < 500:
                    ink_target = (400, 100)
                else:
                    ink_target = (self.player.x, self.player.y)
            else:
                ink_target = return_target
            if not self.pinky.dead:
                if 340 < pink_x < 560 and 340 < pink_y < 500:
                    pink_target = (400, 100)
                else:
                    pink_target = (self.player.x, self.player.y)
            else:
                pink_target = return_target
            if not self.clyde.dead:
                if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                    clyd_target = (400, 100)
                else:
                    clyd_target = (self.player.x, self.player.y)
            else:
                clyd_target = return_target
        return [blink_target, ink_target, pink_target, clyd_target]
            
            

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
            centerX = self.player.x + 23
            centerY = self.player.y + 24
            if self.powerUp:
                self.ghost_speeds = [1, 1, 1, 1]
            else:
                self.ghost_speeds = [2, 2, 2, 2]
            if self.eatenGhosts[0]:
                self.ghost_speeds[0] = 2
            if self.eatenGhosts[1]:
                self.ghost_speeds[1] = 2
            if self.eatenGhosts[2]:
                self.ghost_speeds[2] = 2
            if self.eatenGhosts[3]:
                self.ghost_speeds[3] = 2   
            if self.blinky.dead:
                self.ghost_speeds[0] = 4
            if self.inky.dead:
                self.ghost_speeds[1] = 4
            if self.pinky.dead:
                self.ghost_speeds[2] = 4
            if self.clyde.dead:
                self.ghost_speeds[3] = 4
                    
            player_circle = pygame.draw.circle(self.screen, 'black', (centerX, centerY), 20, 2)
            self.player.draw(self.screen)
            Blinky = Ghost(self.blinky.x, self.blinky.y, self.targets[0], self.ghost_speeds[0], self.blinky.img, self.blinky.direction, self.blinky.dead, self.blinky.box, 0, self.__WIDTH, self.__HEIGHT, self.level, self.screen, self.powerUp, self.eatenGhosts)
            Inky = Ghost(self.inky.x, self.inky.y, self.targets[1], self.ghost_speeds[1], self.inky.img, self.inky.direction, self.inky.dead, self.inky.box, 1, self.__WIDTH, self.__HEIGHT, self.level, self.screen, self.powerUp, self.eatenGhosts)
            Pinky = Ghost(self.pinky.x, self.pinky.y, self.targets[2], self.ghost_speeds[2], self.pinky.img, self.pinky.direction, self.pinky.dead, self.pinky.box, 2, self.__WIDTH, self.__HEIGHT, self.level, self.screen, self.powerUp, self.eatenGhosts)
            Clyde = Ghost(self.clyde.x, self.clyde.y, self.targets[3], self.ghost_speeds[3], self.clyde.img, self.clyde.direction, self.clyde.dead, self.clyde.box, 3, self.__WIDTH, self.__HEIGHT, self.level, self.screen, self.powerUp, self.eatenGhosts)
            
            self.draw_misc()
            self.targets = self.get_targets(self.blinky.x, self.blinky.y, self.inky.x, self.inky.y, self.pinky.x, self.pinky.y, self.clyde.x, self.clyde.y)
            self.turns_allowed = self.check_position(centerX, centerY)
            if self.moving:
                self.player.x, self.player.y = self.player.move_player(self.turns_allowed)
                if not Blinky.dead and not Blinky.in_box:
                    self.blinky.x, self.blinky.y, self.blinky.direction = Blinky.move_blinky()
                else:
                    self.blinky.x, self.blinky.y, self.blinky.direction = Blinky.move_clyde()
                if not Pinky.dead and not Pinky.in_box:
                    self.pinky.x, self.pinky.y, self.pinky.direction = Pinky.move_pinky()
                else:
                    self.pinky.x, self.pinky.y, self.pinky.direction = Pinky.move_clyde()
                if not Inky.dead and not Inky.in_box:
                    self.inky.x, self.inky.y, self.inky.direction = Inky.move_inky()
                else:
                    self.inky.x, self.inky.y, self.inky.direction = Inky.move_clyde()
                self.clyde.x, self.clyde.y, self.clyde.direction = Clyde.move_clyde()
            self.score, self.powerUp, self.powerCount, self.eatenGhosts = self.check_collisions(centerX, centerY)

            if not self.powerUp:
                if (player_circle.colliderect(Blinky.rect) and not Blinky.dead) or (player_circle.colliderect(Inky.rect) and not Inky.dead) or (player_circle.colliderect(Pinky.rect) and not Pinky.dead) or (player_circle.colliderect(Clyde.rect) and not Clyde.dead):
                    if self.player.lives > 0:
                        self.player.lives -= 1
                        self.startUpCounter = 0
                        self.powerUp = False
                        self.powerCount = 0
                        self.player.x = 450
                        self.player.y = 663
                        self.player.direction = 0
                        self.player.direction_command = 0
                        self.blinky.x = 56
                        self.blinky.y = 58
                        self.blinky.direction = 0
                        self.inky.x = 440
                        self.inky.y = 388
                        self.inky.direction = 2
                        self.pinky.x = 440
                        self.pinky.y = 438
                        self.pinky.direction = 2
                        self.clyde.x = 440
                        self.clyde.y = 438
                        self.clyde.direction = 2
                        self.eatenGhosts = [False, False, False, False]
                        self.blinky.dead = False
                        self.inky.dead = False
                        self.clyde.dead = False
                        self.pinky.dead = False
                    else:
                        self.game_over = True
                        self.moving = False
                        self.startUpCounter = 0
                        
                        
            if self.powerUp and player_circle.colliderect(Blinky.rect) and self.eatenGhosts[0] and not self.blinky.dead:
                if self.player.lives > 0:
                    self.player.lives -= 1
                    self.startUpCounter = 0
                    self.powerUp = False
                    self.powerCount = 0
                    self.player.x = 450
                    self.player.y = 663
                    self.player.direction = 0
                    self.player.direction_command = 0
                    self.blinky.x = 56
                    self.blinky.y = 58
                    self.blinky.direction = 0
                    self.inky.x = 440
                    self.inky.y = 388
                    self.inky.direction = 2
                    self.pinky.x = 440
                    self.pinky.y = 438
                    self.pinky.direction = 2
                    self.clyde.x = 440
                    self.clyde.y = 438
                    self.clyde.direction = 2
                    self.eatenGhosts = [False, False, False, False]
                    self.blinky.dead = False
                    self.inky.dead = False
                    self.clyde.dead = False
                    self.pinky.dead = False
                else:
                        self.game_over = True
                        self.moving = False
                        self.startUpCounter = 0
                    
            if self.powerUp and player_circle.colliderect(Inky.rect) and self.eatenGhosts[1] and not self.inky.dead:
                if self.player.lives > 0:
                    self.player.lives -= 2
                    self.startUpCounter = 0
                    self.powerUp = False
                    self.powerCount = 0
                    self.player.x = 450
                    self.player.y = 663
                    self.player.direction = 0
                    self.player.direction_command = 0
                    self.blinky.x = 56
                    self.blinky.y = 58
                    self.blinky.direction = 0
                    self.inky.x = 440
                    self.inky.y = 388
                    self.inky.direction = 2
                    self.pinky.x = 440
                    self.pinky.y = 438
                    self.pinky.direction = 2
                    self.clyde.x = 440
                    self.clyde.y = 438
                    self.clyde.direction = 2
                    self.eatenGhosts = [False, False, False, False]
                    self.blinky.dead = False
                    self.inky.dead = False
                    self.clyde.dead = False
                    self.pinky.dead = False
                else:
                        self.game_over = True
                        self.moving = False
                        self.startUpCounter = 0   
            if self.powerUp and player_circle.colliderect(Pinky.rect) and self.eatenGhosts[2] and not self.pinky.dead:
                if self.player.lives > 0:
                    self.player.lives -= 1
                    self.startUpCounter = 0
                    self.powerUp = False
                    self.powerCount = 0
                    self.player.x = 450
                    self.player.y = 663
                    self.player.direction = 0
                    self.player.direction_command = 0
                    self.blinky.x = 56
                    self.blinky.y = 58
                    self.blinky.direction = 0
                    self.inky.x = 440
                    self.inky.y = 388
                    self.inky.direction = 2
                    self.pinky.x = 440
                    self.pinky.y = 438
                    self.pinky.direction = 2
                    self.clyde.x = 440
                    self.clyde.y = 438
                    self.clyde.direction = 2
                    self.eatenGhosts = [False, False, False, False]
                    self.blinky.dead = False
                    self.inky.dead = False
                    self.clyde.dead = False
                    self.pinky.dead = False
                else:
                    self.game_over = True
                    self.moving = False
                    self.startUpCounter = 0  
                        
            if self.powerUp and player_circle.colliderect(Clyde.rect) and self.eatenGhosts[3] and not self.clyde.dead:
                if self.player.lives > 0:
                    self.player.lives -= 1
                    self.startUpCounter = 0
                    self.powerUp = False
                    self.powerCount = 0
                    self.player.x = 450
                    self.player.y = 663
                    self.player.direction = 0
                    self.player.direction_command = 0
                    self.blinky.x = 56
                    self.blinky.y = 58
                    self.blinky.direction = 0
                    self.inky.x = 440
                    self.inky.y = 388
                    self.inky.direction = 2
                    self.pinky.x = 440
                    self.pinky.y = 438
                    self.pinky.direction = 2
                    self.clyde.x = 440
                    self.clyde.y = 438
                    self.clyde.direction = 2
                    self.eatenGhosts = [False, False, False, False]
                    self.blinky.dead = False
                    self.inky.dead = False
                    self.clyde.dead = False
                    self.pinky.dead = False            
                else:
                    self.game_over = True
                    self.moving = False
                    self.startUpCounter = 0
            
            if self.powerUp and player_circle.colliderect(Blinky.rect) and not self.blinky.dead and not self.eatenGhosts[0]:
                self.blinky.dead = True
                self.eatenGhosts[0] = True
                self.score += (2 ** self.eatenGhosts.count(True)) * 100
            
            if self.powerUp and player_circle.colliderect(Inky.rect) and not self.inky.dead and not self.eatenGhosts[1]:
                self.inky.dead = True
                self.eatenGhosts[1] = True
                self.score += (2 ** self.eatenGhosts.count(True)) * 100
            
            if self.powerUp and player_circle.colliderect(Pinky.rect) and not self.pinky.dead and not self.eatenGhosts[2]:
                self.pinky.dead = True
                self.eatenGhosts[2] = True
                self.score += (2 ** self.eatenGhosts.count(True)) * 100
                
            if self.powerUp and player_circle.colliderect(Clyde.rect) and not self.clyde.dead and not self.eatenGhosts[3]:
                self.clyde.dead = True
                self.eatenGhosts[3] = True
                self.score += (2 ** self.eatenGhosts.count(True)) * 100
            
            run = self.handle_events()

            if Blinky.in_box and self.blinky.dead:
                self.blinky.dead = False
            if Inky.in_box and self.inky.dead:
                self.inky.dead = False
            if Pinky.in_box and self.pinky.dead:
                self.pinky.dead = False
            if Clyde.in_box and self.clyde.dead:
                self.clyde.dead = False
            pygame.display.flip()

        pygame.quit()
        


if __name__ == "__main__":
    game = Game()
    game.run_game()
