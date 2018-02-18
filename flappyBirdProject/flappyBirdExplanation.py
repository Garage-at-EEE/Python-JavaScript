from Settings import *
from Functions import *

def main():
    global SCREEN, FPSCLOCK # set These two variable as global variable so that they can be used in other functions -- scope ( LEGB )
    pygame.init() # method in module -- pygame
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) # start a pygame canvas -- initialization
    pygame.display.set_caption('Flappy Bird') # title of the pygame

    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png'), # when loading the image 
        pygame.image.load('assets/sprites/1.png'),
        pygame.image.load('assets/sprites/2.png'),
        pygame.image.load('assets/sprites/3.png'),
        pygame.image.load('assets/sprites/4.png'),
        pygame.image.load('assets/sprites/5.png'),
        pygame.image.load('assets/sprites/6.png'),
        pygame.image.load('assets/sprites/7.png'),
        pygame.image.load('assets/sprites/8.png'),
        pygame.image.load('assets/sprites/9.png')
    )
    # variable
    #-----------------
    # dictionary
    # key -- 'numbers'
    # value -- new data type (tuple) with several values

    # game over sprite
    IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png')
    # message sprite for welcome screen
    IMAGES['message'] = pygame.image.load('assets/sprites/message.png')
    # base (ground) sprite
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png')

    while True:# infinite loop -- no exit.
        # select random background sprites
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1) # len(list) get the length len(list) - 1 is the last element
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg])
        # select random player sprites
        randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[randPlayer][0]),
            pygame.image.load(PLAYERS_LIST[randPlayer][1]),
            pygame.image.load(PLAYERS_LIST[randPlayer][2]),
        )
        # select random pipe sprites
        pipeindex = random.randint(0, len(PIPES_LIST) - 1) # get the piple number
        IMAGES['pipe'] = (
            pygame.transform.rotate(pygame.image.load(PIPES_LIST[pipeindex]), 180), # Take the pipe upside down
            pygame.image.load(PIPES_LIST[pipeindex]),
        )
        ################################## ./Functions.py
        # find a solution to determine the size of the object. ( non-rectangular object ) =>object abstractions.
        # hitmask for pipes
        HITMASKS['pipe'] = (
            getHitmask(IMAGES['pipe'][0]),
            getHitmask(IMAGES['pipe'][1]),
        )

        # hitmask for player
        HITMASKS['player'] = (
            getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
            getHitmask(IMAGES['player'][2]),
        )
        ##################################
        # three stages to determine the process of the game.
        movementInfo = showWelcomeAnimation() 
        '''
        return {
            'playery': playery + playerShmVals['val'],  # get y value and assign to key playery standard y + harmonic motion
            'basex': basex,                             # x value of the base note that base is moving ( sudo moving )
            'playerIndexGen': playerIndexGen,           # get wings state
        }
        '''
        crashInfo = mainGame(movementInfo)
        showGameOverScreen(crashInfo)

