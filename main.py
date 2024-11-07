import pygame
import random

def drawConveyer(screen):
    return pygame.draw.rect(screen, "red", pygame.Rect(screen.get_width() / 2 - 50, 0, 100, screen.get_height() - 100))

def conveyBoxes(queuedBoxes, screen):
    conveyerVelocity = pygame.math.Vector2(1, 1)
    for box in queuedBoxes:
        if len(queuedBoxes) < 7:
            box["rect"].y += int(conveyerVelocity.y)
        # draw boxes on scree
        pygame.draw.rect(screen,"blue", box["rect"])    

def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    dt,count, running, queuedBoxes = 0 , 100, True, []
    player_pos = pygame.Vector2(screen.get_width() / 3, screen.get_height() / 2)
    
    # while game is running
    while running:
        count +=1
        ## creates boxes every 100 frames if boxes can fit in conveyer belt
        if count > 100 and len(queuedBoxes) < 7:
            count = 0
            randomPoints = random.randrange(1,5,1)
            queuedBoxes.append({"rect": pygame.Rect(screen.get_width() / 2 - 25, 20, 55, 55), "points": randomPoints})
            print("draw")

        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")
        # Draw player position
        pygame.draw.circle(screen, "purple", player_pos, 40)
        
        ## draw coveyer table
        drawConveyer(screen)
        
        # draw and move boxes on conveyer
        if len(queuedBoxes) > 1:  
            conveyBoxes(queuedBoxes, screen)
            
        #player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 300 * dt
        if keys[pygame.K_s]:
            player_pos.y += 300 * dt
        if keys[pygame.K_a]:
            player_pos.x -= 300 * dt
        if keys[pygame.K_d]:
            player_pos.x += 300 * dt

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
    pygame.quit()


    


if __name__ == "__main__":
    main()


    print("Hello World")

    
