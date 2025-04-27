import pygame
import random
import time
import math
import sys

# Initialize pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("RoboEyes")

# Colors
BGCOLOR = (0, 0, 0)  # Black (background)
MAINCOLOR = (72, 216, 232)  # Blueeeeeish (eyes)
REDCOLOR = (255, 0, 0)
GREENCOLOR = (0, 255, 0)



# Mood types
DEFAULT = 0
TIRED = 1
ANGRY = 2
HAPPY = 3
SLEEPY = 4

scaleFactor = 1

# Eye properties
eyeLwidthDefault = 200 * scaleFactor
eyeLheightDefault = 300 * scaleFactor
eyeLwidthCurrent = eyeLwidthDefault
eyeLheightCurrent = eyeLheightDefault
eyeLborderRadiusDefault = 0

eyeRwidthDefault = eyeLwidthDefault
eyeRheightDefault = eyeLheightDefault
eyeRwidthCurrent = eyeRwidthDefault
eyeRheightCurrent = eyeRheightDefault
eyeRborderRadiusDefault = 0

eyeSpaceBetween = 60 * scaleFactor

eyeLxDefault = (screen_width - (eyeLwidthDefault + eyeSpaceBetween + eyeLwidthDefault)) // 2
eyeLyDefault = (screen_height - eyeLheightDefault) // 2
eyeLx = eyeLxDefault
eyeLy = eyeLyDefault

eyeRxDefault = eyeLx + eyeLwidthCurrent + eyeSpaceBetween
eyeRyDefault = eyeLy
eyeRx = eyeRxDefault
eyeRy = eyeRyDefault

moveSteps = 5
stepsDone = 0

eyesClosed = False

moveLTox = eyeLxDefault
moveLToy = eyeLyDefault
moveRTox = eyeRxDefault
moveRToy = eyeRyDefault

LastEyeLx = eyeLxDefault
LastEyeLy = eyeLyDefault
LastEyeRx = eyeRxDefault
LastEyeRy = eyeRyDefault


# For mood expressions
tired = False
angry = False
happy = False
sleepy = False
cyclops = False
eyeL_open = True
eyeR_open = True

# Define FPS
fps = 60
frameInterval = 1 / fps
clock = pygame.time.Clock()

eyesClosed = False
last_blink_time = last_move_time = time.time()

moved = False    

blinking = False

lastMood = DEFAULT

lastUpdateTime = time.time()

def setMood(mood):
    global tired, angry, happy, sleepy
    tired, angry, happy, sleepy = False, False, False, False
    if mood == TIRED:
        tired = True
    elif mood == ANGRY:
        angry = True
    elif mood == HAPPY:
        happy = True
    elif mood == SLEEPY:
        sleepy = True





def blinkClose():
    global eyeLheightCurrent, eyeRheightCurrent,eyeLy, eyeRy
    eyeLheightCurrent = 10 * scaleFactor  # Closed eye
    eyeRheightCurrent = 10 * scaleFactor  # Closed eye
    eyeLy = eyeLy 
    eyeRy = eyeRy 
    
def blinkOpen():
    global eyeLheightCurrent, eyeRheightCurrent,eyeLy, eyeRy
    eyeLheightCurrent = eyeLheightDefault  # Open eye
    eyeRheightCurrent = eyeRheightDefault  # Open eye
    eyeLy = eyeLy 
    eyeRy = eyeRy 

def winkClose():
    global eyeLheightCurrent, eyeRheightCurrent
    if(random.randint(0,1)):
        eyeLheightCurrent = 10 * scaleFactor  # Closed eye
    else:
        eyeRheightCurrent = 10 * scaleFactor # Closed eye
    
def winkOpen():
    global eyeLheightCurrent, eyeRheightCurrent
    if(eyeLheightCurrent < eyeRheightCurrent):
        eyeLheightCurrent = eyeLheightDefault  # Closed eye
    else:
        eyeRheightCurrent = eyeRheightDefault  # Closed eye
        