def showWelcomeAnimation():
    """Shows welcome screen animation of flappy bird"""
    # index of player to blit on screen
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0

    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)

    basex = 0
    # amount by which base can maximum shift to left
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # player simple harmonic motion for up-down motion on welcome screen
    playerShmVals = {'val': 0, 'dir': 1}

    while True: # start the game
        for event in pygame.event.get():
            '''
            This function will return when player stroke 'space' key
            '''
            '''
            Event will include mouse position and key stroke(UP and DOWN) together with some value 
            e.g. mouse X,Y position and key name.
            ##########################################################################################
                                            windows active event

                <Event(1-ActiveEvent {'gain': 1, 'state': 1})> focus on screen mouse move in
                <Event(1-ActiveEvent {'gain': 0, 'state': 1})> focus on screen mouse move out
                <Event(1-ActiveEvent {'gain': 0, 'state': 2})> unfocus on screen app not running
                <Event(1-ActiveEvent {'gain': 1, 'state': 6})> call back from unfocus
                -----------------------------------------------------------------------------------
                                            mouse moving event =              
                            {
                                pos: position
                                rel: relative position 
                                buttons: {
                                    element: {
                                        x:left,
                                        y:middle,
                                        z:right
                                    }
                                    value: {
                                        1: active,
                                        0: inactive
                                    }
                                }
                            }
                <Event(4-MouseMotion {'pos': (287, 405), 'rel': (20, -106), 'buttons': (0, 0, 0)})> 
                <Event(4-MouseMotion {'pos': (271, 403), 'rel': (-16, -2), 'buttons': (0, 0, 0)})>
                -----------------------------------------------------------------------------------
                                            holding mouse event
                <Event(4-MouseMotion {'pos': (248, 401), 'rel': (10, 0), 'buttons': (1, 0, 0)})>
                <Event(4-MouseMotion {'pos': (268, 401), 'rel': (20, 0), 'buttons': (1, 0, 0)})>
                <Event(4-MouseMotion {'pos': (286, 400), 'rel': (18, -1), 'buttons': (1, 0, 0)})>
                -----------------------------------------------------------------------------------
                                            stroke keyboard event = 
                            {
                                mod: {
                                meaning: existing key stroke
                                value:{
                                    1:  left-shift,
                                    2:  right-shift,
                                    256:    left-alt
                                    257: left-shift + left-alt
                                    }
                                }   
                                unicode: value of the key e.g. a,b,c,d
                                key: unicode number       e.g. 97,98,99,100
                                scancode: key position on the keyboard
                            }
                <Event(2-KeyDown {'unicode': '', 'key': 304, 'mod': 0, 'scancode': 42})>
                <Event(3-KeyUp {'key': 304, 'mod': 0, 'scancode': 42})>
                -----------------------------------------------------------------------------------
                                            left mouse click event

                <Event(5-MouseButtonDown {'pos': (194, 417), 'button': 1})> 
                <Event(4-MouseMotion {'pos': (199, 417), 'rel': (5, 0), 'buttons': (1, 0, 0)})>
                <Event(4-MouseMotion {'pos': (204, 416), 'rel': (5, -1), 'buttons': (1, 0, 0)})>
                <Event(6-MouseButtonUp {'pos': (204, 416), 'button': 1})>
                -----------------------------------------------------------------------------------
                                           
            ##########################################################################################
            pygame.event.get will update repeatedly when the game is running
            '''
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                '''
                QUIT is the event when you click on the 'X' button
                event.type KEYDOWN is the event when you press down a button 
                event.key K_ESCAPE is the 'Esc' key
                '''
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # make first flap sound and return values for mainGame
                # start the game
                return {
                    'playery': playery + playerShmVals['val'],  # get entry point value and assign to key playery
                    'basex': basex,                             # x value of the base note that base is moving ( sudo moving )
                    'playerIndexGen': playerIndexGen,           # get player number
                }

        # adjust playery, playerIndex, basex
        if (loopIter + 1) % 5 == 0:
            playerIndex = next(playerIndexGen) # use to display the wings -- final implementation
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 100) % baseShift) # make base move
        playerShm(playerShmVals)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))
        SCREEN.blit(IMAGES['player'][playerIndex], # useless
                    (playerx, playery + playerShmVals['val'])) # initial harmonic motion -- final implementation
        SCREEN.blit(IMAGES['message'], (messagex, messagey))
        SCREEN.blit(IMAGES['base'], (basex, BASEY)) # create the location for base
        pygame.display.update()
        FPSCLOCK.tick(FPS) # frames per second.

