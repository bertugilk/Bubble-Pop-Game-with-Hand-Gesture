import cv2
import numpy as np
import time
import HandTrackingModule as htm
import pygame
import sys
import random

pygame.init()
screen_width,screen_height=648,480
screen = pygame.display.set_mode((screen_width, screen_height))

red_bubble=pygame.image.load("images/red.png")
rect_red_bubble=red_bubble.get_rect()
rect_red_bubble.x,rect_red_bubble.y = 250, 10

aqua_bubble=pygame.image.load("images/aqua.png")
rect_aqua_bubble=aqua_bubble.get_rect()
rect_aqua_bubble.x,rect_aqua_bubble.y = 250, 10

orange_bubble=pygame.image.load("images/orange.png")
rect_orange_bubble=orange_bubble.get_rect()
rect_orange_bubble.x,rect_orange_bubble.y = 250, 10

wCam, hCam = 800, 600
camera = cv2.VideoCapture(0)
camera.set(3, wCam)
camera.set(4, hCam)
pTime = 0
score=0
elapsed_time=60
block_size=10
clock=pygame.time.Clock()
game=True
random_num = random.randint(1, 3)
life=5

detector = htm.HandDetector(detectionCon=0.8,maxHands=1)

pop_sound=pygame.mixer.Sound("music/pop.mp3")

def write(message, color, x, y, size):
    message = message
    color = color
    x = x
    y = y
    size = size
    font = pygame.font.SysFont(None, size)
    text = font.render(message, True, color)
    screen.blit(text, [x, y])

def finishScreen():
    bg=pygame.image.load("images/bg.jpg")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill((0, 0, 0))
        screen.blit(bg,(0,0))
        write("Your score is: " + str(int(score)), (0,0,0), 200, 300, 60)
        pygame.display.update()

def popRedBubble():
    rect_red_bubble.x=random.randint(50,img.shape[1]-348)
    rect_red_bubble.y=img.shape[0]-450
def popAquaBubble():
    rect_aqua_bubble.x=random.randint(50,img.shape[1]-348)
    rect_aqua_bubble.y=img.shape[0]-450
def popOrangeBubble():
    rect_orange_bubble.x=random.randint(50,img.shape[1]-348)
    rect_orange_bubble.y=img.shape[0]-450

while game:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    success, img = camera.read()
    img=cv2.flip(img,1)

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x, y = lmList[8][1], lmList[8][2]
        cv2.circle(img, (x, y), 12, (255, 0, 255), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    elapsed_time-=0.1
    if elapsed_time <= 0:
        elapsed_time=0

    cv2.putText(img, f'Score: {int(score)}', (10, 70), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 0, 0), 2)
    cv2.putText(img, f'Elapsed Time: {int(elapsed_time)}', (10, 110), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 255), 2)
    cv2.putText(img, f'Fps: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 0.6, (25, 130, 50), 2)
    cv2.putText(img, f'Life: {int(life)}', (10, 150), cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 20, 147), 2)

    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    imgRGB=np.rot90(imgRGB)
    frame=pygame.surfarray.make_surface(imgRGB).convert()
    frame=pygame.transform.flip(frame,True,False)

    if len(lmList) != 0:
        x, y = lmList[8][1], lmList[8][2]
        if rect_red_bubble.collidepoint(x,y):
            popRedBubble()
            pop_sound.play()
            score+=10
            random_num = random.randint(1, 3)
        if rect_aqua_bubble.collidepoint(x,y):
            popAquaBubble()
            pop_sound.play()
            score+=20
            random_num = random.randint(1, 3)
        if rect_orange_bubble.collidepoint(x,y):
            popOrangeBubble()
            pop_sound.play()
            score+=30
            random_num = random.randint(1, 3)

    if rect_red_bubble.y >= 400 and random_num == 1:
        popRedBubble()
        score-=30
        if score<=0:
            score=0
        life-=1
        if life <= 0:
            life = 0
            game = False
            if game == False:
                finishScreen()
        random_num = random.randint(1, 3)
    if rect_aqua_bubble.y >= 400 and random_num == 2:
        popAquaBubble()
        score -= 40
        if score <= 0:
            score = 0
        life -= 1
        if life <= 0:
            life = 0
            game = False
            if game == False:
                finishScreen()
        random_num = random.randint(1, 3)
    if rect_orange_bubble.y >= 400 and random_num == 3:
        popOrangeBubble()
        score -= 50
        if score <= 0:
            score = 0
        life -= 1
        if life <= 0:
            life=0
            game = False
            if game == False:
                finishScreen()
        random_num = random.randint(1, 3)

    screen.blit(frame,(0,0))

    if random_num==1:
        rect_red_bubble.y += 10
        screen.blit(red_bubble,rect_red_bubble)
    if random_num==2:
        rect_aqua_bubble.y += 12
        screen.blit(aqua_bubble, rect_aqua_bubble)
    if random_num==3:
        rect_orange_bubble.y += 14
        screen.blit(orange_bubble, rect_orange_bubble)

    if elapsed_time <= 0:
        elapsed_time = 0
        game = False
        if game == False:
            finishScreen()

    pygame.draw.rect(screen, [255, 0, 0], [0, 430, 700, 50])

    pygame.display.flip()
    pygame.display.update()

camera.release()
cv2.destroyAllWindows()