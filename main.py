import pygame
import random
import time


# ALL IMAGES 

#images for boxes
boxesImgs = {"orange": pygame.image.load('sprites/boxes/sprite_0.png'),"green": pygame.image.load('sprites/boxes/sprite_1.png'),"cyan": pygame.image.load('sprites/boxes/sprite_2.png'),"red": pygame.image.load('sprites/boxes/sprite_3.png'),"purple": pygame.image.load('sprites/boxes/sprite_4.png'),"yellow": pygame.image.load('sprites/boxes/sprite_5.png')}
#images for dropoffs
dropoffImgs = {"orange": pygame.image.load('sprites/dropoffs/dropoff_orange.png'),"green": pygame.image.load('sprites/dropoffs/dropoff_green.png'),"cyan": pygame.image.load('sprites/dropoffs/dropoff_blue.png'),"red": pygame.image.load('sprites/dropoffs/dropoff_red.png'),"purple": pygame.image.load('sprites/dropoffs/dropoff_purple.png'),"yellow": pygame.image.load('sprites/dropoffs/dropoff_yellow.png'), "black": pygame.image.load('sprites/dropoffs/dropff_bomb.png') }

def allText(fontFile, fontSize, text, trueOrFalse, tColor): # one function to handle all texts
    textFont = pygame.font.Font(fontFile, fontSize) # font file and size
    textSurface = textFont.render(text, trueOrFalse, tColor) # content and color
    return textSurface # return the rendered text surface

def allButtons(screen, buttonRectShape, text, fontFile, fontSize, buttonColor, textColor): # one function to handle all buttons
    pygame.draw.rect(screen, buttonColor, buttonRectShape) # create a button
    buttonText = allText(fontFile, fontSize, text, True, textColor) # add text to the button
    screen.blit(
        buttonText , 
        (
            buttonRectShape.x + (buttonRectShape.width - buttonText.get_width()) / 2 ,
            buttonRectShape.y + (buttonRectShape.height - buttonText.get_height()) / 2,
        ),
    ) # put the text in the center of the button

    mousePosition = pygame.mouse.get_pos() # get current mouse position
    mouseClicked = pygame.mouse.get_pressed() # get mouse click status

    if buttonRectShape.collidepoint(mousePosition) and mouseClicked[0]:
        return True # return True if the button is clicked
    else: 
        return False
    

def conveyBoxes(queuedBoxes, screen):
    conveyerVelocity = pygame.math.Vector2(1, 1) # velocity that box should be moving in
    for box in queuedBoxes:
        box["rect"].y += int(conveyerVelocity.y) # moves boxes according to set velocity
        # draw boxes on screen 
        screen.blit(box["image"],(box["rect"].x, box["rect"].y))
        

def pickBox(queuedBoxes, playerOnePos):
    removedBox = False # default is no box was removed
    boxesInQueue = queuedBoxes # copies boxes in queue in order to later remove one box from list

    for box in range(len(queuedBoxes)): # loops through boxes in queue (loop by index)
        xDiff = abs(playerOnePos.x - queuedBoxes[box]["rect"].x) # calculates how close player is to box in the x dimension
        yDiff = abs(playerOnePos.y - queuedBoxes[box]["rect"].y) # calculates how close player is to box in the y dimension
        if xDiff < 100 and yDiff < 50: # if players is 100pixels close (x dimension) and  50 pixels close (y dimension) then player picks box
            indexRemoved = box # 'box' variable is the index (sinces loop is set to the range of the length of queued boxes)
            removedBox = queuedBoxes[box] # get's box to be removed by index
            if removedBox["boxIsBomb"]: # runs if a box is a bomb
                removedBox["color"] = "black"  # Displays box as bomb
                removedBox["pickupTime"] = time.time()  # marks when bomb was removed from box (explodes after a period of time)
                removedBox["image"] = pygame.image.load('sprites/boxes/sprite_6.png') # changes image displayed (to see bomb)
                removedBox["exploded"] = False # creates new key in box dictionary
            boxesInQueue.pop(indexRemoved) # removes picked up box from queue
            # Sets box position to by above players head
            removedBox["rect"].y = playerOnePos.y - 10 
            removedBox["rect"].x = playerOnePos.x + 20 
            break # breaks loop after found box to be removed 
    return {"newQueue": boxesInQueue, "boxPicked": removedBox} # returns new List of boxes and which box was removed

# draws drop off locations in screen
def drawDropOffs(screen):
    colors = ["orange","green","cyan","red","purple","yellow","black"]
    y = 25
    for color in colors:
        screen.blit(dropoffImgs[color], (screen.get_width() - 75, y))
        screen.blit(dropoffImgs[color], (25, y))
        y = y +100

