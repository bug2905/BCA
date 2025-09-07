# tower_defense.py
# Save as tower_defense.py
# Controls:
#  - Left click on valid ground to place tower (cost shown)
#  - Press R to start next wave, Q to quit

import pygame, math, random, sys

pygame.init()
W, H = 900, 520
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Tower Defense - Simple")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 18)

# Colors
BG = (30, 30, 40)
PATH_COLOR = (100, 100, 110)
TOWER_COLOR = (60, 170, 80)
ENEMY_COLOR = (200, 60, 60)
BULLET_COLOR = (255, 220, 60)
UI_COLOR = (200, 200, 220)

# Game variables
money = 200
lives = 10
score = 0
wave = 0
wave_active = False

# Path (list of points enemy will follow)
path = [(0, 240), (160, 240), (160, 80), (420, 80), (420, 360), (700, 360), (900, 360)]

# Helper: draw path as thick line/road
def draw_path():
    for i in range(len(path)-1):
        pygame.draw.line(screen, PATH_COLOR, path[i], path[i+1], 60)
    # center line for clarity
    for i in range(len(path)-1):
        pygame.draw.line(screen, (160,160,160), path[i], path[i+1], 2)

# Enemy class
class Enemy:
    def __init__(self, hp=10, speed=1.2):
        self.hp = hp
        self.max_hp = hp
        self.speed = speed
        self.pos = list(path[0])
        self.seg = 0  # current segment index
        self.radius = 14

    def update(self):
        if self.seg >= len(path)-1:
            return False  # reached end
        target = path[self.seg+1]
        dx = target[0] - self.pos[0]
        dy = target[1] - self.pos[1]
        dist = math.hypot(dx, dy)
        if dist < 1:
            self.seg += 1
        else:
            self.pos[0] += dx / dist * self.speed
            self.pos[1] += dy / dist * self.speed
        return True

    def draw(self, surf):
        x, y = int(self.pos[0]), int(self.pos[1])
        pygame.draw.circle(surf, ENEMY_COLOR, (x, y), self.radius)
        # hp bar
        hp_w = int(28 * (self.hp / self.max_hp))
        pygame.draw.rect(surf, (255,0,0), (x-14, y-20, 28, 4))
        pygame.draw.rect(surf, (0,255,0), (x-14, y-20, hp_w, 4))

