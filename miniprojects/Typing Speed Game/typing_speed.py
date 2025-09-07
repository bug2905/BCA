# typing_speed.py
# Save as typing_speed.py
# Controls:
#  - Type letters on keyboard, press ENTER to submit a word
#  - Q to quit, R to restart

import pygame, random, sys, time

pygame.init()
W, H = 900, 520
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Typing Speed Game")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Consolas", 26)
BIG = pygame.font.SysFont("Arial", 36)

BG = (25,25,40)
WORD_COLOR = (255,220,100)
INPUT_COLOR = (180,180,255)

words_list = [
    "python","game","player","speed","random","typing","score","keyboard","pygame","challenge",
    "function","variable","loop","condition","string","display","window","object","class","event",
    "desktop","console","project","example","demo","impress","teacher","student","performance","design"
]

falling = []  # each: {"word":str,"x":int,"y":float,"speed":float}
spawn_timer = 0
spawn_rate = 80  # frames
score = 0
lives = 5
input_text = ""
running = True
start_time = time.time()

def spawn_word():
    w = random.choice(words_list)
    x = random.randint(30, W-160)
    speed = 1.2 + random.random()*1.6 + (score/100.0)
    falling.append({"word": w, "x": x, "y": -20.0, "speed": speed})

def reset():
    global falling, spawn_timer, score, lives, input_text, start_time
    falling = []
    spawn_timer = 0
    score = 0
    lives = 5
    input_text = ""
    start_time = time.time()

while running:
    dt = clock.tick(60)
    screen.fill(BG)
    elapsed = int(time.time() - start_time)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                running = False
            if e.key == pygame.K_r:
                reset()
            elif e.key == pygame.K_RETURN:
                # submit input
                matched = None
                for f in falling:
                    if f["word"] == input_text.strip():
                        matched = f; break
                if matched:
                    score += len(matched["word"])*10
                    try:
                        falling.remove(matched)
                    except:
                        pass
                input_text = ""
            elif e.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                if len(input_text) < 24 and e.unicode.isprintable():
                    input_text += e.unicode

    # spawn words faster as score increases
    spawn_timer += 1
    if spawn_timer > max(20, spawn_rate - score//6):
        spawn_timer = 0
        spawn_word()

    # update falling words
    for f in falling[:]:
        f["y"] += f["speed"]
        if f["y"] > H-80:
            falling.remove(f)
            lives -= 1
            if lives <= 0:
                # game over
                pass

    # draw falling words
    for f in falling:
        txt = FONT.render(f["word"], True, WORD_COLOR)
        screen.blit(txt, (f["x"], int(f["y"])))

    # draw input box
    pygame.draw.rect(screen, (10,10,20), (0, H-80, W, 80))
    prompt = BIG.render(f"Type: {input_text}", True, INPUT_COLOR)
    screen.blit(prompt, (20, H-68))

    # HUD
    screen.blit(FONT.render(f"Score: {score}", True, (220,220,220)), (12,10))
    screen.blit(FONT.render(f"Lives: {lives}", True, (220,220,220)), (140,10))
    screen.blit(FONT.render(f"Time: {elapsed}s", True, (220,220,220)), (220,10))
    screen.blit(FONT.render("Press ENTER to submit word. R restart, Q quit.", True, (190,190,190)), (340,12))

    if lives <= 0:
        screen.blit(BIG.render(f"GAME OVER! Score: {score}   Press R to restart", True, (255,120,120)), (W//2-320, H//2-20))

    pygame.display.flip()

pygame.quit()
sys.exit()