# function for dropping boxes in correct location 
def dropBox(screen, playerOne, playerOnePosition, box):
    dropOffXLocation = 25 # dropoff x possition for player one (left side of the screen)
    if playerOne == False:
        dropOffXLocation = screen.get_width() - 85  # dropoff x possition for player two (right side of the screen)

    boxColors = ["orange","green","cyan","red","purple","yellow","black"] # drop off colors
    dropOffs = [] # List of drop of colors
    locationY = -50 # first location of the first dropoff zone
    for color in boxColors:
        dropOffs.append({"location": locationY, "color": color}) # appends a Dictionary of drop off zone information
        locationY = locationY + 100 # moves to the next dropoff zone location

    # loops through drop off zone list of dictionaties
    for dropOff in dropOffs:
        if abs(playerOnePosition.x - dropOffXLocation) < 100 and abs(playerOnePosition.y - dropOff["location"] - 100) < 35: # checks if player is close to dropoff zone in order to drop box
            if dropOff["color"] == box["color"]: # check if drop off zone player is close to is the same color as the box he is holding
                return box["points"]  # Return 1 point when the box is dropped in the correct place

    return 0  # No points if box is not dropped in the correct place
 

def bombTimerOver(screen, bombBox):
    #  Bomb explosion effect
    if bombBox and not bombBox["exploded"]:
        if time.time() - bombBox["pickupTime"] > 2: # checks bomb timer is over (2 seconds)
            # Draw explosion effect
            pygame.draw.circle(screen, (255, 0, 0), (bombBox["rect"].x + 60, bombBox["rect"].y), 50)
            return True # if timer is over 
    return False # if timer is not over 

# DRAWS STATIC OBJECTS
def drawScreenObjects(screen,conveyerSwitch):
    conveyerImg = pygame.image.load('sprites/conveyer/conveyer_0.png')
    tableImg = pygame.image.load("sprites/table/table.png")
    if(not conveyerSwitch): # Switches between to different pixel arts to portray movement in conveyer belt
        conveyerImg = pygame.image.load('sprites/conveyer/conveyer_1.png')
    screen.blit(conveyerImg,(screen.get_width() / 2 - 50,0))
    screen.blit(tableImg,(screen.get_width() - 100, 0))
    screen.blit(tableImg,(0, 0))
    drawDropOffs(screen)


def mainMenu(screen, playing):#to create a main menu
    clock = pygame.time.Clock()#get framerate
    inMainMenu = not playing
    

    while inMainMenu: #main menu shows until player click to start or quit game
        screen.fill("black") #the background color of main menu        
        # To make a smaller title
        titleText = allText(None, 100, "BOX MASTER", True, "purple")  # Reduced font size from 150 to 100
        screen.blit(titleText, ((screen.get_width() - titleText.get_width()) / 2, 80))  # Move title up slightly


        # Add "How to Play" instructions
        instructions = [
            "How to Play:",
            "1. Move Player 1 with W/A/S/D and Player 2 with Arrow Keys.",
            "2. Press SPACE (Player 1) or 'return/enter' (Player 2) to pick or drop a box.",
            "3. Match boxes to their corresponding drop-off zones to score points.",
            "4. Watch out for bombs! They deduct points  and paralyze player for 2 seconds when they explode.",
            "5. with player facing the conveyer, press space for player one and press enter for player two, to pick up boxes.",
            "6. Put the bombs in black drop-off zones before Bomb explodes to score points.",
            "7. The Game ends when someone gets 30 points.",
            "8. Press P to pause the game.",

        ]
        instructionY = 200  # Move instructions up (from 250 to 200)
        for line in instructions:
            instructionText = allText(None, 30, line, True, "black")
            screen.blit(instructionText, ((screen.get_width() - instructionText.get_width()) / 2, instructionY))
            instructionY += 30  # Increase Y position for the next line of instructions


        # Add start button
        startButton = pygame.Rect(screen.get_width() / 2 - 100, 450, 200, 60)
        startButtonClicked = allButtons(screen, startButton, "New Game", None, 40, "darkgreen", "white")

        # Add quit button
        quitButton = pygame.Rect(screen.get_width() / 2 - 100, 550, 200, 60)
        quitButtonClicked = allButtons(screen, quitButton, "Quit", None, 40, "red", "white")

        if startButtonClicked:  # click to start the game
            break  # the main menu function breaks and the game starts


        if startButtonClicked: #click to start the game
            return True #the main menu function breaks and the game starts

        if quitButtonClicked: #click to quit the game
            pygame.quit()
            exit()
            
        pygame.display.flip()  # render display & buttons

        clock.tick(60)  # limiting framerate to 60 in main menu

        for event in pygame.event.get():  # make sure the game quits when the user closes the entire window
            if event.type == pygame.QUIT:
                return True



        pygame.display.flip() #render display & buttons

        clock.tick(60) #limiting framerate to 60 in main menu

        for event in pygame.event.get(): #make sure the game quits when the user closes the entire window
            if event.type == pygame.QUIT:

                pygame.quit()
                exit()

