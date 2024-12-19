import pygame
import random
import time

test = pygame.image.load('sprites/boxes/sprite_1.png')
# boxColors = ["orange","green","cyan","pink","purple","brown","black"]
boxesImgs = {"orange": pygame.image.load('sprites/boxes/sprite_0.png'),"green": pygame.image.load('sprites/boxes/sprite_1.png'),"cyan": pygame.image.load('sprites/boxes/sprite_2.png'),"red": pygame.image.load('sprites/boxes/sprite_3.png'),"purple": pygame.image.load('sprites/boxes/sprite_4.png'),"yellow": pygame.image.load('sprites/boxes/sprite_5.png')}
dropoffImgs = {"orange": pygame.image.load('sprites/dropoffs/dropoff_orange.png'),"green": pygame.image.load('sprites/dropoffs/dropoff_green.png'),"cyan": pygame.image.load('sprites/dropoffs/dropoff_blue.png'),"red": pygame.image.load('sprites/dropoffs/dropoff_red.png'),"purple": pygame.image.load('sprites/dropoffs/dropoff_purple.png'),"yellow": pygame.image.load('sprites/dropoffs/dropoff_yellow.png'), "black": pygame.image.load('sprites/dropoffs/dropff_bomb.png') }
conveyerImgs = {"img1": pygame.image.load('sprites/conveyer/conveyer_0.png'), "img2:": pygame.image.load('sprites/conveyer/conveyer_1.png')}


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
                removedBox["color"] = "black"  # bomb boxes turn black after pick up
                removedBox["pickup_time"] = time.time()  # bomb takes action after a timeframe
                removedBox["image"] = pygame.image.load('sprites/boxes/sprite_6.png')
                removedBox["pickup_time"] = time.time() # bomb takes action after a timeframe

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
        print(abs(playerPosition.x - x))
        if abs(playerPosition.x - x) < 100 and abs(playerPosition.y - dropOff["location"] - 100) < 35:
            if dropOff["color"] == box["color"]:
                return box["points"]  # Return the points when box is dropped in the correct place

    return 0  # No points if box is not dropped in the correct place

# New Function: Bomb Explosion Effect ---
def handleBombExplosion(screen, bomb_box, player_pos):
    # Highlighted: Bomb explosion effect
    if bomb_box:
        # Explosion Effect: Flash the screen red
        pygame.draw.circle(screen, (255, 0, 0), bomb_box["rect"].center, 50)
        # Optionally, add sound here using pygame.mixer for explosion sound

        # Explosion damage: Check if the player is near the explosion
        if pygame.math.Vector2(bomb_box["rect"].center).distance_to(player_pos) < 100:
            # Damage player or perform some effect here
            pygame.draw.circle(screen, (255, 255, 255), player_pos, 40)  # Example: White flash effect on player
            print("Player hit by bomb!")  # You can replace this with health or game over logic
        bomb_box["exploded"] = True
    return bomb_box


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
        start_button = pygame.Rect(screen.get_width() / 2 - 100, 450, 200, 60)
        start_button_clicked = all_buttons(screen, start_button, "New Game", None, 40, "darkgreen", "white")

        
        quit_button = pygame.Rect(screen.get_width() / 2 - 100, 550, 200, 60)
        quit_button_clicked = all_buttons(screen, quit_button, "Quit", None, 40, "red", "white")


        if start_button_clicked: #click to start the game
             break #the main menu function breaks and the game starts

        if quit_button_clicked:
            pygame.quit()
            exit()

        pygame.display.flip() #render display & buttons

        clock.tick(60) #limiting framerate to 60 in main menu

        for event in pygame.event.get(): #make sure the game quits when the user closes the entire window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()




def pause_menu(screen):#created a pause menu
    clock = pygame.time.Clock()
    while True:
        screen.fill("lightgray")

        pause_text = all_text(None, 150, "PAUSED", True, "blue")#to display text on pause menu
        screen.blit(pause_text, ((screen.get_width() - pause_text.get_width()) / 2, 100))

        resume_button = pygame.Rect(screen.get_width() / 2 - 100, 450, 200, 60)#added resume button
        resume_button_clicked = all_buttons(screen, resume_button, "Resume", None, 40, "darkgreen", "white")

        #to add quit button
        quit_button = pygame.Rect(screen.get_width() / 2 - 100, 550, 200, 60)
        quit_button_clicked = all_buttons(screen, quit_button, "Quit", None, 40, "red", "white")

        if resume_button_clicked:
            break

        if quit_button_clicked:
            pygame.quit()
            exit()
            
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get(): #make sure the game quits when the user closes the entire window
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 700))
    clock = pygame.time.Clock()

    main_menu(screen)#call main menu
    paused = False #to call pause menu later
    running = True
    pygame.mixer.music.load("BEAT.mp3")  # Replace with the correct path to your music file
    pygame.mixer.music.set_volume(0.5)  # Set the volume (optional)
    pygame.mixer.music.play(-1, 0.0)  # Loop the music indefinitely
  
    dt, count, running, queuedBoxes = 0 , 100, True, []
    playerAnimationToggle = True
    
    playerImage = pygame.image.load("sprites/player/sprite_0.png")
    playerImageTwo = pygame.image.load("sprites/player/sprite_1.png")

    playerTwoImage = pygame.image.load("sprites/player/sprite_2.png")
    playerTwoImageTwo = pygame.image.load("sprites/player/sprite_3.png")

    player_pos = pygame.Vector2(screen.get_width() / 3, screen.get_height() / 2)
    player2_pos = pygame.Vector2(screen.get_width() / 1.5, screen.get_height() / 2)

    player_one_box = False
    player_two_box = False


    PLAYER_RADIUS = 40  # Defining the Size of the player
    player_one_score = 0  # Initialize player one's score
    player_two_score = 0  # Initialize player two's score

    conveyerSwitch = True
    # while game is running
    while running:
        screen.fill("skyblue")
        ## draw coveyer table

        drawScreenObjects(screen, conveyerSwitch)
        count +=1 # count to send new boxes in conveyer
        #conveyer animation
        if count % 13 == 0:
            conveyerSwitch = not conveyerSwitch
            playerAnimationToggle = not playerAnimationToggle

        #player animation

        
        # creates boxes every 100 count
        if count > 100 :
            boxColors = ["orange","green","cyan","red","purple","yellow"]
            randomPoints = random.randrange(1,4,1)
            box_is_bomb =  random.random() < 0.2 #20% chance of bomb
            boxColor = random.choice(boxColors)
            queuedBoxes.append({"rect": pygame.Rect(screen.get_width() / 2 - 32, 0, 55, 55), "points": randomPoints,"color": boxColor, "box_is_bomb": box_is_bomb,"image":boxesImgs[boxColor]})
            count = 0

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: #press P to call pause menu
                if event.key == pygame.K_p:
                   # paused = True
                    pause_menu(screen)
                        
                    

            if event.type == pygame.QUIT:
                running = False
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
                            
        if player_one_box and "box_is_bomb" in player_one_box and player_one_box["box_is_bomb"]:
            current_time = time.time()
            if current_time - player_one_box["pickup_time"] > 4:

                #print("Bomb")#this can be replaced with visual and sound effects
                player_one_box = False

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

        keys = pygame.key.get_pressed()
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
        

        # Display player scores
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Player 1 Score: {player_one_score}  Player 2 Score: {player_two_score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pause_text = all_text(None, 36, "Press P to pause", True, "black")
        screen.blit(pause_text, (screen.get_width() - pause_text.get_width() - 120, 650))

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        dt = clock.tick(100) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()
