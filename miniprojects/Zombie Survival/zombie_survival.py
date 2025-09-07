# zombie_survival.py
# Save as zombie_survival.py
# Controls:
#  - Move: WASD or Arrow keys
#  - Shoot: Left mouse button
#  - R to restart, Q to quit

import pygame, random, math, sys, time

pygame.init()
W, H = 900, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Zombie Survival")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 20)
BIG = pygame.font.SysFont("Arial", 28)

BG = (40,40,30)
PLAYER_COLOR = (120,200,255)
ZOMBIE_COLOR = (120,200,100)
BULLET_COLOR = (255,220,80)
HEALTH_COLOR = (200,60,60)

# Player
player = {"x": W//2, "y": H//2, "r": 14, "speed": 4, "hp": 100}
bullets = []
zombies = []
score = 0
spawn_timer = 0
game_over = False
start_time = time.time()

def spawn_zombie():
    edge = random.choice(["top","bottom","left","right"])
    if edge == "top":
        x = random.randint(0, W); y = -20
    elif edge == "bottom":
        x = random.randint(0, W); y = H+20
    elif edge == "left":
        x = -20; y = random.randint(0, H)
    else:
        x = W+20; y = random.randint(0, H)
    speed = 0.7 + random.random()*0.9 + score*0.01
    hp = 18 + random.randint(-4,8) + score//8
    zombies.append({"x": x, "y": y, "speed": speed, "hp": hp, "r": 14})

def reset():
    global bullets, zombies, score, spawn_timer, game_over, start_time
    bullets = []
    zombies = []
    score = 0
    spawn_timer = 0
    player["x"], player["y"], player["hp"] = W//2, H//2, 100
    game_over = False
    start_time = time.time()

# Main loop
running = True
while running:
    dt = clock.tick(60)
    screen.fill(BG)
    mx,my = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                running = False
            if e.key == pygame.K_r:
                reset()
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1 and not game_over:
                # fire bullet toward mouse
                angle = math.atan2(my - player["y"], mx - player["x"])
                bullets.append({"x": player["x"], "y": player["y"], "vx": math.cos(angle)*10, "vy": math.sin(angle)*10, "ttl": 60})

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player["y"] -= player["speed"]
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player["y"] += player["speed"]
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player["x"] -= player["speed"]
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player["x"] += player["speed"]
        # clamp
        player["x"] = max(10, min(W-10, player["x"]))
        player["y"] = max(10, min(H-10, player["y"]))

    # spawn zombies
    spawn_timer += 1
    if spawn_timer > max(20, 80 - score//2):
        spawn_timer = 0
        spawn_zombie()

    # update bullets
    for b in bullets[:]:
        b["x"] += b["vx"]; b["y"] += b["vy"]
        b["ttl"] -= 1
        if b["ttl"] <= 0 or b["x"] < -10 or b["x"] > W+10 or b["y"] < -10 or b["y"] > H+10:
            bullets.remove(b)

    # update zombies
    for z in zombies[:]:
        dx = player["x"] - z["x"]; dy = player["y"] - z["y"]
        dist = math.hypot(dx, dy)
        if dist != 0:
            z["x"] += dx/dist * z["speed"]
            z["y"] += dy/dist * z["speed"]

        # collision with player
        if math.hypot(player["x"]-z["x"], player["y"]-z["y"]) < player["r"] + z["r"]:
            # damage over time
            player["hp"] -= 0.35
            if player["hp"] <= 0:
                game_over = True

        # bullets hit zombie
        for b in bullets[:]:
            if math.hypot(b["x"]-z["x"], b["y"]-z["y"]) < z["r"]+4:
                z["hp"] -= 18
                try: bullets.remove(b)
                except: pass
                if z["hp"] <= 0:
                    try: zombies.remove(z)
                    except: pass
                    score += 1
                    # small chance to drop health
                    if random.random() < 0.05:
                        player["hp"] = min(100, player["hp"] + 10)
                    break

    # draw bullets
    for b in bullets:
        pygame.draw.circle(screen, BULLET_COLOR, (int(b["x"]), int(b["y"])), 4)

    # draw zombies
    for z in zombies:
        # body
        pygame.draw.circle(screen, ZOMBIE_COLOR, (int(z["x"]), int(z["y"])), z["r"])
        # eyes
        pygame.draw.circle(screen, (20,20,20), (int(z["x"]-4), int(z["y"]-4)), 3)
        pygame.draw.circle(screen, (20,20,20), (int(z["x"]+4), int(z["y"]-4)), 3)
        # hp
        hp_w = int((z["hp"]/ (20+score//8 + 8))* (z["r"]*2))
        pygame.draw.rect(screen, (255,0,0), (z["x"]-z["r"], z["y"]-z["r"]-8, z["r"]*2, 4))
        pygame.draw.rect(screen, (0,255,0), (z["x"]-z["r"], z["y"]-z["r"]-8, hp_w, 4))

    # draw player
    pygame.draw.circle(screen, PLAYER_COLOR, (int(player["x"]), int(player["y"])), player["r"])
    # draw aim line
    pygame.draw.line(screen, (200,200,200), (player["x"], player["y"]), (mx, my), 1)

    # HUD
    elapsed = int(time.time() - start_time)
    pygame.draw.rect(screen, (20,20,20), (0,0,W,36))
    screen.blit(FONT.render(f"HP: {int(player['hp'])}   Score: {score}   Time: {elapsed}s   Zombies: {len(zombies)}", True, (230,230,230)), (10,8))
    screen.blit(FONT.render("Move: WASD/Arrows  Shoot: Mouse  R restart  Q quit", True, (200,200,200)), (430,8))

    if game_over:
        screen.blit(BIG.render("YOU DIED! Press R to restart or Q to quit", True, (255,80,80)), (W//2-260, H//2-20))

    pygame.display.flip()

pygame.quit()
sys.exit()