def moveEyesPos():
    global moveLTox,moveLToy, moveRTox,moveRToy
    
    movex = random.randint(0, 400)
    if(random.randint(0,1)):
        movex = -movex
    
    movey = random.randint(0, 200)
    if(random.randint(0,1)):
        movey = -movey
    

    moveLTox = eyeLx + movex
    moveLToy = eyeLy + movey

    moveRTox = eyeRx + movex
    moveRToy = eyeRy + movey

def moveEyesHomePos():
    global moveLTox,moveLToy, moveRTox,moveRToy

    moveLTox = eyeLxDefault
    moveLToy = eyeLyDefault
    moveRTox = eyeRxDefault
    moveRToy = eyeRyDefault

def moveEyes():
    global eyeLx, eyeLy, eyeRx, eyeRy, stepsDone
    # print(LastEyeLx)
    moveStepsLx = (moveLTox - LastEyeLx) / moveSteps
    moveStepsLy = (moveLToy - LastEyeLy) / moveSteps

    moveStepsRx = (moveRTox - LastEyeRx) / moveSteps
    moveStepsRy = (moveRToy - LastEyeRy) / moveSteps
    
    stepsDone += 1

    if(stepsDone <= moveSteps):
        eyeLx = eyeLx + moveStepsLx
        eyeLy = eyeLy + moveStepsLy

        eyeRx = eyeRx + moveStepsLx
        eyeRy = eyeRy + moveStepsLy



