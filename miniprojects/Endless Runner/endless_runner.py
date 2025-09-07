# endless_runner.py
import pygame, random, sys

pygame.init()
W, H = 800, 400
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption("Endless Runner")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 22)

WHITE = (250,250,250)
BLACK = (20,20,20)
GROUND = (50,200,100)
PLAYER_COLOR = (60,120,255)
OBSTACLE_COLOR = (200,60,60)
COIN_COLOR = (255,200,40)

# Player
player = pygame.Rect(80, H-90, 40, 60)
vel_y = 0
gravity = 0.9
is_jumping = False
is_ducking = False

# Ground scroll
scroll_x = 0

# Obstacles and coins
obstacles = []
coins = []
spawn_timer = 0
score = 0
speed = 6
game_over = False

def spawn_obstacle():
    h = random.randint(30, 80)
    obs = pygame.Rect(W+20, H-80-h, 30, h)
    obstacles.append(obs)

def spawn_coin():
    c = pygame.Rect(W+random.randint(20,200), random.randint(120, H-140), 12, 12)
    coins.append(c)

def reset():
    obstacles.clear(); coins.clear()
    player.x = 80; player.y = H-90
    global vel_y, is_jumping, is_ducking, score, speed, spawn_timer, game_over
    vel_y = 0; is_jumping = False; is_ducking = False
    score = 0; speed = 6; spawn_timer = 0; game_over = False

# Main loop
running = True
while running:
    dt = clock.tick(60)
    screen.fill((135,206,250))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE and not is_jumping and not game_over:
                vel_y = -15
                is_jumping = True
            if e.key == pygame.K_DOWN and not is_jumping:
                is_ducking = True
            if e.key == pygame.K_r and game_over:
                reset()
            if e.key == pygame.K_q:
                running = False
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_DOWN:
                is_ducking = False

    if not game_over:
        # gravity & jump
        vel_y += gravity
        player.y += vel_y
        if player.bottom >= H-20:
            player.bottom = H-20
            vel_y = 0
            is_jumping = False

        # duck reduces player height
        if is_ducking:
            player.height = 36
        else:
            player.height = 60

        # spawn obstacles & coins faster over time
        spawn_timer += 1
        if spawn_timer > max(30, 90 - score//5):
            spawn_timer = 0
            if random.random() < 0.65:
                spawn_obstacle()
            else:
                spawn_coin()

        # update obstacles
        for ob in obstacles[:]:
            ob.x -= speed
            if ob.right < 0:
                obstacles.remove(ob)
                score += 2  # reward passing
            if ob.colliderect(player):
                game_over = True

        # update coins
        for c in coins[:]:
            c.x -= speed
            if c.right < 0:
                coins.remove(c)
            if c.colliderect(player):
                coins.remove(c)
                score += 10

        # ground scroll
        scroll_x = (scroll_x - speed) % W

        # speed up slowly
        if score % 50 == 0 and score != 0:
            speed = 6 + score//50

    # Draw ground
    pygame.draw.rect(screen, GROUND, (0, H-20, W, 20))
    for i in range(0, W, 40):
        x = (i + scroll_x) % W
        pygame.draw.rect(screen, (30,160,70), (x, H-20, 20, 20))

    # Draw player (simple running animation by color change)
    pygame.draw.rect(screen, PLAYER_COLOR, (player.x, player.y, player.width, player.height))

    # Draw obstacles & coins
    for ob in obstacles:
        pygame.draw.rect(screen, OBSTACLE_COLOR, ob)
    for c in coins:
        pygame.draw.ellipse(screen, COIN_COLOR, c)

    # HUD
    txt = FONT.render(f"Score: {score}    Speed: {speed}", True, BLACK)
    screen.blit(txt, (10, 10))
    if game_over:
        msg = FONT.render("GAME OVER - Press R to restart or Q to quit", True, (180,30,30))
        screen.blit(msg, (W//2-230, H//2))

    pygame.display.flip()

pygame.quit()
sys.exit()
