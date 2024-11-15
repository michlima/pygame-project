import pygame
import random

def drawRectangle(screen, x,y, width, height):
    #                                                           xAxis              y  width height
    return pygame.draw.rect(screen, "red", pygame.Rect(x, y, width, height))

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
            
            newBoxes.pop(indexRemoved)
            removedBox["rect"].y = player_pos.y - 50
            removedBox["rect"].x = player_pos.x
            break
    return {"newQueue": newBoxes, "boxPicked": removedBox}


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    dt, count, running, queuedBoxes = 0 , 100, True, []
    
    # player position               x Axis                  y axis
    player_pos = pygame.Vector2(screen.get_width() / 3, screen.get_height() / 2)
    player_one_box = False
    
    # while game is running
    while running:
        screen.fill("white")
        ## draw coveyer table
        drawRectangle(screen,screen.get_width() / 2 - 50,0,100,screen.get_height())
        
        count +=1

        ## creates boxes every 100 frames if boxes can fit in conveyer belt
        if count > 100 :
            count = 0
            colors = ["orange", "green", "cyan", "pink", "gray"]
            randomPoints = random.randrange(1,5,1)
            randomColor = random.choice(colors)
            queuedBoxes.append({"rect": pygame.Rect(screen.get_width() / 2 - 25, -50, 55, 55), "points": randomPoints,"color":randomColor})
        
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    newBoxes = pickBox( queuedBoxes, player_pos)
                    queuedBoxes = newBoxes["newQueue"]
                    if newBoxes["boxPicked"] != False:
                        player_one_box = newBoxes["boxPicked"]
                        player_one_box["rect"].y = player_pos.y - 100
                        player_one_box["rect"].x = player_pos.x - 30

        # draw and move boxes on conveyer
        conveyBoxes(queuedBoxes, screen)
        
        # Draw player position
        pygame.draw.circle(screen, "purple", player_pos, 40)

        if(player_one_box):
            pygame.draw.rect(screen, player_one_box["color"], player_one_box["rect"])
            
            
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

        # pygame.draw.rect(screen,"green", player_one_box)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        dt = clock.tick(100) / 1000

    pygame.quit()
    


if __name__ == "__main__":
    main()