# Tower class
class Tower:
    def __init__(self, x, y):
        self.x = x; self.y = y
        self.range = 120
        self.rate = 30  # frames per shot
        self.timer = 0
        self.damage = 6
        self.cost = 60

    def update(self, enemies, bullets):
        if self.timer > 0:
            self.timer -= 1
        else:
            # find nearest enemy within range
            target = None
            bestd = 9999
            for e in enemies:
                d = math.hypot(self.x - e.pos[0], self.y - e.pos[1])
                if d <= self.range and d < bestd:
                    bestd = d; target = e
            if target:
                # shoot bullet (simple homing by velocity)
                angle = math.atan2(target.pos[1]-self.y, target.pos[0]-self.x)
                bullets.append({"x": self.x, "y": self.y, "vx": math.cos(angle)*8, "vy": math.sin(angle)*8, "d": self.damage})
                self.timer = self.rate

    def draw(self, surf):
        pygame.draw.circle(surf, TOWER_COLOR, (self.x, self.y), 16)
        # optional: range circle (semi-transparent)
        s = pygame.Surface((self.range*2, self.range*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (100,100,150,40), (self.range, self.range), self.range)
        surf.blit(s, (self.x-self.range, self.y-self.range))

# Game lists
enemies = []
towers = []
bullets = []

# Precompute allowed tower placement area (not on path)
def point_on_road(px, py):
    # check distance to each path segment centerline
    for i in range(len(path)-1):
        x1,y1 = path[i]; x2,y2 = path[i+1]
        # distance from point to segment
        px_to_seg = abs((y2-y1)*px - (x2-x1)*py + x2*y1 - y2*x1) / (math.hypot(y2-y1, x2-x1)+1e-6)
        # approximate if close to road centerline -> disallow
        if px_to_seg < 28:
            return True
    return False

# Spawn wave
def start_wave(n):
    global wave_active
    for i in range(n):
        hp = 8 + wave*2
        spd = 0.9 + wave*0.12 + random.random()*0.4
        enemies.append({"ent": Enemy(hp, spd), "delay": i*28})
    wave_active = True

# Main loop
running = True
spawned = 0
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
            if e.key == pygame.K_r and not wave_active:
                wave += 1
                start_wave(6 + wave*2)
            if e.key == pygame.K_c:
                # clear towers refund partially
                for t in towers:
                    money += t.cost//2
                towers.clear()

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            # place tower if enough money and not on road and not colliding with other towers
            if money >= 60 and not point_on_road(mx,my):
                ok = True
                for t in towers:
                    if math.hypot(t.x-mx, t.y-my) < 36:
                        ok = False; break
                if ok:
                    towers.append(Tower(mx, my))
                    money -= 60

    # Draw path
    draw_path()

    # Update spawn delays and enemy movement
    for e in enemies[:]:
        if e["delay"] > 0:
            e["delay"] -= 1
            continue
        ent = e["ent"]
        alive = ent.update()
        if not alive or ent.seg >= len(path)-1:
            # reached end
            enemies.remove(e)
            lives -= 1
            if lives <= 0:
                # game over message handled later
                pass

    # Update towers (shoot)
    for t in towers:
        t.update([ee["ent"] for ee in enemies if ee["delay"]<=0], bullets)

    # Update bullets
    for b in bullets[:]:
        b["x"] += b["vx"]
        b["y"] += b["vy"]
        # collision with enemies
        hit = False
        for e in enemies[:]:
            if e["delay"]>0: continue
            ent = e["ent"]
            if math.hypot(ent.pos[0]-b["x"], ent.pos[1]-b["y"]) < ent.radius + 6:
                ent.hp -= b["d"]
                try: bullets.remove(b)
                except: pass
                hit = True
                if ent.hp <= 0:
                    score += 10
                    money += 15
                    try:
                        enemies.remove(e)
                    except:
                        pass
                break
        if hit: continue
        # remove bullet off-screen
        if b["x"] < -20 or b["x"] > W+20 or b["y"] < -20 or b["y"] > H+20:
            bullets.remove(b)

    # Draw enemies
    for e in enemies:
        if e["delay"]>0:
            continue
        e["ent"].draw(screen)

    # Draw towers and bullets
    for t in towers:
        t.draw(screen)
    for b in bullets:
        pygame.draw.circle(screen, BULLET_COLOR, (int(b["x"]), int(b["y"])), 5)

    # UI
    pygame.draw.rect(screen, (20,20,30), (0,0,W,48))
    screen.blit(FONT.render(f"Money: ${money}", True, UI_COLOR), (12,10))
    screen.blit(FONT.render(f"Lives: {lives}", True, UI_COLOR), (140,10))
    screen.blit(FONT.render(f"Score: {score}", True, UI_COLOR), (220,10))
    screen.blit(FONT.render(f"Wave: {wave} (Press R to start)", True, UI_COLOR), (340,10))
    screen.blit(FONT.render("Click to place tower ($60). Press C to clear towers (refund 50%). Q to quit", True, UI_COLOR), (520,12))

    # Show placement preview
    color = (120, 230, 140) if (money >= 60 and not point_on_road(mx,my)) else (180,60,60)
    pygame.draw.circle(screen, color, (mx,my), 16, 2)

    # Check game over
    if lives <= 0:
        screen.blit(FONT.render("GAME OVER - You lost all lives. Press Q to quit.", True, (255, 120, 120)), (W//2-210, H//2))
    pygame.display.flip()

pygame.quit()
sys.exit()
