import pygame
import random
import time



test = pygame.image.load('sprites/boxes/sprite_1.png')
# boxColors = ["orange","green","cyan","pink","purple","brown","black"]
boxesImgs = {"orange": pygame.image.load('sprites/boxes/sprite_0.png'),"green": pygame.image.load('sprites/boxes/sprite_1.png'),"cyan": pygame.image.load('sprites/boxes/sprite_2.png'),"red": pygame.image.load('sprites/boxes/sprite_3.png'),"purple": pygame.image.load('sprites/boxes/sprite_4.png'),"yellow": pygame.image.load('sprites/boxes/sprite_5.png')}
dropoffImgs = {"orange": pygame.image.load('sprites/dropoffs/dropoff_orange.png'),"green": pygame.image.load('sprites/dropoffs/dropoff_green.png'),"cyan": pygame.image.load('sprites/dropoffs/dropoff_blue.png'),"red": pygame.image.load('sprites/dropoffs/dropoff_red.png'),"purple": pygame.image.load('sprites/dropoffs/dropoff_purple.png'),"yellow": pygame.image.load('sprites/dropoffs/dropoff_yellow.png'), "black": pygame.image.load('sprites/dropoffs/dropff_bomb.png') }
conveyerImgs = {"img1": pygame.image.load('sprites/conveyer/conveyer_0.png'), "img2:": pygame.image.load('sprites/conveyer/conveyer_1.png')}

player_one_disabled_until = 0  # Track when player 1 can move again
player_two_disabled_until = 0  # Track when player 2 can move again


def drawConveyer(screen,x,y,color, w,h):
    pygame.draw.rect(screen, color, pygame.Rect(x, y, w,h))

def drawRectBorders(screen,color ,rect):
    pygame.draw.rect(screen, color, rect,5)

def all_text(font_file, font_size, text, true_or_false, t_color): # one function to handle all texts
    text_font = pygame.font.Font(font_file, font_size) # font file and size
    text_surface = text_font.render(text, true_or_false, t_color) # content and color
    return text_surface # return the rendered text surface

def all_buttons(screen, button_rect_shape, text, font_file, font_size, button_color, text_color): # one function to handle all buttons
    pygame.draw.rect(screen, button_color, button_rect_shape) # create a button
    button_text = all_text(font_file, font_size, text, True, text_color) # add text to the button
    screen.blit(
        button_text , 
        (
            button_rect_shape.x + (button_rect_shape.width - button_text.get_width()) / 2 ,
            button_rect_shape.y + (button_rect_shape.height - button_text.get_height()) / 2,
        ),
    ) # put the text in the center of the button

    mouse_position = pygame.mouse.get_pos() # get current mouse position
    mouse_clicked = pygame.mouse.get_pressed() # get mouse click status

    if button_rect_shape.collidepoint(mouse_position) and mouse_clicked[0]:
        return True # return True if the button is clicked
    else: 
        return False
    

def conveyBoxes(queuedBoxes, screen):
    conveyerVelocity = pygame.math.Vector2(1, 1)
    for box in queuedBoxes:
        box["rect"].y += int(conveyerVelocity.y)

        # draw boxes on screen 
        screen.blit(box["image"],(box["rect"].x, box["rect"].y))
        

def pickBox(queuedBoxes, player_pos):
    removedBox = False
    indexRemoved = -1
    newBoxes = queuedBoxes

    for box in range(len(queuedBoxes)):
        x_diff = abs(player_pos.x - queuedBoxes[box]["rect"].x)
        y_diff = abs(player_pos.y - queuedBoxes[box]["rect"].y)
        if x_diff < 100 and y_diff < 50:
            indexRemoved = box
            removedBox = queuedBoxes[box]
            if removedBox["box_is_bomb"]:
                removedBox["color"] = "black"  # Displays box as bomb
                removedBox["pickup_time"] = time.time()  # bomb takes action after a timeframe
                removedBox["image"] = pygame.image.load('sprites/boxes/sprite_6.png')
                removedBox["exploded"] = False
            newBoxes.pop(indexRemoved)
            removedBox["rect"].y = player_pos.y - 10
            removedBox["rect"].x = player_pos.x + 20
            break
    return {"newQueue": newBoxes, "boxPicked": removedBox}

