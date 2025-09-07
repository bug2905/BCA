# maze_escape.py
import pygame, random, sys, collections, time

pygame.init()
CELL = 24
COLS = 21  # should be odd or use any; maze generation handles it
ROWS = 17
W, H = COLS*CELL, ROWS*CELL + 40
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption("Maze Escape")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 20)

WHITE = (245,245,245)
BLACK = (15,15,15)
PLAYER_COLOR = (60,180,75)
EXIT_COLOR = (230,90,90)
WALL_COLOR = (20,20,60)
PATH_COLOR = (220,220,220)

# Maze representation: grid of cells, each cell has walls: top,right,bottom,left (booleans)
def generate_maze(cols, rows):
    cols_cells = cols
    rows_cells = rows
    grid = [[{"x":x,"y":y,"walls":[True,True,True,True],"vis":False} for x in range(cols_cells)] for y in range(rows_cells)]

    stack = []
    cx, cy = 0, 0
    grid[cy][cx]["vis"] = True
    stack.append(grid[cy][cx])

    while stack:
        current = stack[-1]
        x, y = current["x"], current["y"]
        # neighbors not visited
        neighbors = []
        if y > 0 and not grid[y-1][x]["vis"]:
            neighbors.append(("N", grid[y-1][x]))
        if x < cols_cells-1 and not grid[y][x+1]["vis"]:
            neighbors.append(("E", grid[y][x+1]))
        if y < rows_cells-1 and not grid[y+1][x]["vis"]:
            neighbors.append(("S", grid[y+1][x]))
        if x > 0 and not grid[y][x-1]["vis"]:
            neighbors.append(("W", grid[y][x-1]))
        if neighbors:
            direction, neighbor = random.choice(neighbors)
            # remove wall between current and neighbor
            if direction == "N":
                current["walls"][0] = False
                neighbor["walls"][2] = False
            elif direction == "E":
                current["walls"][1] = False
                neighbor["walls"][3] = False
            elif direction == "S":
                current["walls"][2] = False
                neighbor["walls"][0] = False
            elif direction == "W":
                current["walls"][3] = False
                neighbor["walls"][1] = False
            neighbor["vis"] = True
            stack.append(neighbor)
        else:
            stack.pop()
    return grid

grid = generate_maze(COLS, ROWS)

# Player starts at (0,0)
player_cell = [0, 0]
exit_cell = [COLS-1, ROWS-1]
start_time = time.time()

def cell_rect(cx, cy):
    return pygame.Rect(cx*CELL, cy*CELL, CELL, CELL)

def draw_maze():
    screen.fill(WHITE)
    # draw background squares
    for y in range(ROWS):
        for x in range(COLS):
            rect = cell_rect(x,y)
            pygame.draw.rect(screen, PATH_COLOR, rect.inflate(-2,-2))
    # draw walls
    for y in range(ROWS):
        for x in range(COLS):
            cell = grid[y][x]
            x0 = x*CELL; y0 = y*CELL
            if cell["walls"][0]:
                pygame.draw.line(screen, WALL_COLOR, (x0, y0), (x0+CELL, y0), 3)  # top
            if cell["walls"][1]:
                pygame.draw.line(screen, WALL_COLOR, (x0+CELL, y0), (x0+CELL, y0+CELL), 3)  # right
            if cell["walls"][2]:
                pygame.draw.line(screen, WALL_COLOR, (x0, y0+CELL), (x0+CELL, y0+CELL), 3)  # bottom
            if cell["walls"][3]:
                pygame.draw.line(screen, WALL_COLOR, (x0, y0), (x0, y0+CELL), 3)  # left
    # draw exit
    er = cell_rect(exit_cell[0], exit_cell[1])
    pygame.draw.rect(screen, EXIT_COLOR, er.inflate(-8,-8))

def move_player(dx, dy):
    x,y = player_cell
    cell = grid[y][x]
    # dx,dy correspond to direction: left(-1,0), right(1,0), up(0,-1), down(0,1)
    if dx == -1 and not cell["walls"][3]:
        player_cell[0] += dx
    if dx == 1 and not cell["walls"][1]:
        player_cell[0] += dx
    if dy == -1 and not cell["walls"][0]:
        player_cell[1] += dy
    if dy == 1 and not cell["walls"][2]:
        player_cell[1] += dy

# Helper: shortest path length (BFS) - optional to show hints
def shortest_path_length():
    start = tuple(player_cell)
    goal = tuple(exit_cell)
    q = collections.deque()
    q.append((start,0))
    seen = {start}
    while q:
        (cx,cy),dist = q.popleft()
        if (cx,cy)==goal:
            return dist
        cell = grid[cy][cx]
        # neighbors
        if not cell["walls"][0] and (cx,cy-1) not in seen:
            seen.add((cx,cy-1)); q.append(((cx,cy-1), dist+1))
        if not cell["walls"][1] and (cx+1,cy) not in seen:
            seen.add((cx+1,cy)); q.append(((cx+1,cy), dist+1))
        if not cell["walls"][2] and (cx,cy+1) not in seen:
            seen.add((cx,cy+1)); q.append(((cx,cy+1), dist+1))
        if not cell["walls"][3] and (cx-1,cy) not in seen:
            seen.add((cx-1,cy)); q.append(((cx-1,cy), dist+1))
    return None

# Main loop
running = True
win = False
while running:
    dt = clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                running = False
            if e.key == pygame.K_r:
                grid = generate_maze(COLS, ROWS)
                player_cell = [0,0]
                exit_cell = [COLS-1, ROWS-1]
                start_time = time.time()
                win = False
            if not win:
                if e.key == pygame.K_LEFT:
                    move_player(-1,0)
                if e.key == pygame.K_RIGHT:
                    move_player(1,0)
                if e.key == pygame.K_UP:
                    move_player(0,-1)
                if e.key == pygame.K_DOWN:
                    move_player(0,1)

    draw_maze()
    # Draw player as circle in cell center
    px = player_cell[0]*CELL + CELL//2
    py = player_cell[1]*CELL + CELL//2
    pygame.draw.circle(screen, PLAYER_COLOR, (px,py), CELL//3)

    # HUD
    elapsed = int(time.time() - start_time)
    dist = shortest_path_length()
    draw_text = FONT.render(f"Time: {elapsed}s    Steps-to-exit: {'' if dist is None else dist}    Press R to regenerate, Q to quit", True, BLACK)
    screen.blit(draw_text, (8, ROWS*CELL + 6))

    # Check win
    if player_cell == exit_cell and not win:
        win = True
        win_time = elapsed

    if win:
        wmsg = FONT.render(f"YOU ESCAPED! Time: {win_time}s - Press R to play again", True, (10,120,40))
        screen.blit(wmsg, (W//2 - 180, ROWS*CELL//2))

    pygame.display.flip()

pygame.quit()
sys.exit()