def pauseMenu(screen):#created a pause menu
    clock = pygame.time.Clock()
    while True:
        screen.fill("lightgray")

        pauseText = allText(None, 150, "PAUSED", True, "blue")#to display text on pause menu
        screen.blit(pauseText, ((screen.get_width() - pauseText.get_width()) / 2, 100))

        resumeButton = pygame.Rect(screen.get_width() / 2 - 100, 350, 200, 60)#added resume button
        resumeButtonClicked = allButtons(screen, resumeButton, "Resume", None, 40, "darkgreen", "white")

        newgameButton = pygame.Rect(screen.get_width() / 2 - 100, 450, 200, 60)#added resume button
        newgameButtonClicked = allButtons(screen, newgameButton, "New Game", None, 40, "darkorange", "white")

        #to add quit button
        quitButton = pygame.Rect(screen.get_width() / 2 - 100, 550, 200, 60)
        quitButtonClicked = allButtons(screen, quitButton, "Quit", None, 40, "red", "white")

        if resumeButtonClicked:
            break
        
        if newgameButtonClicked:
            return True

        if quitButtonClicked:
            pygame.quit()
            exit()
            
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get(): #make sure the game quits when the user closes the entire window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def gameEnd(screen, winner, playerImage):
    clock = pygame.time.Clock()#get framerate
    while True:
        screen.fill("pink")
        screen.blit(playerImage, (screen.get_width()/2 - 30, screen.get_height() / 2 - 50 ))
        titleText = allText(None, 150, winner + " WINS!", True, "orange")
        screen.blit(titleText, ((screen.get_width() - titleText.get_width()) / 2, 100))

        newgameButton = pygame.Rect(screen.get_width() / 2 - 100, 450, 200, 60)
        newgameButtonClicked = allButtons(screen, newgameButton, "New Game", None, 40, "red", "white")

        quitButton = pygame.Rect(screen.get_width() / 2 - 100, 550, 200, 60)
        quitButtonClicked = allButtons(screen, quitButton, "Quit", None, 40, "red", "white")

        if quitButtonClicked:
            pygame.quit()
            exit()
            
        if newgameButtonClicked:
            return True

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get(): #make sure the game quits when the user closes the entire window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()



