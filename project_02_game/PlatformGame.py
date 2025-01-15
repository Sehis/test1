# Example file showing a basic pygame "game loop"
import pygame
import random
import time

# pygame setup
pygame.init()
screen = pygame.display.set_mode((500, 700))
clock = pygame.time.Clock()
running = True
onstage = False
dt = 0
start_1 = pygame.Rect(175, 300, 150, 100)
yes_1 = pygame.Rect(87.5, 400, 150, 100)
no_1 = pygame.Rect(262.5, 400, 150, 100)
roundnumber = 1
player_pos = pygame.Vector2(100, 600)



def START_SCREEN():

    screen.fill("light blue")

    # RENDER YOUR GAME HERE
    screen.blit(begin, (0, 0))
    pygame.draw.rect(screen, "pink", start_1)


    if pygame.font:
        font = pygame.font.Font(None, 64)
        text = font.render("MONKEY JUMP!", True, (10, 10, 10))
        textpos = text.get_rect(centerx=screen.get_width() / 2, y=150)
        screen.blit(text, textpos)

    if pygame.font:
        font = pygame.font.Font(None, 64)
        text = font.render("START", True, "white")
        textpos = text.get_rect(centerx=screen.get_width() / 2, y=325)
        screen.blit(text, textpos)
    # flip() the display to put your work on screen


def stage1():
    global mapData, platforms, goal, roundnumber
    #10 * 1 size, 10 platforms

    #generate the rect's list for all platforms
    platforms.clear()

    #25 x 35 cells
    randPos = []
    for i in range(8):
        rx = random.randint(0,25-10)
        ry = (35-3) // 8 * i + 3
        if i == 0:
            goal = pygame.Vector2(rx+4,ry-1)
        platforms.append(pygame.Rect((rx * 20, ry * 20), (20 * 10, 20)))
        for i in range(10):
            mapData[ry][rx + i] = 1
    # ground
    x, y = 0, 34
    platforms.append(pygame.Rect(((0, 680)), (500, 20)))
    for i in range(25):
        mapData[y][x + i] = 1

def stage2():
    global mapData, platforms, goal, roundnumber
    # 10 * 1 size, 10 platforms
    # generate the rect's list for all platforms
    platforms.clear()
    for i in range(25):
        for j in range(35):
            mapData[j][i] = 0

    # 25 x 35 cells
    randPos = []
    for i in range(8):
        rx = random.randint(0, 25 - 8)
        ry = (35 - 3) // 8 * i + 3
        if i == 0:
            goal = pygame.Vector2(rx + 4, ry - 1)
        platforms.append(pygame.Rect((rx * 20, ry * 20), (20 * 8, 20)))
        for i in range(8):
            mapData[ry][rx + i] = 1
    x, y = 0, 34
    platforms.append(pygame.Rect(((0, 680)), (500, 20)))
    for i in range(25):
        mapData[y][x + i] = 1

def stage3():
    global mapData, platforms, goal, roundnumber
    # 10 * 1 size, 10 platforms
    # generate the rect's list for all platforms
    platforms.clear()
    for i in range(25):
        for j in range(35):
            mapData[j][i] = 0

    # 25 x 35 cells
    randPos = []
    for i in range(6):
        rx = random.randint(0, 25 - 8)
        ry = (35 - 3) // 8 * i + 3
        if i == 0:
            goal = pygame.Vector2(rx + 4, ry - 1)
        platforms.append(pygame.Rect((rx * 20, ry * 20), (20 * 6, 20)))
        for i in range(6):
            mapData[ry][rx + i] = 1

    x, y = 0, 34
    platforms.append(pygame.Rect(((0, 680)), (500, 20)))
    for i in range(25):
        mapData[y][x + i] = 1

def gameScene():
    global timer
    #Creating the visuals, text, etc
    screen.fill((82, 82, 140))
    screen.blit(background,(0,0))
    Round_Number = pygame.Rect(0, 0, 500, 50)
    pygame.draw.rect(screen,(255, 185, 50), Round_Number)

    if pygame.font:
        font = pygame.font.Font(None, 32)
        text = font.render(("Round " + str(roundnumber)), True, (255, 255, 255))
        textpos = text.get_rect(centerx=screen.get_width() / 2, y=15)
        screen.blit(text, textpos)


    #Render map for mapData
    #cell size: 20 x 20
    #cell code: 1 -> plat
    #cell code: 0 -> air
    for i in range(35):
        for j in range(25):
            if mapData[i][j] == 0:
                continue
            elif mapData[i][j] == 1:
                #rect = pygame.Rect((20*j, 20*i),(20,20))
                #pygame.draw.rect(screen, (255, 255, 255), rect)
                screen.blit(pygame.transform.scale(tile['grass_plat'],(20,20)), (20*j, 20*i))

    screen.blit(mouse_touch, pygame.Rect((goal[0] * 20 + 10, goal[1] * 20), (20,20)))
    #Timer

    timer = 20 - int(time.time() - startTime)
    if pygame.font:
        font = pygame.font.Font(None, 50)
        text = font.render(str(timer), True, (255, 255, 255))
        textpos = text.get_rect(centerx=screen.get_width() / 2, y=60)
        screen.blit(text, textpos)

