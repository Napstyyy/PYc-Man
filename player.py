import pygame

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 0
        self.direction_command = 0
        self.counter = 0
        self.speed = 2
        self.images = [pygame.transform.scale(pygame.image.load(f'assets/PlayerImages/{i}.png'), (45, 45)) for i in range(1, 5)]
    
    def draw(self, screen):
         # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
        if self.direction == 0:
            screen.blit(self.images[self.counter // 5], (self.x, self.y))
        elif self.direction == 1:
            screen.blit(pygame.transform.flip(self.images[self.counter // 5], True, False), (self.x, self.y))
        elif self.direction == 2:
            screen.blit(pygame.transform.rotate(self.images[self.counter // 5], 90), (self.x, self.y))
        elif self.direction == 3:
            screen.blit(pygame.transform.rotate(self.images[self.counter // 5], 270), (self.x, self.y))
    
    def move_player(self, turns_allowed):
        # r, l, u ,d
        if self.direction == 0 and turns_allowed[0]:
            self.x += self.speed
        elif self.direction == 1 and turns_allowed[1]:
            self.x -= self.speed
        if self.direction == 2 and turns_allowed[2]:
            self.y -= self.speed
        elif self.direction == 3 and turns_allowed[3]:
            self.y += self.speed
        return self.x, self.y
            
        