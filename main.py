import pygame
import random
import time #add timer

def drawConveyer(screen,x,y,color, w,h):
    #                                                        xAxis              y  width height
    pygame.draw.rect(screen, color, pygame.Rect(x, y, w,h))

def drawRectBorders(screen,color ,rect):
    pygame.draw.rect(screen, color, rect,5)


def conveyBoxes(queuedBoxes, screen):
    conveyerVelocity = pygame.math.Vector2(1, 1)
    for box in queuedBoxes:
        box["rect"].y += int(conveyerVelocity.y)
        # draw boxes on scree
        pygame.draw.rect(screen,box["color"], box["rect"])    

def pickBox(queuedBoxes, player_pos):
    removedBox = False
    indexRemoved = -1
    newBoxes = queuedBoxes

    for box in range(len(queuedBoxes)):
        x_diff = abs(player_pos.x - queuedBoxes[box]["rect"].x )
        y_diff = abs(player_pos.y - queuedBoxes[box]["rect"].y)
        if x_diff < 80 and y_diff < 50:
            indexRemoved = box
            removedBox = queuedBoxes[box]
            if removedBox["box_is_bomb"]:
                removedBox["color"] = "black" # bomb boxes turn black after pick up
                removedBox["pickup_time"] = time.time # bomb takes action after a timeframe

            newBoxes.pop(indexRemoved)
            removedBox["rect"].y = player_pos.y - 50
            removedBox["rect"].x = player_pos.x
            break
    return {"newQueue": newBoxes, "boxPicked": removedBox}

def drawDropOffs(screen):
    colors = ["orange","green","cyan","pink","purple","brown","gray"]
    y = 25
    for color in colors:
        drawRectBorders(screen, color,((screen.get_width() - 75,y,55,55)))
        drawRectBorders(screen, color,((25,y,55,55)))
        y = y +100



def dropBox(screen,playerOne, playerPosition,box):
    x, y = 25, screen.get_height() / 2 - 175
    if playerOne == False:
        x = screen.get_width() - 75
    boxColors = ["orange","green","cyan","pink","purple","brown","gray"]

    dropOffs = []
    locationY = -35
    for color in boxColors:
        dropOffs.append({"location": locationY, "color": color})
        locationY = locationY + 100


    for dropOff in dropOffs:
        if abs(playerPosition.x - x) < 200 and abs(playerPosition.y - dropOff["location"] - 100) < 35:
            if dropOff["color"] == box["color"]:
                return True

    return False

    