def drawDropOffs(screen):

    colors = ["orange","green","cyan","red","purple","yellow","black"]
    y = 25
    for color in colors:
        screen.blit(dropoffImgs[color], (screen.get_width() - 75, y))
        # drawRectBorders(screen, color,((screen.get_width() - 75,y,55,55)))
        screen.blit(dropoffImgs[color], (25, y))

        y = y +100

def dropBox(screen, playerOne, playerPosition, box):
    x = 25
    if playerOne == False:
        x = screen.get_width() - 85

    boxColors = ["orange","green","cyan","red","purple","yellow","black"]
    dropOffs = []
    locationY = -50
    for color in boxColors:
        dropOffs.append({"location": locationY, "color": color})
        locationY = locationY + 100
    for dropOff in dropOffs:
        if abs(playerPosition.x - x) < 100 and abs(playerPosition.y - dropOff["location"] - 100) < 35:
            if dropOff["color"] == box["color"]:
                return box["points"]  # Return 1 point when the box is dropped in the correct place

    return 0  # No points if box is not dropped in the correct place
 

def handleBombExplosion(screen, bomb_box):
    #  Bomb explosion effect
    if bomb_box and not bomb_box["exploded"]:
        current_time = time.time()
        if current_time - bomb_box["pickup_time"] > 1.7: # checks if bomb is past time
            # Draw explosion effect
            pygame.draw.circle(screen, (255, 0, 0), (bomb_box["rect"].x + 60, bomb_box["rect"].y), 50)
            # Deduct points
            return True
    return False


conveyerSwitch = True 

def drawScreenObjects(screen,conveyerSwitch):
    conveyerImg = pygame.image.load('sprites/conveyer/conveyer_0.png')
    tableImg = pygame.image.load("sprites/table/table.png")
    if(not conveyerSwitch):
        conveyerImg = pygame.image.load('sprites/conveyer/conveyer_1.png')

    # drawConveyer(screen, screen.get_width() / 2 - 50,0,"red",100,screen.get_height())
    screen.blit(conveyerImg,(screen.get_width() / 2 - 50,0))
    screen.blit(tableImg,(screen.get_width() - 100, 0))
    screen.blit(tableImg,(0, 0))
    drawDropOffs(screen)

def main_menu(screen):#to create a main menu
    clock = pygame.time.Clock()#get framerate
    
    while True: #main menu shows until player click to start or quit game
        screen.fill("lightgray") #the background color of main menu
        
        #to make a title
        title_text = all_text(None, 150, "BOX MASTER", True, "purple")
        screen.blit(title_text, ((screen.get_width() - title_text.get_width()) / 2, 100))

        #to add start button
        start_button = pygame.Rect(screen.get_width() / 2 - 100, 350, 200, 60)
        start_button_clicked = all_buttons(screen, start_button, "Start", None, 40, "darkgreen", "white")

        #to add help & pause button
        help_pause_button = pygame.Rect(screen.get_width() / 2 - 100, 450, 200, 60)
        help_pause_button_clicked = all_buttons(screen, help_pause_button, "How to play", None, 40, "orange", "white")

        #to add quit button
        quit_button = pygame.Rect(screen.get_width() / 2 - 100, 550, 200, 60)
        quit_button_clicked = all_buttons(screen, quit_button, "Quit", None, 40, "red", "white")


        if start_button_clicked: #click to start the game
            break #the main menu function breaks and the game starts


        if quit_button_clicked: #click to quit the game
            return True

        pygame.display.flip() #render display & buttons

        clock.tick(60) #limiting framerate to 60 in main menu

        for event in pygame.event.get(): #make sure the game quits when the user closes the entire window
            if event.type == pygame.QUIT:
                return True