def gameOver():

    screen.fill("Black")

    if pygame.font:
        font = pygame.font.Font(None, 64)
        text = font.render("GAME OVER", True, (255, 0, 0))
        textpos = text.get_rect(centerx=screen.get_width() / 2, y=150)
        screen.blit(text, textpos)

    if pygame.font:
        font = pygame.font.Font(None, 64)
        text = font.render("Play Again?", True, "white")
        textpos = text.get_rect(centerx=screen.get_width() / 2, y=325)
        screen.blit(text, textpos)

    pygame.draw.rect(screen, "green", yes_1)
    pygame.draw.rect(screen, "red", no_1)

    if pygame.font:
        font = pygame.font.Font(None, 64)
        text = font.render("YES", True, "white")
        textpos = text.get_rect(x=130, y=420)
        screen.blit(text, textpos)

    if pygame.font:
        font = pygame.font.Font(None, 64)
        text = font.render("NO", True, "white")
        textpos = text.get_rect(x=310, y=420)
        screen.blit(text, textpos)

#collision check
def collisionCheck():
    for plat in platforms:
        #when the platform is against the player
        if plat.colliderect(pygame.Rect(player_pos,(20,40))):
            #say that the player is touching a platform
            return True

    #outside check... (to prevent it from getting out of frame)
    if player_pos[0] <= -5 or player_pos[0] >= 480:
        return True

    return False

def goalinCheck():
    t = pygame.Rect((goal[0] * 20 + 10, goal[1] * 20), (20,20))
    return t.colliderect(pygame.Rect(pygame.Rect(player_pos, (30, 30))))

#map data (25 x 35 cells, 20px * 20px size for each cell)
# list (2dim)
mapData = [[0]*25 for _ in range(35)]
platforms = []


tile = dict()
tile['grass_plat'] = pygame.image.load('./Tiles/gblock.png').convert_alpha()

mouse_touch = pygame.image.load('./Tiles/mouse.png')
player_image = pygame.image.load('./Tiles/Character.png').convert_alpha()
background = pygame.image.load('./Tiles/Wallpaper.png').convert_alpha()
begin = pygame.image.load('./Tiles/Begin.png').convert_alpha()

yVelo = 0
yAcc = 600
dt = 0.001
onTheGround = False

timer = 20
startTime = time.time()

goal = pygame.Vector2(0,0)


while running:
    if not onstage:
        START_SCREEN()
        screen.blit(player_image,pygame.Rect(pygame.Rect(player_pos, (30, 30))) )

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_pos.y -= 300 * dt

        if keys[pygame.K_DOWN]:
            player_pos.y += 300 * dt

        if keys[pygame.K_LEFT]:
            player_pos.x -= 300 * dt
            if collisionCheck():
                player_pos.x += 300 * dt

        if keys[pygame.K_RIGHT]:
            player_pos.x += 300 * dt
            if collisionCheck():
                player_pos.x -= 300 * dt

        if keys[pygame.K_RETURN]:
            collide = pygame.Rect.colliderect(pygame.Rect(player_pos, (20, 40)), start_1)
            if collide:
                print("!!!")
                player_pos = pygame.Vector2(40, 640)
                onstage = True
                stage1()

    else:
        gameScene()
        screen.blit(player_image, pygame.Rect(pygame.Rect(player_pos, (30, 30))))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and onTheGround:
            yVelo = -400
            player_pos.y += yVelo * dt
            onTheGround = False
            #player_pos.y -= 300 * dt
            #if collisionCheck():
                #player_pos.y += 300 * dt

        if keys[pygame.K_LEFT]:
            player_pos.x -= 300 * dt
            if collisionCheck():
                player_pos.x += 300 * dt

        if keys[pygame.K_RIGHT]:
            player_pos.x += 300 * dt
            if collisionCheck():
                player_pos.x -= 300 * dt

        #gravity effect
        #gravity effect

        #using laws of physics
        yVelo += yAcc * dt
        player_pos.y += yVelo * dt
        if collisionCheck():
            player_pos.y -= yVelo * dt

            if yVelo > 0:
                onTheGround = True
            yVelo = 0


    dt = clock.tick(60) / 1000
    pygame.display.flip()

    if goalinCheck():
        roundnumber += 1

        if roundnumber == 2:
            stage2()
        if roundnumber == 3:
            stage3()

        timer = 20
        player_pos = pygame.Vector2(40, 640)
        startTime = time.time()

    if timer == 0:
        print("gameOver")
        gameOver()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            gameOver()
            screen.blit(player_image, pygame.Rect(pygame.Rect(player_pos, (30, 30))))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player_pos.y -= 300 * dt

            if keys[pygame.K_DOWN]:
                player_pos.y += 300 * dt

            if keys[pygame.K_LEFT]:
                player_pos.x -= 300 * dt

            if keys[pygame.K_RIGHT]:
                player_pos.x += 300 * dt

            if keys[pygame.K_RETURN]:
                collide_1 = pygame.Rect.colliderect(pygame.Rect(player_pos, (20, 40)), yes_1)
                collide_2 = pygame.Rect.colliderect(pygame.Rect(player_pos, (20, 40)), no_1)

                if collide_1:
                    print(":)")
                    player_pos = pygame.Vector2(40, 640)
                    onstage = True
                    START_SCREEN()
                    timer = 20
                    startTime = time.time()
                    break

                elif collide_2:
                    print(":(")
                    running = False
                    break

            dt = clock.tick(60) / 1000
            pygame.display.flip()
                # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


pygame.quit()

