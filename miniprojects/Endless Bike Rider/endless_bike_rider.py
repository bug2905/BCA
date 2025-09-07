# endless_bike_rider.py
import pygame, random, sys, time, math
pygame.init()
W, H = 960, 540
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Endless Bike Rider")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 20)
BIG = pygame.font.SysFont("Arial", 30)

bike = {"x": W//2, "y": H-140, "r": 18, "speed": 6}
obstacles = []
bg_offset = 0
spawn_timer = 0
score = 0
game_over = False
start_time = time.time()

def spawn_obstacle():
    typ = random.choice(["cone", "barrel", "car"])
    x = random.randint(60, W-60)
    obstacles.append({"x": x, "y": -80, "type": typ, "vy": random.uniform(3.5, 6.0)})

def reset():
    global bike, obstacles, spawn_timer, score, game_over, start_time, bg_offset
    bike["x"], bike["y"], bike["speed"] = W//2, H-140, 6
    obstacles = []; spawn_timer = 0; score = 0; game_over = False; start_time = time.time(); bg_offset = 0

running = True
while running:
    dt = clock.tick(60)
    screen.fill((90,180,250))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q: running = False
            if e.key == pygame.K_r: reset()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] and bike["x"] > 60:
            bike["x"] -= 6
        if keys[pygame.K_RIGHT] and bike["x"] < W-60:
            bike["x"] += 6
        if keys[pygame.K_UP]:
            bike["speed"] = min(14, bike["speed"] + 0.1)
        if keys[pygame.K_DOWN]:
            bike["speed"] = max(3, bike["speed"] - 0.2)

        # background parallax
        bg_offset = (bg_offset + bike["speed"]) % W
        for i in range(-1, 2):
            pygame.draw.rect(screen, (80,80,80), (i*W - bg_offset, H-140, W, 160))

        spawn_timer += 1
        if spawn_timer > max(10, 60 - score//10):
            spawn_timer = 0
            spawn_obstacle()

        for ob in obstacles[:]:
            ob["y"] += ob["vy"] + bike["speed"]*0.02
            if ob["y"] > H+80:
                try: obstacles.remove(ob); score += 5
                except: pass
            else:
                # collision
                if math.hypot(bike["x"]-ob["x"], bike["y"]-ob["y"]) < 36:
                    game_over = True

    # road overlay
    pygame.draw.rect(screen, (20,20,20), (0, H-160, W, 160))
    # lane marks
    for i in range(0, W, 40):
        pygame.draw.rect(screen, (200,200,200), (i+10, H-80, 20, 6))

    # obstacles draw
    for ob in obstacles:
        if ob["type"] == "cone":
            pygame.draw.polygon(screen, (230,120,20), [(ob["x"], ob["y"]), (ob["x"]-12, ob["y"]+30), (ob["x"]+12, ob["y"]+30)])
        elif ob["type"] == "barrel":
            pygame.draw.rect(screen, (120,60,20), (ob["x"]-12, ob["y"], 24, 30))
        else:
            pygame.draw.rect(screen, (200,60,60), (ob["x"]-22, ob["y"], 44, 26))

    # draw bike (circle + wheel)
    pygame.draw.circle(screen, (70,160,220), (int(bike["x"]), int(bike["y"])), bike["r"])
    pygame.draw.circle(screen, (30,30,30), (int(bike["x"]-10), int(bike["y"]+14)), 8)
    pygame.draw.circle(screen, (30,30,30), (int(bike["x"]+10), int(bike["y"]+14)), 8)

    # HUD
    elapsed = int(time.time() - start_time)
    screen.blit(FONT.render(f"Score: {score}   Speed: {int(bike['speed'])}   Time: {elapsed}s", True, (240,240,240)), (12,12))
    screen.blit(FONT.render("Arrows to steer  Up/Down to change speed  R restart  Q quit", True, (220,220,220)), (12,36))

    if game_over:
        screen.blit(BIG.render("CRASH! Press R to restart", True, (255,80,80)), (W//2-180, H//2-20))

    pygame.display.flip()

pygame.quit()
sys.exit()