def drawEyes():
    global eyeLx, eyeLy, eyeRx, eyeRy, eyeLwidthCurrent, eyeRwidthCurrent, eyeLheightCurrent, eyeRheightCurrent
    screen.fill(BGCOLOR)  # Fill background
    if(eyesClosed):
        eyeLy = eyeLy + (eyeLheightDefault/2)
        eyeRy = eyeRy + (eyeRheightDefault/2)
    if(tired):
        if(eyesClosed):
            pygame.draw.ellipse(screen, MAINCOLOR, pygame.Rect(eyeLx, eyeLy, eyeLwidthCurrent, eyeLheightCurrent))
            pygame.draw.ellipse(screen, MAINCOLOR, pygame.Rect(eyeRx, eyeRy, eyeRwidthCurrent, eyeRheightCurrent))
        else:
            # pygame.draw.polygon(screen, MAINCOLOR, ((eyeLx, eyeLy+ eyeLheightDefault/4) , (eyeLx + eyeLwidthDefault, eyeLy) ,                     (eyeLx + eyeLwidthDefault, eyeLy + eyeLheightDefault), (eyeLx, eyeLy + eyeLheightDefault)) )
            # pygame.draw.polygon(screen, MAINCOLOR, ((eyeRx, eyeRy ),                      (eyeRx + eyeRwidthDefault, eyeRy+ eyeRheightDefault/4), (eyeRx + eyeRwidthDefault, eyeRy + eyeRheightDefault), (eyeRx, eyeRy + eyeRheightDefault)) )
            pygame.draw.ellipse(screen, MAINCOLOR, pygame.Rect(eyeLx, eyeLy, eyeLwidthCurrent, eyeLheightCurrent))
            pygame.draw.circle(screen, BGCOLOR, (eyeLx + eyeLwidthDefault/2 - 100 * scaleFactor, eyeLy + eyeLheightDefault/2 - 330 * scaleFactor ), eyeLwidthDefault/0.6 )

            pygame.draw.ellipse(screen, MAINCOLOR, pygame.Rect(eyeRx, eyeRy, eyeRwidthCurrent, eyeRheightCurrent))
            pygame.draw.circle(screen, BGCOLOR, (eyeRx + eyeRwidthDefault/2 + 100 * scaleFactor, eyeRy + eyeRheightDefault/2 - 330 * scaleFactor), eyeRwidthDefault/0.6  )



    elif(angry):  
        
        if(eyesClosed):
            pygame.draw.ellipse(screen, MAINCOLOR, pygame.Rect(eyeLx, eyeLy, eyeLwidthCurrent, eyeLheightCurrent))
            pygame.draw.ellipse(screen, MAINCOLOR, pygame.Rect(eyeRx, eyeRy, eyeRwidthCurrent, eyeRheightCurrent))
        else:
            # pygame.draw.polygon(screen, MAINCOLOR, ((eyeLx, eyeLy) ,                       (eyeLx + eyeLwidthDefault, eyeLy+ eyeLheightDefault/4) , (eyeLx + eyeLwidthDefault, eyeLy + eyeLheightDefault), (eyeLx, eyeLy + eyeLheightDefault)) )
            # pygame.draw.polygon(screen, MAINCOLOR, ((eyeRx, eyeRy + eyeRheightDefault/4), (eyeRx + eyeRwidthDefault, eyeRy),                        (eyeRx + eyeRwidthDefault, eyeRy + eyeRheightDefault), (eyeRx, eyeRy + eyeRheightDefault)) )
            pygame.draw.ellipse(screen, REDCOLOR, pygame.Rect(eyeLx, eyeLy, eyeLwidthCurrent, eyeLheightCurrent))
            pygame.draw.circle(screen, BGCOLOR, (eyeLx + eyeLwidthDefault/2 + 100 * scaleFactor, eyeLy + eyeLheightDefault/2 - 300 * scaleFactor), eyeLwidthDefault/0.6 )

            pygame.draw.ellipse(screen, REDCOLOR, pygame.Rect(eyeRx, eyeRy, eyeRwidthCurrent, eyeRheightCurrent))
            pygame.draw.circle(screen, BGCOLOR, (eyeRx + eyeRwidthDefault/2 - 100 * scaleFactor, eyeRy + eyeRheightDefault/2 - 300 * scaleFactor), eyeRwidthDefault/0.6)



    elif(happy):
        if(eyesClosed):
            pygame.draw.ellipse(screen, MAINCOLOR, pygame.Rect(eyeLx, eyeLy, eyeLwidthCurrent, eyeLheightCurrent))
            pygame.draw.ellipse(screen, MAINCOLOR, pygame.Rect(eyeRx, eyeRy, eyeRwidthCurrent, eyeRheightCurrent))

        else:
            pygame.draw.ellipse(screen, GREENCOLOR, pygame.Rect(eyeLx, eyeLy, eyeLwidthCurrent, eyeLheightCurrent))
            pygame.draw.circle(screen, BGCOLOR, (eyeLx + eyeLwidthDefault/2, eyeLy + eyeLheightDefault/2 + 100 * scaleFactor), eyeLwidthDefault/1.5)

            pygame.draw.ellipse(screen, GREENCOLOR, pygame.Rect(eyeRx, eyeRy, eyeRwidthCurrent, eyeRheightCurrent))
            pygame.draw.circle(screen, BGCOLOR, (eyeRx + eyeRwidthDefault/2, eyeRy + eyeRheightDefault/2 + 100 * scaleFactor), eyeRwidthDefault/1.5)

    elif(sleepy):
        if(eyesClosed):
            pygame.draw.ellipse(screen, MAINCOLOR, pygame.Rect(eyeLx, eyeLy, eyeLwidthCurrent, eyeLheightCurrent))
            pygame.draw.circle(screen, BGCOLOR, (eyeLx + eyeLwidthDefault/2 - 100 * scaleFactor, eyeLy + eyeLheightDefault/2 - 330 * scaleFactor ), eyeLwidthDefault/0.6 )

            pygame.draw.ellipse(screen, MAINCOLOR, pygame.Rect(eyeRx, eyeRy, eyeRwidthCurrent, eyeRheightCurrent))
            pygame.draw.circle(screen, BGCOLOR, (eyeRx + eyeRwidthDefault/2 + 100 * scaleFactor, eyeRy + eyeRheightDefault/2 - 330 * scaleFactor), eyeRwidthDefault/0.6  )

        else:
            pygame.draw.ellipse(screen, MAINCOLOR, pygame.Rect(eyeLx, eyeLy, eyeLwidthCurrent, eyeLheightCurrent))
            pygame.draw.circle(screen, BGCOLOR, (eyeLx + eyeLwidthDefault/2 - 100 * scaleFactor, eyeLy + eyeLheightDefault/2 - 330 * scaleFactor ), eyeLwidthDefault/0.6 )

            pygame.draw.ellipse(screen, MAINCOLOR, pygame.Rect(eyeRx, eyeRy, eyeRwidthCurrent, eyeRheightCurrent))
            pygame.draw.circle(screen, BGCOLOR, (eyeRx + eyeRwidthDefault/2 + 100 * scaleFactor, eyeRy + eyeRheightDefault/2 - 330 * scaleFactor), eyeRwidthDefault/0.6  )

    
    else:
        pygame.draw.ellipse(screen, MAINCOLOR, pygame.Rect(eyeLx, eyeLy, eyeLwidthCurrent, eyeLheightCurrent))
        pygame.draw.ellipse(screen, MAINCOLOR, pygame.Rect(eyeRx, eyeRy, eyeRwidthCurrent, eyeRheightCurrent))
        # pygame.draw.rect(screen, MAINCOLOR, pygame.Rect(eyeLx, eyeLy, eyeLwidthCurrent, eyeLheightCurrent), border_radius=eyeLborderRadiusDefault)
        # pygame.draw.rect(screen, MAINCOLOR, pygame.Rect(eyeRx, eyeRy, eyeRwidthCurrent, eyeRheightCurrent), border_radius=eyeRborderRadiusDefault)

    # Update the screen
    pygame.display.flip()





