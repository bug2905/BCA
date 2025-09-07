# reaction_time.py
# Save as reaction_time.py
# Controls:
#  - Press SPACE when screen turns green, or click
#  - Press R to restart, Q to quit

import pygame, random, time, sys

pygame.init()
W, H = 600, 400
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Reaction Time Test")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 28)

BG = (40,40,40)

state = "ready"  # "ready" -> waiting -> "go" -> result
waiting_until = 0
start_time = 0
reaction = None
best = None

running = True
while running:
    dt = clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                running = False
            if e.key == pygame.K_r:
                state = "ready"; reaction = None
            if e.key == pygame.K_SPACE:
                if state == "ready":
                    # start a waiting period with random delay
                    waiting_until = pygame.time.get_ticks() + random.randint(1200, 3500)
                    state = "waiting"
                elif state == "go":
                    # record reaction
                    reaction = pygame.time.get_ticks() - start_time
                    if best is None or reaction < best:
                        best = reaction
                    state = "result"
        if e.type == pygame.MOUSEBUTTONDOWN:
            # treat clicks like space
            if state == "ready":
                waiting_until = pygame.time.get_ticks() + random.randint(1200, 3500)
                state = "waiting"
            elif state == "go":
                reaction = pygame.time.get_ticks() - start_time
                if best is None or reaction < best:
                    best = reaction
                state = "result"

    # state transitions
    now = pygame.time.get_ticks()
    if state == "waiting" and now >= waiting_until:
        state = "go"
        start_time = pygame.time.get_ticks()

    # draw
    if state == "ready":
        screen.fill((50,50,80))
        txt = FONT.render("Press SPACE or Click to start", True, (230,230,230))
        screen.blit(txt, (W//2-170, H//2-40))
    elif state == "waiting":
        screen.fill((200,50,50))  # red - get ready
        screen.blit(FONT.render("Wait for green ...", True, (255,255,255)), (W//2-120, H//2-40))
    elif state == "go":
        screen.fill((40,180,60))  # green - go!
        screen.blit(FONT.render("GO! Press SPACE / Click now!", True, (10,10,10)), (W//2-170, H//2-40))
    elif state == "result":
        screen.fill((30,30,40))
        if reaction is not None:
            screen.blit(FONT.render(f"Reaction: {reaction} ms", True, (255,255,120)), (W//2-150, H//2-60))
            screen.blit(FONT.render(f"Best: {best} ms", True, (160,255,160)), (W//2-120, H//2))
        screen.blit(FONT.render("Press R to try again. Q to quit.", True, (200,200,200)), (W//2-190, H//2+60))

    # footer
    pygame.draw.rect(screen, (20,20,20), (0, H-34, W, 34))
    screen.blit(FONT.render("Reaction Time Test - Simple Demo", True, (200,200,200)), (10, H-30))

    pygame.display.flip()

pygame.quit()
sys.exit()
