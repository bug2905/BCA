# bike_stunt.py
import pygame, random, sys, math, time
pygame.init()
W, H = 900, 480
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Bike Stunt")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 22)
BIG = pygame.font.SysFont("Arial", 30)

bike = pygame.Rect(120, H-120, 56, 26)
vel_y = 0
gravity = 0.8
on_ground = True
score = 0
obstacles = []  # ramps/spikes, each dict: {"x":, "type": "ramp"/"spike"}
stars = []
spawn_timer = 0
game_over = False
start_time = time.time()

def spawn_obstacle():
    x = W + random.randint(60, 320)
    if random.random() < 0.6:
        obstacles.append({"x": x, "type": "ramp", "w": random.randint(80,140)})
    else:
        obstacles.append({"x": x, "type": "spike", "w": 36})

def spawn_star():
    x = W + random.randint(40, 300)
    y = random.randint(120, H-200)
    stars.append({"x": x, "y": y})

def reset():
    global bike, vel_y, on_ground, score, obstacles, stars, spawn_timer, game_over, start_time
    bike.x, bike.y = 120, H-120
    vel_y = 0; on_ground = True; score = 0
    obstacles = []; stars = []; spawn_timer = 0; game_over = False
    start_time = time.time()

running = True
while running:
    dt = clock.tick(60)
    screen.fill((120,180,255))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                running = False
            if e.key == pygame.K_r:
                reset()
            if e.key == pygame.K_SPACE and on_ground and not game_over:
                vel_y = -15
                on_ground = False

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] and bike.x > 40:
            bike.x -= 5
        if keys[pygame.K_RIGHT] and bike.right < W-40:
            bike.x += 5

        # gravity
        vel_y += gravity
        bike.y += vel_y
        if bike.bottom >= H-40:
            bike.bottom = H-40
            vel_y = 0
            on_ground = True

        # spawn
        spawn_timer += 1
        if spawn_timer > 30:
            spawn_timer = 0
            if random.random() < 0.6:
                spawn_obstacle()
            else:
                spawn_star()

        # move obstacles & stars
        for ob in obstacles[:]:
            ob["x"] -= 7
            if ob["x"] < -200:
                obstacles.remove(ob); score += 3
            # collision checks
            if ob["type"] == "spike":
                spike_rect = pygame.Rect(ob["x"], H-60, ob["w"], 40)
                if spike_rect.colliderect(bike):
                    game_over = True
            else:
                ramp_rect = pygame.Rect(ob["x"], H-60-ob["w"]//6, ob["w"], ob["w"]//6)
                # simple ramp collision: if bike intersects ramp base while falling slowly, bounce
                if bike.colliderect(ramp_rect) and bike.bottom <= ramp_rect.top + 12 and vel_y >= -2:
                    vel_y = -12  # bounce as a stunt
                    on_ground = False

        for s in stars[:]:
            s["x"] -= 7
            if pygame.Rect(s["x"]-10, s["y"]-10, 20, 20).colliderect(bike):
                try: stars.remove(s)
                except: pass
                score += 20
            elif s["x"] < -20:
                try: stars.remove(s)
                except: pass

    # draw ground
    pygame.draw.rect(screen, (80,180,90), (0, H-40, W, 40))
    # draw obstacles
    for ob in obstacles:
        if ob["type"] == "spike":
            # spikes as triangles
            x = ob["x"]; w = ob["w"]
            for i in range(5):
                px = x + i*(w//5)
                pygame.draw.polygon(screen, (150,40,40), [(px, H-40), (px + w//10, H-40), (px + w//20, H-60)])
        else:
            x = ob["x"]; w = ob["w"]
            ramp = pygame.Rect(x, H-60-w//6, w, w//6)
            pygame.draw.rect(screen, (100,70,40), ramp)
            pygame.draw.polygon(screen, (120,80,50), [(x, H-60), (x+w, H-60), (x+w, H-60-w//6)])

    # draw stars
    for s in stars:
        pygame.draw.circle(screen, (255,220,60), (int(s["x"]), int(s["y"])), 10)
        pygame.draw.circle(screen, (255,255,255), (int(s["x"])+3, int(s["y"])-4), 3)

    # draw bike as rectangle + wheel circles, rotate visually based on vel_y sign
    bike_center = (bike.centerx, bike.centery)
    angle = max(-25, min(25, -vel_y*2))
    body_rect = pygame.Rect(0,0, bike.width, bike.height)
    body_rect.center = bike_center
    pygame.draw.rect(screen, (40,120,210), body_rect)
    pygame.draw.circle(screen, (20,20,20), (bike.left+12, bike.bottom-6), 10)
    pygame.draw.circle(screen, (20,20,20), (bike.right-12, bike.bottom-6), 10)

    # HUD
    elapsed = int(time.time() - start_time)
    screen.blit(FONT.render(f"Score: {score}   Time: {elapsed}s", True, (255,255,255)), (10,10))
    screen.blit(FONT.render("Left/Right to move  Space to jump  R restart  Q quit", True, (220,220,220)), (10,34))
    if game_over:
        screen.blit(BIG.render("YOU CRASHED! Press R to restart", True, (255,80,80)), (W//2-220, H//2-20))

    pygame.display.flip()

pygame.quit()
sys.exit()