def inGame(screen, playing):
    screen = pygame.display.set_mode((1280, 700))
    
    pygame.mixer.pre_init()
    pygame.mixer.init()

    # plays music in channel 0
    pygame.mixer.Channel(0).play(pygame.mixer.Sound("./BEAT.mp3"))

    
    clock = pygame.time.Clock()
    running, count, queuedBoxes =  True, 100, []

    playerAnimationToggle = True # changes players sprites between two sprites

    # PLAYER IMAGES
    playerImage = pygame.image.load("sprites/player/sprite_0.png")
    playerImageTwo = pygame.image.load("sprites/player/sprite_1.png")
    playerTwoImage = pygame.image.load("sprites/player/sprite_2.png")
    playerTwoImageTwo = pygame.image.load("sprites/player/sprite_3.png")

    # PLAYER POSSTIONS
    playerOnePos = pygame.Vector2(screen.get_width() / 3, screen.get_height() / 2)
    playerTwoPos = pygame.Vector2(screen.get_width() / 1.5, screen.get_height() / 2)

    # BOX PLAYER IS HOLDING (False is no box is being held)
    playerOneBox = False 
    playerTwoBox = False

    # CONTROLS IF PLAYER CAN MOVE OR NOT AND HOW LONG THEY HAVE NOT BEING ABLE TO MOVE
    playerOneMovement = {"disabled": False, "time": time.time()}
    playerTwoMovement = {"disabled": False, "time": time.time()}
 
        
    PLAYER_RADIUS = 40  # Defining the Size of the player
    playerOneScore = 0  # Initialize player one's score
    playerTwoScore = 0  # Initialize player two's score 

    conveyerSwitch = True
    # while game is running
    while running:
        if(playerOneScore > 29 or playerTwoScore > 29):
            if(playerOneScore > playerTwoScore):
                restart = gameEnd(screen, "PLAYER ONE", playerImage)
                if(restart):
                    running = False
            if(playerOneScore < playerTwoScore):
                restart = gameEnd(screen, "PLAYER TWO", playerTwoImage)
                if(restart):
                    running = False
            
        screen.fill("skyblue")
        ## draw coveyer table
        drawScreenObjects(screen, conveyerSwitch)
        count +=1 # count to send new boxes in conveyer

        #conveyer + player animation
        if count % 13 == 0:
            conveyerSwitch = not conveyerSwitch
            playerAnimationToggle = not playerAnimationToggle

        # Handles bomb explosion / disables player movement and subtracts points
        if playerOneBox:            
            if playerOneBox["boxIsBomb"]:
                exploded = bombTimerOver(screen, playerOneBox) # function returns if bomb exploded or not
                if(exploded):
                    playerOneScore -= playerOneBox["points"] # deducts points
                    playerOneBox = False # removes box for players hand
                    playerOneMovement = {"disabled": True, "time": time.time()} # make disabled key in playmovement library equal to true
                    #handle sound effect
                    pygame.mixer.music.load("explosion.mp3")
                    pygame.mixer.music.play()

        if playerTwoBox:    
            if playerTwoBox["boxIsBomb"]:
                exploded = bombTimerOver(screen, playerTwoBox)
                if(exploded):
                    playerTwoScore -= playerTwoBox["points"] # deducts points
                    playerTwoBox = False # removes box for players hand
                    playerTwoMovement = {"disabled": True, "time": time.time()} # make disabled key in playmovement library equal to true
                    
                    #handle sound effect
                    pygame.mixer.music.load("explosion.mp3")
                    pygame.mixer.music.play()

        
            
        # enables movement again for player One
        if playerOneMovement["disabled"]:
            if playerOneMovement["time"] < time.time() - 2: # calculates time since player was able to move
                playerOneMovement = {"disabled": False, "time": time.time()}

        # enables movement again for player Two
        if playerTwoMovement["disabled"]:
            if playerTwoMovement["time"] < time.time() - 2:  # calculates time since player was able to move
                playerTwoMovement = {"disabled": False, "time": time.time()}

        
        # creates boxes every 100 count
        if count > 100 :
            boxColors = ["orange","green","cyan","red","purple","yellow"]
            randomPoints = random.randrange(1,4,1)
            boxIsBomb =  random.random() < 0.2 #20% chance of bomb
            boxColor = random.choice(boxColors)
            queuedBoxes.append({"rect": pygame.Rect(screen.get_width() / 2 - 32, 0, 55, 55), "points": randomPoints,"color": boxColor, "boxIsBomb": boxIsBomb,"image":boxesImgs[boxColor]})
            count = 0
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: #press P to call pause menu
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE :
                   if pauseMenu(screen):
                       running = False
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if playerOneBox:
                        boxDroppedPoints = dropBox(screen, True, playerOnePos, playerOneBox)
                        playerOneScore += boxDroppedPoints  # Add points if box is dropped
                        if boxDroppedPoints > 0:
                            playerOneBox = False

                    else: # if player is NOT holding box then pick box 
                        newBoxes = pickBox(queuedBoxes, playerOnePos)
                        queuedBoxes = newBoxes["newQueue"]
                        if newBoxes["boxPicked"] != False:
                            playerOneBox = newBoxes["boxPicked"]
                            playerOneBox["rect"].y = playerOnePos.y
                            playerOneBox["rect"].x = playerOnePos.x 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if playerTwoBox:
                        boxDroppedPoints = dropBox(screen, False, playerTwoPos, playerTwoBox)
                        playerTwoScore += boxDroppedPoints  # Add points if box is dropped
                        if boxDroppedPoints > 0:
                            playerTwoBox = False
                    else:
                        newBoxes = pickBox(queuedBoxes, playerTwoPos)
                        queuedBoxes = newBoxes["newQueue"]
                        if newBoxes["boxPicked"] != False:
                            playerTwoBox = newBoxes["boxPicked"]
                            playerTwoBox["rect"].y = playerTwoPos.y - 100
                            playerTwoBox["rect"].x = playerTwoPos.x - 30

                            
        if playerOneBox and "boxIsBomb" in playerOneBox and playerOneBox["boxIsBomb"]:
            if time.time() - playerOneBox["pickupTime"] > 4:
                #this can be replaced with visual and sound effects
                playerOneBox = False

        # draw and move boxes on conveyer
        conveyBoxes(queuedBoxes, screen)
        
        # Draw player position
        # pygame.draw.circle(screen, "purple", playerOnePos, 40)
        if playerAnimationToggle:
            screen.blit(playerImage, (playerOnePos.x, playerOnePos.y))
            screen.blit(playerTwoImage, (playerTwoPos.x, playerTwoPos.y))
        else:
            screen.blit(playerImageTwo, (playerOnePos.x, playerOnePos.y))
            screen.blit(playerTwoImageTwo, (playerTwoPos.x, playerTwoPos.y))
        
        


        if(playerOneBox):
            screen.blit(playerOneBox["image"],(playerOneBox["rect"].x + 30 , playerOneBox["rect"].y ))
        if(playerTwoBox):
            screen.blit(playerTwoBox["image"],(playerTwoBox["rect"].x + 30, playerTwoBox["rect"].y))
            
            
        if(len(queuedBoxes) > 8):
            del queuedBoxes[0]

        # Display player scores
        font = pygame.font.SysFont(None, 36)
        playerOneScoreText = font.render(f"Player 1: {playerOneScore}", True, (0, 0, 0))
        playerTwoScoreText = font.render(f"Player 2: {playerTwoScore}", True, (0, 0, 0)) # Position scores
        pygame.draw.rect(screen, (255, 255, 255), (screen.get_width() // 4 - playerOneScoreText.get_width() // 2 - 10, 5, playerOneScoreText.get_width() + 20, 30))
        pygame.draw.rect(screen, (255, 255, 255), (3 * screen.get_width() // 4 - playerTwoScoreText.get_width() // 2 - 10, 5, playerTwoScoreText.get_width() + 20, 30))
        
        # Position scores
        screen.blit(playerOneScoreText, (screen.get_width() // 4 - playerOneScoreText.get_width() // 2, 10))
        screen.blit(playerTwoScoreText, (3 * screen.get_width() // 4 - playerTwoScoreText.get_width() // 2, 10))


        keys = pygame.key.get_pressed()
        if(playerOneMovement["disabled"] == False): # if player not disabled then move
            if keys[pygame.K_w]:
                if(playerOnePos.y > 5): # enforces borders
                    playerOnePos.y -= 3
                if playerOneBox != False:
                    playerOneBox["rect"].y -= 3
            if keys[pygame.K_s]:
                if(playerOnePos.y < 625): # enforces borders
                    playerOnePos.y += 3   
                if playerOneBox != False:
                    playerOneBox["rect"].y += 3
            if keys[pygame.K_a]:
                if(playerOnePos.x > 110): # enforces borders
                    playerOnePos.x -= 3
                if playerOneBox != False:
                    playerOneBox["rect"].x -= 3
            if keys[pygame.K_d]:
                if(playerOnePos.x < 515): # enforces borders
                    playerOnePos.x += 3
                if playerOneBox != False:
                    playerOneBox["rect"].x += 3  
        
        if(playerTwoMovement["disabled"] == False): # if player not disabled then move
            if keys[pygame.K_UP]:
                if(playerTwoPos.y > 5): # enforces borders
                    playerTwoPos.y -= 3
                if playerTwoBox != False:
                    playerTwoBox["rect"].y -= 3
            if keys[pygame.K_DOWN]:
                if(playerTwoPos.y < 625): # enforces borders
                    playerTwoPos.y += 3   
                if playerTwoBox != False:
                    playerTwoBox["rect"].y += 3
            if keys[pygame.K_LEFT]:
                if(playerTwoPos.x > 700): # enforces borders
                    playerTwoPos.x -= 3
                if playerTwoBox != False:
                    playerTwoBox["rect"].x -= 3
            if keys[pygame.K_RIGHT]:
                if(playerTwoPos.x < 1100): # enforces borders
                    playerTwoPos.x += 3
                if playerTwoBox != False:
                    playerTwoBox["rect"].x += 3                      

        
        # Keeps the picked up box centered over the character
        if playerOneBox:
            playerOneBox["rect"].x = playerOnePos.x - playerOneBox["rect"].width // 2
            playerOneBox["rect"].y = playerOnePos.y - playerOneBox["rect"].height - 10
        if playerTwoBox:
            playerTwoBox["rect"].x = playerTwoPos.x - playerTwoBox["rect"].width // 2
            playerTwoBox["rect"].y = playerTwoPos.y - playerTwoBox["rect"].height - 10
        


        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        clock.tick(100) / 1000


def main():
    #SESSIONS : 1. In Game || 2. Main Menu
    pygame.init()
    screen = pygame.display.set_mode((1280, 700))
    running = True # Game is running
    playing = True # Player is playing game
    mainMenu(screen, False)
    while(running):
        exit = inGame(screen, playing)
        if(exit):
            pygame.quit()
if __name__ == "__main__":
    main()
