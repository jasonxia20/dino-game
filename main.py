import pygame
import os

pygame.init()

SCRN_HEIGHT = 600
SCRN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCRN_WIDTH,SCRN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")), \
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = [pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))]
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),\
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

S_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")), \
            pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")), \
            pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
L_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")), \
            pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")), \
            pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),\
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = [pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))]
BG = [pygame.image.load(os.path.join("Assets/Other", "Track.png"))]

class Dinosaur:
    xpos = 18
    ypos = 310

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.xpos
        self.dino_rect.y = self.ypos

    def update(self, user_input):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0
        
        if user_input[pygame.K_UP] and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
            self.dino_duck = False
        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_duck or user_input[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
        
    def duck(self):
        pass

    def run(self):
        print(self.step_index//5)
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.xpos
        self.dino_rect.y = self.ypos
        self.step_index += 1

    def jump(self):
        pass

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

def main():
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        SCREEN.fill((255,255,255))
        usr_inpt = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(usr_inpt)

        clock.tick(30)
        pygame.display.update()
    

main()