def mainGame(movementInfo):
    score = playerIndex = loopIter = 0
    playerIndexGen = movementInfo['playerIndexGen']
    playerx, playery = int(SCREENWIDTH * 0.2), movementInfo['playery'] # initialize x and get y value from previous session

    basex = movementInfo['basex']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # get 2 new pipes to add to upperPipes lowerPipes list
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # ---------------------------------------
    # implementation
    # PIPDISTANCE = 144
    # INITIALPIPE = 400
    # def pipesGen(getRandomPipe,width):
    #     pU = pD = []
    #     for i in range(width//PIPDISTANCE):
    #         pU.append({'x':INITIALPIPE,'y':getRandomPipe()[0]['y']})
    #         pD.append({'x':INITIALPIPE,'y':getRandomPipe()[1]['y']})
    #     return (pU,pD)
    # upperPipes,lowerPipes = pipeGen(newPipe1,newPipe2,SCREENWIDTH)
    # ---------------------------------------
    
    # in the canvas there can only exist two pipes.
    # list of upper pipes
    
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # list of lowerpipe
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]


    #####################################################################################
    #                               physics engine

    # player velocity, max velocity, downward accleration, accleration on flap
    pipeVelX      =  -4

    playerVelY    =  -9   # player's velocity along Y, default same as playerFlapped
    playerMaxVelY =  10   # max vel along Y, max descend speed
    playerMinVelY =  -8   # min vel along Y, max ascend speed
    playerAccY    =   1   # players downward accleration
    playerRot     =  45   # player's rotation
    playerVelRot  =   3   # angular speed
    playerRotThr  =  20   # rotation threshold
    playerFlapAcc =  -9   # players speed on flapping
    playerFlapped = False # True when player flaps

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP): # key event control
                if playery > 0: # in canvas bird
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    

        # check for crash here
        crashTest = checkCrash({'x': playerx, 'y': playery, 'index': playerIndex},
                               upperPipes, lowerPipes)
        if crashTest[0]:
            return {
                'y': playery,
                'groundCrash': crashTest[1], # second element in crash Test
                'basex': basex,
                'upperPipes': upperPipes,
                'lowerPipes': lowerPipes,
                'score': score,
                'playerVelY': playerVelY,
                'playerRot': playerRot
            }

        # check for score
        playerMidPos = playerx + IMAGES['player'][0].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4: # pipe velocity is -4 if not specify + 4 score will add A lot, since game updates fast
                score += 1                

        # playerIndex basex change
        if (loopIter + 1) % 5 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + baseShift-pipeVelX) % baseShift) # math trick! since velocity is -4 we need to find the value so that base can move alone with the pipe

        # rotate the player
        if playerRot > -90:
            playerRot -= playerVelRot

        # player's movement
        if playerVelY < playerMaxVelY and not playerFlapped: # once flap change volocity to -9 and gradually drop down to +10
            playerVelY += playerAccY
        if playerFlapped:# one time applicable
            playerFlapped = False

            # more rotation to cover the threshold (calculated in visible rotation)
            playerRot = 45

        playerHeight = IMAGES['player'][playerIndex].get_height()
        playery += min(playerVelY, BASEY - playery - playerHeight) # when the bird is closer to the ground, crash to the ground surface.

        # move pipes to left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])
            
        # remove first pipe if its out of the screen
        if upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # redraw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        # print score so player overlaps the score
        showScore(score)

        # Player rotation has a threshold
        visibleRot = playerRotThr
        if playerRot <= playerRotThr:
            visibleRot = playerRot

        # create a object formally called surface which has a rotation value
        playerSurface = pygame.transform.rotate(IMAGES['player'][playerIndex], visibleRot)
        SCREEN.blit(playerSurface, (playerx, playery))

        pygame.display.update()
        FPSCLOCK.tick(FPS) # frame per second




def showGameOverScreen(crashInfo):
    """crashes the player down ans shows gameover image"""
    score = crashInfo['score']
    # playerx = SCREENWIDTH * 0.2
    # playery = crashInfo['y']
    # playerHeight = IMAGES['player'][0].get_height()
    # playerVelY = crashInfo['playerVelY']
    # playerAccY = 2
    # playerRot = crashInfo['playerRot']
    # playerVelRot = 7

    # basex = crashInfo['basex']

    # upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery + playerHeight >= BASEY - 1:
                    return

        # # player y shift
        # if playery + playerHeight < BASEY - 1:
        #     playery += min(playerVelY, BASEY - playery - playerHeight)

        # # player velocity change
        # if playerVelY < 15:
        #     playerVelY += playerAccY

        # # rotate only when it's a pipe crash
        # if not crashInfo['groundCrash']:
        #     if playerRot > -90:
        #         playerRot -= playerVelRot

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))
        SCREEN.blit(IMAGES['gameover'], ((SCREENHEIGHT-IMAGES['gameover'].get_height)/2,SCREENWIDTH-IMAGES['gameover'].get_width)/2))
        print(1)
        # for uPipe, lPipe in zip(upperPipes, lowerPipes):
        #     SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
        #     SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        # SCREEN.blit(IMAGES['base'], (basex, BASEY))
        showScore(score)

        # playerSurface = pygame.transform.rotate(IMAGES['player'][1], playerRot)
        # SCREEN.blit(playerSurface, (playerx,playery))

        FPSCLOCK.tick(FPS)
        pygame.display.update()

def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]# change number to list and use graph to show
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()


if __name__ == '__main__':
    main()