def drawScreenObjects(screen):
    drawConveyer(screen, screen.get_width() / 2 - 50,0,"red",100,screen.get_height())
    drawConveyer(screen, screen.get_width() - 100, 0 ,"blue",100,screen.get_height())
    drawConveyer(screen, 0,0,"blue",100,screen.get_height())
    drawDropOffs(screen)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    dt, count, running, queuedBoxes = 0 , 100, True, []

    player_pos = pygame.Vector2(screen.get_width() / 3, screen.get_height() / 2)    # defines player position
    player2_pos = pygame.Vector2(screen.get_width() / 1.5, screen.get_height() / 2) # defines player position

    player_one_box = False # defines box player one is holding
    player_two_box = False # defines box player two is holding

    PLAYER_RADIUS = 40  # Defining the Size of the player

    # while game is running
    while running:
        screen.fill("white")
        ## draw coveyer table
        drawScreenObjects(screen)
        count +=1 # count to send new boxes in conveyer

        # creates boxes every 100 count
        if count > 100 :
            boxColors = ["orange","green","cyan","pink","purple","brown","gray"]

            randomPoints = random.randrange(1,4,1)
            box_is_bomb = random.random() < 0.1 #10% chance of bomb
            queuedBoxes.append({"rect": pygame.Rect(screen.get_width() / 2 - 25, -50, 55, 55), "points": randomPoints,"color":random.choice(boxColors), "box_is_bomb": box_is_bomb})
            count = 0
        
                
        # Player picks boxes
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # PLayer one pick / drop box
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if(player_one_box): # if player is holding box then drop box 
                        boxDropped = dropBox(screen,True,player_pos,player_one_box)
                        if(boxDropped):
                            # What happens when player drops box off
                            player_one_box = False
                    else: # if player is NOT holding box then drop box 
                        newBoxes = pickBox(queuedBoxes, player_pos)
                        queuedBoxes = newBoxes["newQueue"]
                        if newBoxes["boxPicked"] != False:
                            player_one_box = newBoxes["boxPicked"]
                            player_one_box["rect"].y = player_pos.y - 100
                            player_one_box["rect"].x = player_pos.x - 30

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SLASH:
                    if(player_two_box):
                        dropBox(screen,True,player2_pos, player_two_box)
                    else:
                        newBoxes = pickBox( queuedBoxes, player2_pos)
                        queuedBoxes = newBoxes["newQueue"]
                        if newBoxes["boxPicked"] != False:
                            player_two_box = newBoxes["boxPicked"]
                            player_two_box["rect"].y = player2_pos.y -100
                            player_two_box["rect"].x = player2_pos.x -30
        if player_one_box and "box_is_bomb" in player_one_box and player_one_box["box_is_bomb"] : #bomb boxes explode after 4 secs without deposit
            current_time = time.time()
            if current_time - player_one_box["pickup_time"] > 4:
                #print("Bomb")#this can be replaced with visual and sound effects
                player_one_box = False
        # draw and move boxes on conveyer
        conveyBoxes(queuedBoxes, screen)
        
        # Draw player position
        pygame.draw.circle(screen, "purple", player_pos, 40)
        pygame.draw.circle(screen, "green", player2_pos, 40)


        if(player_one_box):
            pygame.draw.rect(screen, player_one_box["color"], player_one_box["rect"])
        if(player_two_box):
            pygame.draw.rect(screen, player_two_box["color"], player_two_box["rect"])
            
            
        if(len(queuedBoxes) > 8):
            del queuedBoxes[0]
        
        #player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 3
            if player_one_box != False:
                player_one_box["rect"].y -= 3
        if keys[pygame.K_s]:
            player_pos.y += 3
            if player_one_box != False:
                player_one_box["rect"].y += 3
        if keys[pygame.K_a]: 
            player_pos.x -= 3
            if player_one_box != False:
                player_one_box["rect"].x -= 3
        if keys[pygame.K_d]:
            player_pos.x += 3
            if player_one_box != False:

                player_one_box["rect"].x += 3  
        if keys[pygame.K_UP]:
            player2_pos.y -= 3
            if player_two_box != False:
                player_two_box["rect"].y -= 3
        if keys[pygame.K_DOWN]:
            player2_pos.y += 3
            if player_two_box != False:
                player_two_box["rect"].y += 3
        if keys[pygame.K_LEFT]: 
            player2_pos.x -= 3
            if player_two_box != False:
                player_two_box["rect"].x -= 3
        if keys[pygame.K_RIGHT]:
            player2_pos.x += 3
            if player_two_box != False:
                player_two_box["rect"].x += 3                      
                player_one_box["rect"].x += 3 

        if player_pos.x > screen.get_width() / 2 - 50 - PLAYER_RADIUS:
            player_pos.x = screen.get_width() / 2 - 50 - PLAYER_RADIUS

        if player_pos.x < 50 + 100 + PLAYER_RADIUS:
            player_pos.x = 50 + 100 + PLAYER_RADIUS


        if player_pos.x < PLAYER_RADIUS:    #Restricts the player from moving of the left side of the screen
            player_pos.x = PLAYER_RADIUS
        if player_pos.x > screen.get_width() - PLAYER_RADIUS:   #Restricts the player from moving of the right side of the screen
            player_pos.x = screen.get_width() - PLAYER_RADIUS
        if player_pos.y < PLAYER_RADIUS: #Restricts the player from moving of the top of the screen
            player_pos.y = PLAYER_RADIUS
        if player_pos.y > screen.get_height() - PLAYER_RADIUS: #Restricts the player from moving of the bottom of the screen
            player_pos.y = screen.get_height() - PLAYER_RADIUS

        # Keeps the box centered over the character
        if player_one_box:
            player_one_box["rect"].x = player_pos.x - player_one_box["rect"].width // 2
            player_one_box["rect"].y = player_pos.y - player_one_box["rect"].height - 10

        # pygame.draw.rect(screen,"green", player_one_box)
        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        dt = clock.tick(100) / 1000

    pygame.quit()
    

if __name__ == "__main__":
    main()

