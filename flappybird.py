import pygame
import random
pygame.init()


BIRD_WIDTH,BIRD_HEIGHT = 70,50
SPACING = 300
class bird(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y

        #Loading and scaling image
        self.img = pygame.image.load('flappybird.png')
        self.img = pygame.transform.scale(self.img,(BIRD_WIDTH,BIRD_HEIGHT))
        self.imgRect = self.img.get_rect()
        #Roatted images
        self.imgUP =pygame.transform.rotate(self.img, 30)
        self.imgDown = pygame.transform.rotate(self.img, -30)

        self.isFlapping = False
        self.isAlive = True

    def draw_bird(self):
        if self.isFlapping:
            self.img = self.imgUP
        else:
            self.img = self.imgDown

        self.imgRect = self.img.get_rect()
        self.imgRect.center = (self.x, self.y)
        win.blit(self.img, self.imgRect)

class pipe(object):
    def __init__(self,x):
        self.x=x
        self.y = random.randint(300,HEIGHT-GROUND_HEIGHT-100)
        self.width = 100
        self.height = 535
        self.pipeDown = pygame.image.load('pipeDown.png')
        self.pipeDown = pygame.transform.scale(self.pipeDown,(self.width,self.height))
        self.pipeUP = pygame.image.load('pipeUp.png')
        self.pipeUP = pygame.transform.scale(self.pipeUP,(self.width,self.height))
        self.GAP = 200
        self.passed = False

    def draw_pipe(self):
        win.blit(self.pipeDown,(self.x,self.y))
        win.blit(self.pipeUP,(self.x,self.y-self.GAP-self.height))





def draw_ground():
    #draws moving ground
    global ground_x
    if flappybird.isAlive:
        ground_x-=moving_speed

    win.blit(ground, (ground_x, HEIGHT - GROUND_HEIGHT))
    #if ground is out of screen it will draw another one at the end
    if ground_x<0:
        win.blit(ground,(WIDTH-ground_x*(-1),HEIGHT - GROUND_HEIGHT))

    #if the end of the picture is off the screen, draw it at x = zero
    if ground_x<=-WIDTH:
        ground_x=0


def check_colision():
    #checks collision between bird and pipes
    for p in pipes:
        if flappybird.x+BIRD_WIDTH//2 >= p.x and flappybird.x+BIRD_WIDTH//2<=p.x+p.width:
            if flappybird.y-BIRD_HEIGHT//2 <= p.y-p.GAP or  flappybird.y+BIRD_HEIGHT//2 >=p.y:
                flappybird.isAlive =False

def update_score():
    global  score
    for p in pipes:
        if flappybird.x > p.x+p.width and p.passed == False:
            score +=1
            p.passed=True
    text= font.render(str(score),True,(255,255,255))
    win.blit(text,(WIDTH//2,50))

def move_pipes():
    for p in pipes:
        p.x-=moving_speed

    #checks if pipe is out of the screen, if it is, it will put it behind the last one and change positions in list
    #1 -> 0; 2 -> 1; 0 -> 2
    if pipes[0].x+pipes[0].width<=0:
        pipes[0].x = pipes[len(pipes)-1].x+SPACING
        temp = pipes[0]
        for i in range(1,len(pipes)):
            pipes[i-1]=pipes[i]

        pipes[len(pipes)-1]=temp
        #Changes passed parameter so it can count again for score
        pipes[len(pipes)-1].passed = False


def draw_pipes():
    for p in pipes:
        p.draw_pipe()

def draw_play():
    text = ["Press","Space","To","Play"]
    counter = 0
    for t in text:
        rend =big_font.render(t,True,(255,255,255))
        rendRect = rend.get_rect()
        rendRect.center = (WIDTH//2,150+counter*150)
        win.blit(rend,rendRect)
        counter+=1

def start():
    global pipes,score,flappybird,bird_y
    flappybird.isAlive = True
    pipes = []
    pipes.append(pipe(1000))
    pipes.append(pipe(pipes[0].x + SPACING))
    pipes.append(pipe(pipes[1].x + SPACING))
    score = 0
    flappybird.y = HEIGHT//2-100
    bird_y=flappybird.y

#background
background = pygame.image.load('background.png')

#ground
ground = pygame.image.load('ground.png')
GROUND_HEIGHT = 95
ground_x=0

#Window settings
WIDTH,HEIGHT = 500,750
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird")
font = pygame.font.Font('FlappyBirdFont.ttf',50)
big_font = pygame.font.Font('FlappyBirdFont.ttf',200)

#bird initalization
bird_x,bird_y = WIDTH//2,HEIGHT//2
flappybird = bird(bird_x,bird_y)

#vel - speed of the bird falling, moving speed - speed of pipes and ground
vel = 10
moving_speed = vel//2


score = 0
clock = pygame.time.Clock()

#number of flapps, same as jump height
flapp_count =6

#list of pipes
pipes=[]
start()
flappybird.isAlive = False
run=True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and flappybird.isAlive:
                flappybird.isFlapping = True


    if flappybird.isFlapping:
        if flapp_count>0 and bird_y > 0 + BIRD_HEIGHT // 2:
            bird_y-=(flapp_count**2)//3
            flapp_count -= 1
        else:
            flappybird.isFlapping=False
            flapp_count=10
    else:
        if bird_y < HEIGHT-BIRD_HEIGHT//2-GROUND_HEIGHT:
            bird_y+=vel
        elif bird_y >= HEIGHT-BIRD_HEIGHT//2-GROUND_HEIGHT:
            flappybird.isAlive = False


    flappybird.y=bird_y

    win.blit(background,(0,0))
    draw_pipes()
    flappybird.draw_bird()

    if flappybird.isAlive:
        check_colision()
        move_pipes()
        update_score()

    draw_ground()

    while(flappybird.isAlive==False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flappybird.isAlive=True
                run=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start()

        draw_play()
        pygame.display.update()

    pygame.display.update()

    clock.tick(40)

pygame.quit()