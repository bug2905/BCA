# traffic_dodger.py
import pygame, random, sys, time, math

pygame.init()
W, H = 640, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Traffic Dodger")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 20)
BIG = pygame.font.SysFont("Arial", 36)

player = pygame.Rect(W//2-20, H-140, 40, 80)
player_speed = 5
score = 0
coins = []
cars = []
spawn_timer = 0
game_over = False
start_time = time.time()

def spawn_car():
    lane_x = random.randint(80, W-120)
    w = 44; h = 80
    y = -120
    spd = random.uniform(3.5, 7.0)
    cars.append({"rect": pygame.Rect(lane_x, y, w, h), "speed": spd})

def spawn_coin():
    coins.append({"pos": [random.randint(60, W-60), -40], "vy": random.uniform(2.0, 4.0)})

def reset():
    global player, cars, coins, score, spawn_timer, game_over, start_time
    player.x = W//2-20; player.y = H-140
    cars = []; coins = []; score = 0; spawn_timer = 0; game_over = False; start_time = time.time()

running = True
while running:
    dt = clock.tick(60)
    screen.fill((30,30,40))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                running = False
            if e.key == pygame.K_r:
                reset()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] and player.left > 40:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < W-40:
            player.x += player_speed
        if keys[pygame.K_UP]:
            player.y -= 4
        if keys[pygame.K_DOWN]:
            player.y += 4

        spawn_timer += 1
        if spawn_timer > 20:
            spawn_timer = 0
            if random.random() < 0.6:
                spawn_car()
            else:
                spawn_coin()

        # update cars
        for c in cars[:]:
            c["rect"].y += c["speed"]
            if c["rect"].top > H+50:
                cars.remove(c); score += 3
            if c["rect"].colliderect(player):
                game_over = True

        # update coins
        for coin in coins[:]:
            coin["pos"][1] += coin["vy"]
            if coin["pos"][1] > H+10:
                coins.remove(coin)
            if pygame.Rect(coin["pos"][0]-10, coin["pos"][1]-10, 20, 20).colliderect(player):
                coins.remove(coin); score += 15

    # draw road edges and dashed center
    pygame.draw.rect(screen, (50,50,60), (40, 0, W-80, H))
    for y in range(0, H, 40):
        pygame.draw.rect(screen, (200,200,200), (W//2-6, y+10, 12, 20))

    # draw cars
    for c in cars:
        pygame.draw.rect(screen, (200,50,60), c["rect"])
        pygame.draw.rect(screen, (10,10,10), (c["rect"].x+8, c["rect"].y+12, c["rect"].w-16, c["rect"].h-30))
    # draw coins
    for coin in coins:
        pygame.draw.circle(screen, (255,200,60), (int(coin["pos"][0]), int(coin["pos"][1])), 10)
        pygame.draw.circle(screen, (255,255,255), (int(coin["pos"][0])+3, int(coin["pos"][1])-3), 3)

    # draw player
    pygame.draw.rect(screen, (60,160,220), player)
    pygame.draw.rect(screen, (10,10,10), (player.x+8, player.y+12, player.width-16, player.height-30))

    # HUD
    elapsed = int(time.time() - start_time)
    screen.blit(FONT.render(f"Score: {score}   Time: {elapsed}s", True, (240,240,240)), (12,12))
    screen.blit(FONT.render("Arrows to move, R restart, Q quit", True, (200,200,200)), (12,36))

    if game_over:
        screen.blit(BIG.render("CRASH! Press R to restart", True, (255,100,100)), (W//2-160, H//2-20))

    pygame.display.flip()

pygame.quit()
sys.exit()