blink_interval_close = random.randint(3, 4)  # Random blink interval
blink_interval_open = random.randint(1,3) * 0.1
move_interval = random.randint(2,3)


def eyes(x ,y , mood = DEFAULT,selfMove = False, selfEmote = False):
    global blink_interval_close, blink_interval_open, move_interval ,eyeLx, eyeLy, eyeRx, eyeRy, eyeLwidthCurrent, eyeRwidthCurrent, eyeLheightCurrent, eyeRheightCurrent, LastEyeLx, LastEyeLy, LastEyeRx, LastEyeRy, lastMood, stepsDone, eyesClosed, last_blink_time, moved, lastUpdateTime,last_move_time
    
    if((time.time() - lastUpdateTime) > (frameInterval)):
        if(lastMood != mood):
            blink_interval_close = 0
        lastMood = mood

        screen.fill(BGCOLOR)  # Clear the screen

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        if(selfMove):
            if(not moved):
                if (time.time() - last_move_time) > move_interval:
                    moved = True
                    stepsDone = 0
                    LastEyeLx = eyeLx
                    LastEyeLy = eyeLy
                    LastEyeRx = eyeRx
                    LastEyeRy = eyeRy
                    moveEyesPos()
                    last_move_time = time.time()
            else:
                if (time.time() - last_move_time) > move_interval:
                    moved = False
                    stepsDone = 0
                    LastEyeLx = eyeLx
                    LastEyeLy = eyeLy
                    LastEyeRx = eyeRx
                    LastEyeRy = eyeRy
                    moveEyesHomePos()
                    last_move_time = time.time()
        else:
            x = x / 100 * 480
            y = y / 100 * 230
            eyeLx = eyeLxDefault + x
            eyeLy = eyeLyDefault + y 
            eyeRx = eyeRxDefault + x
            eyeRy = eyeRyDefault + y 


        if(not eyesClosed):
            if (time.time() - last_blink_time) > blink_interval_close:
                blinkClose()
                last_blink_time = time.time()
                blink_interval_close = random.randint(3, 5)  # Randomize blink interval
                eyesClosed = True

        else:
            if (time.time() - last_blink_time) > blink_interval_open:
                if(selfEmote):
                    mood = random.choice([DEFAULT, TIRED, ANGRY, HAPPY])
                
                setMood(mood)
                
                blinkOpen()
                eyesClosed = False
                blink_interval_open = random.randint(1,3) * 0.1
                last_blink_time = time.time()
            

        moveEyes()

        # Draw eyes on the screen
        drawEyes()
        lastUpdateTime = time.time()

