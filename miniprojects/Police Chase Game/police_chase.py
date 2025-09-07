# police_chase.py
import pygame, random, math, sys, time
pygame.init()
W, H = 1000, 560
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Police Chase")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 20)
BIG = pygame.font.SysFont("Arial", 34)

player = {"x": 150, "y": H//2, "w": 54, "h": 30, "speed": 5}
police = {"x": 50, "y": H//2, "speed": 4}
obstacles = []
nitros = []
score = 0
spawn_timer = 0
police_timer = 0
game_over = False
start_time = time.time()
nitro_active = False
nitro_timer = 0

def spawn_obstacle():
    obstacles.append({"x": W + random.randint(40,300), "y": random.randint(80, H-120), "w": random.randint(40,80), "h": random.randint(20,70)})

def spawn_nitro():
    nitros.append({"x": W + random.randint(30,400), "y": random.randint(80, H-120)})

def reset():
    global player, police, obstacles, nitros, score, spawn_timer, game_over, start_time, nitro_active, nitro_timer
    player["x"], player["y"] = 150, H//2
    police["x"], police["y"] = 50, H//2
    police["speed"] = 4
    obstacles = []; nitros = []; score = 0; spawn_timer = 0; game_over = False; start_time = time.time()
    nitro_active = False; nitro_timer = 0

running = True
while running:
    dt = clock.tick(60)
    screen.fill((16,70,30))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q: running = False
            if e.key == pygame.K_r: reset()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: player["x"] -= player["speed"]
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: player["x"] += player["speed"]
        if keys[pygame.K_UP] or keys[pygame.K_w]: player["y"] -= player["speed"]
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: player["y"] += player["speed"]
        # clamp
        player["x"] = max(40, min(W-100, player["x"]))
        player["y"] = max(60, min(H-60, player["y"]))

        # spawn stuff
        spawn_timer += 1
        if spawn_timer > 40:
            spawn_timer = 0
            if random.random() < 0.7:
                spawn_obstacle()
            else:
                spawn_nitro()

        # move obstacles/nitro
        for ob in obstacles[:]:
            ob["x"] -= 6 + score*0.02
            if ob["x"] < -100:
                obstacles.remove(ob)
                score += 2
            if pygame.Rect(player["x"], player["y"], player["w"], player["h"]).colliderect(pygame.Rect(ob["x"], ob["y"], ob["w"], ob["h"])):
                game_over = True
        for n in nitros[:]:
            n["x"] -= 6
            if n["x"] < -40: nitros.remove(n)
            if pygame.Rect(player["x"], player["y"], player["w"], player["h"]).colliderect(pygame.Rect(n["x"]-10, n["y"]-10, 20, 20)):
                nitros.remove(n); nitro_active = True; nitro_timer = 120

        # police AI: chase towards player's x,y gradually and speed up if far
        dx = player["x"] - police["x"]; dy = player["y"] - police["y"]
        dist = math.hypot(dx, dy)
        police["speed"] = 3.5 + min(3.5, dist/120)
        if nitro_active:
            police["speed"] += 1.5  # police more aggressive when nitro used
        police["x"] += dx/dist * police["speed"] if dist != 0 else 0
        police["y"] += dy/dist * police["speed"] if dist != 0 else 0

        # nitro effect on player
        if nitro_active:
            nitro_timer -= 1
            player_speed_boost = 3
            player["x"] += player_speed_boost if keys[pygame.K_RIGHT] or keys[pygame.K_d] else 0
            if nitro_timer <= 0:
                nitro_active = False

        # police catches player?
        if math.hypot(player["x"]-police["x"], player["y"]-police["y"]) < 36:
            game_over = True

    # draw road background
    for i in range(0, W, 200):
        pygame.draw.rect(screen, (50,50,50), (i, 0, 120, H))
    # draw player
    pygame.draw.rect(screen, (40,150,220), (player["x"], player["y"], player["w"], player["h"]))
    # draw police
    pygame.draw.rect(screen, (220,50,50), (police["x"], police["y"], 50, 28))
    # draw obstacles
    for ob in obstacles:
        pygame.draw.rect(screen, (80,80,80), (ob["x"], ob["y"], ob["w"], ob["h"]))
    # draw nitros
    for n in nitros:
        pygame.draw.circle(screen, (255,200,60), (int(n["x"]), int(n["y"])), 10)
    # HUD
    elapsed = int(time.time() - start_time)
    screen.blit(FONT.render(f"Score: {score}   Time: {elapsed}s", True, (240,240,240)), (12,12))
    screen.blit(FONT.render("WASD/Arrows to move  R restart  Q quit", True, (220,220,220)), (12,36))
    if nitro_active:
        screen.blit(FONT.render("NITRO ACTIVE!", True, (255,220,60)), (W-180, 12))
    if game_over:
        screen.blit(BIG.render("CAUGHT BY POLICE! Press R to restart", True, (255,80,80)), (W//2-300, H//2-20))

    pygame.display.flip()

pygame.quit()
sys.exit()