def inGame(screen, gameRunning):
    clock = pygame.time.Clock()
    dt, count, running, queuedBoxes = 0 , 100, gameRunning, []
    playerAnimationToggle = True
    
    playerImage = pygame.image.load("sprites/player/sprite_0.png")
    playerImageTwo = pygame.image.load("sprites/player/sprite_1.png")

    playerTwoImage = pygame.image.load("sprites/player/sprite_2.png")
    playerTwoImageTwo = pygame.image.load("sprites/player/sprite_3.png")

    player_pos = pygame.Vector2(screen.get_width() / 3, screen.get_height() / 2)
    player2_pos = pygame.Vector2(screen.get_width() / 1.5, screen.get_height() / 2)

    player_one_box = False
    player_two_box = False
    playerOneMovement = {"disabled": False, "time": time.time()}
    playerTwoMovement = {"disabled": False, "time": time.time()}
 

    PLAYER_RADIUS = 40  # Defining the Size of the player
    player_one_score = 0  # Initialize player one's score
    player_two_score = 0  # Initialize player two's score 

    conveyerSwitch = True
    # while game is running
    while running:
        screen.fill("white")
        ## draw coveyer table
        
        drawScreenObjects(screen, conveyerSwitch)
        count +=1 # count to send new boxes in conveyer
        #conveyer animation
        if count % 13 == 0:
            conveyerSwitch = not conveyerSwitch
            playerAnimationToggle = not playerAnimationToggle
            

        # Other game logic goes here...
        # if player_one_box:
            # boxDroppedPoints = dropBox(screen, True, player_pos, player_one_box)
            # player_one_score += boxDroppedPoints  # Add points if box is dropped

        # Handle bomb explosion / disables player movement and subtracts points
        if player_one_box:            
            if player_one_box["box_is_bomb"]:
                exploded = handleBombExplosion(screen, player_one_box)
                if(exploded):
                    player_one_score -= player_one_box["points"]
                    player_one_box = False 
                    playerOneMovement = {"disabled": True, "time": time.time()}
                    pygame.mixer.music.load("explosion.mp3")  # Replace with the correct path to your music file
                    pygame.mixer.music.set_volume(0.5)  # Set the volume (optional)
                    pygame.mixer.music.play()

        # enables movement again
        if playerOneMovement["disabled"]:
            if playerOneMovement["time"] < time.time() - 2:
                playerOneMovement = {"disabled": False, "time": time.time()}


        
        # creates boxes every 100 count
        if count > 100 :
            boxColors = ["orange","green","cyan","red","purple","yellow"]
            randomPoints = random.randrange(1,4,1)
            box_is_bomb =  random.random() < 0.2 #20% chance of bomb
            boxColor = random.choice(boxColors)
            queuedBoxes.append({"rect": pygame.Rect(screen.get_width() / 2 - 32, 0, 55, 55), "points": randomPoints,"color": boxColor, "box_is_bomb": box_is_bomb,"image":boxesImgs[boxColor]})
            count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_one_box:
                        boxDroppedPoints = dropBox(screen, True, player_pos, player_one_box)
                        player_one_score += boxDroppedPoints  # Add points if box is dropped
                        if boxDroppedPoints > 0:
                            player_one_box = False

                    else: # if player is NOT holding box then pick box 
                        newBoxes = pickBox(queuedBoxes, player_pos)
                        queuedBoxes = newBoxes["newQueue"]
                        if newBoxes["boxPicked"] != False:
                            player_one_box = newBoxes["boxPicked"]
                            player_one_box["rect"].y = player_pos.y
                            player_one_box["rect"].x = player_pos.x 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SLASH:
                    if player_two_box:
                        boxDroppedPoints = dropBox(screen, False, player2_pos, player_two_box)
                        player_two_score += boxDroppedPoints  # Add points if box is dropped
                        if boxDroppedPoints > 0:
                            player_two_box = False
                    else:
                        newBoxes = pickBox(queuedBoxes, player2_pos)
                        queuedBoxes = newBoxes["newQueue"]
                        if newBoxes["boxPicked"] != False:
                            player_two_box = newBoxes["boxPicked"]
                            player_two_box["rect"].y = player2_pos.y - 100
                            player_two_box["rect"].x = player2_pos.x - 30

        # draw and move boxes on conveyer
        conveyBoxes(queuedBoxes, screen)
        
        # Draw player position
        # pygame.draw.circle(screen, "purple", player_pos, 40)
        if playerAnimationToggle:
            screen.blit(playerImage, (player_pos.x, player_pos.y))
            screen.blit(playerTwoImage, (player2_pos.x, player2_pos.y))
        else:
            screen.blit(playerImageTwo, (player_pos.x, player_pos.y))
            screen.blit(playerTwoImageTwo, (player2_pos.x, player2_pos.y))
        
        


        if(player_one_box):
            screen.blit(player_one_box["image"],(player_one_box["rect"].x + 30 , player_one_box["rect"].y ))
        if(player_two_box):
            screen.blit(player_two_box["image"],(player_two_box["rect"].x + 30, player_two_box["rect"].y))
            
            
        if(len(queuedBoxes) > 8):
            del queuedBoxes[0]

            # Display player scores
        font = pygame.font.SysFont(None, 36)
        player_one_score_text = font.render(f"Player 1: {player_one_score}", True, (0, 0, 0))
        player_two_score_text = font.render(f"Player 2: {player_two_score}", True, (0, 0, 0)) # Position scores
        pygame.draw.rect(screen, (255, 255, 255), (screen.get_width() // 4 - player_one_score_text.get_width() // 2 - 10, 5, player_one_score_text.get_width() + 20, 30))
        pygame.draw.rect(screen, (255, 255, 255), (3 * screen.get_width() // 4 - player_two_score_text.get_width() // 2 - 10, 5, player_two_score_text.get_width() + 20, 30))
        # Position scores
        screen.blit(player_one_score_text, (screen.get_width() // 4 - player_one_score_text.get_width() // 2, 10))
        screen.blit(player_two_score_text, (3 * screen.get_width() // 4 - player_two_score_text.get_width() // 2, 10))


        keys = pygame.key.get_pressed()
        if(playerOneMovement["disabled"] == False):
            if keys[pygame.K_w]:
                if(player_pos.y > 5): # enforces borders
                    player_pos.y -= 3
                if player_one_box != False:
                    player_one_box["rect"].y -= 3
            if keys[pygame.K_s]:
                if(player_pos.y < 625): # enforces borders
                    player_pos.y += 3   
                if player_one_box != False:
                    player_one_box["rect"].y += 3
            if keys[pygame.K_a]:
                if(player_pos.x > 110): # enforces borders
                    player_pos.x -= 3
                if player_one_box != False:
                    player_one_box["rect"].x -= 3
            if keys[pygame.K_d]:
                if(player_pos.x < 515): # enforces borders
                    player_pos.x += 3
                if player_one_box != False:

                    player_one_box["rect"].x += 3  
        
                
        if keys[pygame.K_UP]:
            if(player2_pos.y > 5): # enforces borders
                player2_pos.y -= 3
            if player_two_box != False:
                player_two_box["rect"].y -= 3
        if keys[pygame.K_DOWN]:
            if(player2_pos.y < 625): # enforces borders
                player2_pos.y += 3   
            if player_two_box != False:
                player_two_box["rect"].y += 3
        if keys[pygame.K_LEFT]:
            if(player2_pos.x > 700): # enforces borders
                player2_pos.x -= 3
            if player_two_box != False:
                player_two_box["rect"].x -= 3
        if keys[pygame.K_RIGHT]:
            if(player2_pos.x < 1100): # enforces borders
                player2_pos.x += 3
            if player_two_box != False:

                player_two_box["rect"].x += 3                      

        if player_pos.x > screen.get_width() / 2 - 50 - PLAYER_RADIUS:
            player_pos.x = screen.get_width() / 2 - 50 - PLAYER_RADIUS
        
        # Keeps the box centered over the character
        if player_one_box:
            player_one_box["rect"].x = player_pos.x - player_one_box["rect"].width // 2
            player_one_box["rect"].y = player_pos.y - player_one_box["rect"].height - 10
        if player_two_box:
            player_two_box["rect"].x = player2_pos.x - player_two_box["rect"].width // 2
            player_two_box["rect"].y = player2_pos.y - player_two_box["rect"].height - 10
        

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        dt = clock.tick(100) / 1000


def main():
    #SESSIONS : 1. In Game || 2. Main Menu
    pygame.init()
    screen = pygame.display.set_mode((1280, 700))
    running = True # Game is running
    playing = True # Player is playing game
    while(running):
        playing = not playing # switches from main menu to in game every time a session ends
        if playing:
            exit = inGame(screen, playing)
            if(exit):
                pygame.quit()
        else:
            exit = main_menu(screen)
            if(exit):
                pygame.quit()
        
    pygame.quit()


if __name__ == "__main__":
    main()
