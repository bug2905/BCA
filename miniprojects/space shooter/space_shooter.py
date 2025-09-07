# space_shooter.py
import pygame, random, sys

pygame.init()
W, H = 600, 700
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 22)

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (220,50,50)
GREEN = (50,220,100)
YELLOW = (255,230,100)
BLUE = (100,150,255)

# Player
player_w, player_h = 50, 30
player = pygame.Rect(W//2 - player_w//2, H - 80, player_w, player_h)
player_speed = 6
cooldown = 0

# Bullets and enemies
bullets = []
enemies = []
explosions = []
score = 0
lives = 3
spawn_timer = 0
level = 1

def spawn_enemy():
    w = random.randint(30, 60)
    h = w // 2
    x = random.randint(10, W - w - 10)
    y = random.randint(-120, -40)
    speed = random.uniform(1.5 + level*0.2, 3.0 + level*0.6)
    enemies.append({"rect": pygame.Rect(x,y,w,h), "speed":speed, "hp": 1})

def draw_text(s, x, y, color=WHITE):
    surf = FONT.render(s, True, color)
    screen.blit(surf, (x,y))

# Main loop
running = True
while running:
    dt = clock.tick(60)
    screen.fill((10,10,30))

    # Events
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                running = False
            if e.key == pygame.K_SPACE and cooldown <= 0:
                # fire
                bullets.append(pygame.Rect(player.centerx-3, player.top-10, 6, 12))
                cooldown = 14  # frames

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < W:
        player.x += player_speed

    # Spawn enemies faster as level grows
    spawn_timer += 1
    if spawn_timer > max(15, 60 - level*5):
        spawn_timer = 0
        spawn_enemy()

    # Update bullets
    for b in bullets[:]:
        b.y -= 10
        if b.bottom < 0:
            bullets.remove(b)

    # Update enemies
    for en in enemies[:]:
        en["rect"].y += en["speed"]
        if en["rect"].top > H:
            enemies.remove(en)
            lives -= 1
            # small explosion
            explosions.append([en["rect"].centerx, H-30, 20, 7])
        # collision with bullets
        for b in bullets[:]:
            if en["rect"].colliderect(b):
                bullets.remove(b)
                en["hp"] -= 1
                explosions.append([b.centerx, b.centery, 12, 6])
                if en["hp"] <= 0:
                    enemies.remove(en)
                    score += 10

    # Player collision
    for en in enemies[:]:
        if en["rect"].colliderect(player):
            try:
                enemies.remove(en)
            except ValueError:
                pass
            lives -= 1
            explosions.append([player.centerx, player.centery, 30, 12])

    # Update explosions (simple pulsing circles)
    for ex in explosions[:]:
        ex[2] += 2  # radius
        ex[3] -= 1  # life
        if ex[3] <= 0:
            explosions.remove(ex)

    # Draw stars background for depth effect
    for i in range(40):
        sx = (i*37 + (pygame.time.get_ticks()//10) % W) % W
        sy = (i*23* ( (pygame.time.get_ticks()//100) % 10 +1)) % H
        pygame.draw.circle(screen, (30,30,60), (sx, sy), 1)

    # Draw player (triangle ship)
    pygame.draw.polygon(screen, BLUE, [(player.centerx, player.top), (player.left, player.bottom), (player.right, player.bottom)])
    pygame.draw.rect(screen, (40,40,80), (player.left, player.centery, player_w, 4))  # body shadow

    # Draw bullets
    for b in bullets:
        pygame.draw.rect(screen, YELLOW, b)

    # Draw enemies
    for en in enemies:
        r = en["rect"]
        pygame.draw.ellipse(screen, RED, r)
        # little eyes
        pygame.draw.circle(screen, BLACK, (r.centerx-8, r.centery-4), 3)
        pygame.draw.circle(screen, BLACK, (r.centerx+8, r.centery-4), 3)

    # Draw explosions
    for ex in explosions:
        pygame.draw.circle(screen, (255,200,60), (int(ex[0]), int(ex[1])), int(max(2, ex[2]//2)))
        pygame.draw.circle(screen, (255,80,30), (int(ex[0]), int(ex[1])), int(max(1, ex[2]//4)))

    # Cooldown & difficulty adjust
    if cooldown > 0:
        cooldown -= 1
    # increase level over time
    level = 1 + (score // 100)

    # HUD
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Lives: {lives}", W-110, 10)
    draw_text(f"Level: {level}", W//2-40, 10)

    # Check game over
    if lives <= 0:
        draw_text("GAME OVER - Press R to restart or Q to quit", W//2-240, H//2, RED)
        pygame.display.flip()
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                    waiting = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r:
                        # reset
                        bullets.clear(); enemies.clear(); explosions.clear()
                        score = 0; lives = 3; level = 1
                        waiting = False
                    if e.key == pygame.K_q:
                        running = False
                        waiting = False
        continue

    pygame.display.flip()

pygame.quit()
sys.exit()
