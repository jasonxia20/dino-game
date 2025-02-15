import pygame
import os
import random

pygame.init()

SCRN_HEIGHT = 600
SCRN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCRN_WIDTH,SCRN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("dino-game/Assets/Dino", "DinoRun1.png")), \
           pygame.image.load(os.path.join("dino-game/Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("dino-game/Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("dino-game/Assets/Dino", "DinoDuck1.png")),\
           pygame.image.load(os.path.join("dino-game/Assets/Dino", "DinoDuck2.png"))]

S_CACTUS = [pygame.image.load(os.path.join("dino-game/Assets/Cactus", "SmallCactus1.png")), \
            pygame.image.load(os.path.join("dino-game/Assets/Cactus", "SmallCactus2.png")), \
            pygame.image.load(os.path.join("dino-game/Assets/Cactus", "SmallCactus3.png"))]
L_CACTUS = [pygame.image.load(os.path.join("dino-game/Assets/Cactus", "LargeCactus1.png")), \
            pygame.image.load(os.path.join("dino-game/Assets/Cactus", "LargeCactus2.png")), \
            pygame.image.load(os.path.join("dino-game/Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("dino-game/Assets/Bird", "Bird1.png")),\
        pygame.image.load(os.path.join("dino-game/Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("dino-game/Assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("dino-game/Assets/Other", "Track.png"))

class Dinosaur:
    xpos = 18
    ypos = 310
    yposduck = 340
    jumpvel = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.jumpvel
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
            #print("goodbye")
            self.dino_jump = True
            self.dino_run = False
            self.dino_duck = False
        elif user_input[pygame.K_DOWN] and not self.dino_jump:
            #print('ducking')
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_duck or user_input[pygame.K_DOWN]) and not self.dino_jump or not user_input[pygame.K_DOWN] and not self.dino_jump:
            #print("hello")
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False
        
    def duck(self):
        #print(self.step_index//5)
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.xpos
        self.dino_rect.y = self.yposduck
        self.step_index += 1

    def run(self):
        #print(self.step_index//5)
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.xpos
        self.dino_rect.y = self.ypos
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        if self.jump_vel < -self.jumpvel:
            self.dino_jump = False
            self.jump_vel = self.jumpvel

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class cloud:
    def __init__(self):
        self.x = SCRN_WIDTH + random.randint(800, 1000)
        self.y = random.randint (50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self, bonus, y1, y2):
        self.x -=(gamespeed + bonus)
        if self.x < -self.width:
            self.x = SCRN_WIDTH + random.randint(100, 1500)
            self.y = random.randint (y1, y2)
        
        y = self.y
        self.y = random.randint (50, 100)
        self.y = y
        
    
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class obstacles:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCRN_WIDTH

    def update(self):
        self.rect.x -= gamespeed
        if self.rect.x <= -self.rect.width:
            obstacle.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class smallcacti(obstacles):
    def __init__(self, image):
        self.type= random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 325

class largecacti(obstacles):
    def __init__(self, image):
        self.type= random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 300

class bird(obstacles):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0

        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


def main():
    global gamespeed, xposbg, yposbg, points, obstacle, font
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    Cloud = cloud()
    Cloud2 = cloud()
    Cloud3 = cloud()
    gamespeed = 14
    xposbg = 0
    yposbg = 380
    points = 0
    font = pygame.font.Font("freesansbold.ttf", 20)
    obstacle = []
    deathcount = 0

    def score():
        global gamespeed, points
        points += 1

        if points % 100 == 0:
            gamespeed += 1

        text = font.render("Points: " + str(points), True, (0,0,0))
        textrect = text.get_rect()
        textrect.center = (1000,40)
        SCREEN.blit(text, textrect)

    def background():
        global xposbg, yposbg
        imagewidth = BG.get_width()
        SCREEN.blit(BG, (xposbg,yposbg))
        SCREEN.blit(BG, (imagewidth+ xposbg,yposbg))
        if xposbg <= -imagewidth:
            SCREEN.blit(BG, (imagewidth +xposbg, yposbg))
            xposbg = 0
        xposbg -= gamespeed


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        SCREEN.fill((255,255,255))
        usr_inpt = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(usr_inpt)
        usr_inpt = False

        if len(obstacle) == 0:
            if random.randint(0,2) == 0:
                obstacle.append(smallcacti(S_CACTUS))
            elif random.randint(0,2) == 1:
                obstacle.append(bird(BIRD))
            elif random.randint(0,2) == 2:
                obstacle.append(largecacti(L_CACTUS))
        
        for item in obstacle:
            item.draw(SCREEN)
            item.update()
            if player.dino_rect.colliderect(item.rect):
                #pygame.draw.rect(SCREEN, (255,0,0), player.dino_rect, 2)
                pygame.time.delay(2000)
                deathcount += 1
                menu(deathcount)

        background()
        score()

        Cloud.draw(SCREEN)
        Cloud.update(0, 50, 100)

        Cloud2.draw(SCREEN)
        Cloud2.update(6, 70, 120)

        Cloud3.draw(SCREEN)
        Cloud3.update(-3, 25, 75)

        clock.tick(30)
        pygame.display.update()

#main()

def menu(deathcount):
    global points
    run = True
    font = pygame.font.Font("freesansbold.ttf", 20)
    while run:
        SCREEN.fill((255,255,255))
        if deathcount == 0:
            text = font.render("Press any key to start", True, (0,0,0))
        elif deathcount > 0:
            text = font.render("Press any key to restart", True, (0,0,0))
            score = font.render(f"Your score: {str(points)}", True, (0,0,0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCRN_WIDTH // 2, SCRN_HEIGHT // 2 +50)
            SCREEN.blit(score, scoreRect)

        textrect = text.get_rect()
        textrect.center = (SCRN_WIDTH // 2, SCRN_HEIGHT // 2)
        SCREEN.blit(text, textrect)
        SCREEN.blit(RUNNING[0], (SCRN_WIDTH //2 -20, SCRN_HEIGHT // 2 -140))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()

            
menu(deathcount=0)