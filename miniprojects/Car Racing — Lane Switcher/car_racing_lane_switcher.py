# car_racing_lane_switcher.py
import pygame, random, sys, time

pygame.init()
W, H = 480, 700
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Car Racing - Lane Switcher")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 22)
BIG = pygame.font.SysFont("Arial", 34)

LANES = [W//4, W//2, 3*W//4]
player_lane = 1
player_y = H - 140
player_w, player_h = 44, 70
speed = 6
score = 0
game_over = False
spawn_timer = 0
obstacles = []  # each: {"lane":int, "y":float, "speed":float}

def spawn_obstacle(level=1):
    lane = random.choice([0,1,2])
    y = -100
    spd = random.uniform(3+level*0.4, 6+level*0.6)
    obstacles.append({"lane":lane, "y":y, "speed":spd})

def reset():
    global player_lane, obstacles, score, game_over, spawn_timer, speed
    player_lane = 1
    obstacles = []
    score = 0
    game_over = False
    spawn_timer = 0
    speed = 6

running = True
start_time = time.time()
while running:
    dt = clock.tick(60)
    screen.fill((20, 24, 30))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT and not game_over:
                player_lane = max(0, player_lane-1)
            if e.key == pygame.K_RIGHT and not game_over:
                player_lane = min(2, player_lane+1)
            if e.key == pygame.K_r:
                reset()
            if e.key == pygame.K_q:
                running = False

    if not game_over:
        spawn_timer += 1
        level = 1 + score//50
        if spawn_timer > max(20, 60 - level*4):
            spawn_timer = 0
            spawn_obstacle(level)
        for ob in obstacles[:]:
            ob["y"] += ob["speed"]
            if ob["y"] > H + 120:
                obstacles.remove(ob)
                score += 5
            # collision
            if ob["lane"] == player_lane:
                px = LANES[player_lane] - player_w//2
                py = player_y
                ox = LANES[ob["lane"]] - player_w//2
                oy = ob["y"]
                # simple rect collision
                if oy + 60 > py and oy < py + player_h:
                    game_over = True

    # draw road
    pygame.draw.rect(screen, (40,40,40), (W//8, 0, 3*W//4, H))
    # lane separators
    for i in range(1,3):
        x = (LANES[i-1]+LANES[i])//2
        for y in range(0, H, 40):
            pygame.draw.rect(screen, (200,200,200), (x-4, y+10, 8, 24))

    # draw obstacles
    for ob in obstacles:
        x = LANES[ob["lane"]]-player_w//2
        y = int(ob["y"])
        pygame.draw.rect(screen, (180,40,40), (x, y, player_w, player_h))
        pygame.draw.rect(screen, (0,0,0), (x+8, y+18, player_w-16, player_h-26))  # windshield

    # draw player car (triangle/stylized)
    px = LANES[player_lane]
    pygame.draw.polygon(screen, (60,160,220), [(px, player_y), (px-player_w//2, player_y+player_h), (px+player_w//2, player_y+player_h)])
    pygame.draw.rect(screen, (20,20,30), (px-12, player_y+10, 24, 10))

    # HUD
    elapsed = int(time.time() - start_time)
    screen.blit(FONT.render(f"Score: {score}", True, (240,240,240)), (12,12))
    screen.blit(FONT.render(f"Time: {elapsed}s  Speed: {speed}", True, (240,240,240)), (12,36))
    screen.blit(FONT.render("Left/Right to switch lanes  R restart  Q quit", True, (200,200,200)), (12,60))

    if game_over:
        screen.blit(BIG.render("CRASHED! Press R to restart", True, (255,80,80)), (W//2-200, H//2-20))

    pygame.display.flip()

pygame.quit()
sys.exit()
