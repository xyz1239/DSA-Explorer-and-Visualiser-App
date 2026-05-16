# Phase 3 - Puzzle Challenges

import pygame
import sys
import random
import heapq
from main_menu import (
    BG_DARK,
    BG_PANEL,
    ACCENT,
    TEXT_PRIMARY,
    TEXT_MUTED,
    BORDER,
    SUCCESS,
    font_title,
    font_subtitle,
    font_button,
    font_label,
    font_small,
)
from utils import (
    WARNING,
    DANGER,
    WIDTH,
    HEIGHT,
    FPS,
    draw_text,
    draw_text_centred,
    draw_background,
    draw_banner,
    draw_status,
    Button,
    InputBox,
)
from heap_module import MaxHeap

# Module-level globals
screen = None
clock = None

MODULE_COLOURS = {
    "Pathfinding": (80, 200, 255),
    "Event Queue": (220, 100, 200),
    "DP Grid": (160, 220, 100),
}

# Shared cell colours
CELL_EMPTY = BG_PANEL
CELL_WALL = (50, 50, 80)
CELL_START = (80, 220, 160)  # green
CELL_END = (255, 100, 100)  # red
CELL_VISITED = (60, 100, 180)  # blue
CELL_PATH = (255, 200, 60)  # yellow
CELL_FRONTIER = (100, 160, 255)  # light blue


# PUZZLE 1 — PATHFINDING  (Dijkstra / A*)
GRID_COLS = 28
GRID_ROWS = 18
CELL_SIZE = 28
GRID_X = (WIDTH - GRID_COLS * CELL_SIZE) // 2
GRID_Y = 80


def make_grid():
    return [[0] * GRID_COLS for _ in range(GRID_ROWS)]


def draw_grid(surface, grid, start, end, visited, path, frontier):
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            x = GRID_X + c * CELL_SIZE
            y = GRID_Y + r * CELL_SIZE
            cell = (r, c)

            if cell == start:
                colour = CELL_START
            elif cell == end:
                colour = CELL_END
            elif cell in path:
                colour = CELL_PATH
            elif cell in frontier:
                colour = CELL_FRONTIER
            elif cell in visited:
                colour = CELL_VISITED
            elif grid[r][c] == 1:
                colour = CELL_WALL
            else:
                colour = CELL_EMPTY

            pygame.draw.rect(
                surface,
                colour,
                (x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2),
                border_radius=3,
            )

    # Grid border
    pygame.draw.rect(
        surface,
        BORDER,
        (GRID_X, GRID_Y, GRID_COLS * CELL_SIZE, GRID_ROWS * CELL_SIZE),
        1,
    )


def get_neighbours(grid, r, c):
    """Return valid 4-directional neighbours."""
    neighbours = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS and grid[nr][nc] == 0:
            neighbours.append((nr, nc))
    return neighbours


def heuristic(a, b):
    """Manhattan distance heuristic for A*."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def dijkstra_steps(grid, start, end):
    """Generator — yields (visited set, frontier set, path list) each step."""
    dist = {start: 0}
    prev = {}
    pq = [(0, start)]
    visited = set()
    frontier = {start}

    while pq:
        cost, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        frontier.discard(node)

        if node == end:
            # Reconstruct path
            path = []
            cur = end
            while cur in prev:
                path.append(cur)
                cur = prev[cur]
            path.append(start)
            yield visited.copy(), frontier.copy(), list(reversed(path))
            return

        for nb in get_neighbours(grid, *node):
            new_cost = dist[node] + 1
            if nb not in dist or new_cost < dist[nb]:
                dist[nb] = new_cost
                prev[nb] = node
                heapq.heappush(pq, (new_cost, nb))
                frontier.add(nb)

        yield visited.copy(), frontier.copy(), []

    yield visited.copy(), set(), []  # no path found


def astar_steps(grid, start, end):
    """Generator — yields (visited set, frontier set, path list) each step."""
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    prev = {}
    pq = [(f_score[start], start)]
    visited = set()
    frontier = {start}

    while pq:
        _, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)
        frontier.discard(node)

        if node == end:
            path = []
            cur = end
            while cur in prev:
                path.append(cur)
                cur = prev[cur]
            path.append(start)
            yield visited.copy(), frontier.copy(), list(reversed(path))
            return

        for nb in get_neighbours(grid, *node):
            tentative_g = g_score[node] + 1
            if nb not in g_score or tentative_g < g_score[nb]:
                g_score[nb] = tentative_g
                f_score[nb] = tentative_g + heuristic(nb, end)
                prev[nb] = node
                heapq.heappush(pq, (f_score[nb], nb))
                frontier.add(nb)

        yield visited.copy(), frontier.copy(), []

    yield visited.copy(), set(), []


def Int_Pathfinding():
    colour = MODULE_COLOURS["Pathfinding"]
    grid = make_grid()
    start = None
    end = None
    visited = set()
    frontier = set()
    path = []
    gen = None
    done = False
    use_astar = False  # toggle between Dijkstra and A*
    message = "Click to place START, then END, then draw walls. Press Run."
    placing = "start"  # state machine: start → end → walls
    last_step = 0
    STEP_MS = 30

    btn_y = HEIGHT - 52
    run_btn = Button("Run", (40, btn_y, 100, 38), colour)
    reset_btn = Button("Reset", (155, btn_y, 100, 38), WARNING)
    toggle_btn = Button("Dijkstra", (270, btn_y, 140, 38), ACCENT)
    clear_btn = Button("Clr Walls", (425, btn_y, 120, 38), BORDER)

    # Legend
    legend = [
        (CELL_START, "Start"),
        (CELL_END, "End"),
        (CELL_WALL, "Wall"),
        (CELL_VISITED, "Visited"),
        (CELL_FRONTIER, "Frontier"),
        (CELL_PATH, "Path"),
    ]

    drawing_wall = False

    while True:
        now = pygame.time.get_ticks()
        mouse = pygame.mouse.get_pos()

        # Advance pathfinding one step
        if gen is not None and not done and now - last_step >= STEP_MS:
            try:
                visited, frontier, path = next(gen)
                last_step = now
                if path:
                    done = True
                    message = (
                        f"{'A*' if use_astar else 'Dijkstra'} found path "
                        f"— {len(path)} cells"
                    )
            except StopIteration:
                done = True
                message = "No path found!" if not path else message

        draw_background(screen)
        draw_banner(screen, "Pathfinding Puzzle", colour)
        draw_grid(screen, grid, start, end, visited, path, frontier)

        # Legend
        lx = GRID_X + GRID_COLS * CELL_SIZE + 12
        draw_text(screen, "Legend", font_label, TEXT_MUTED, (lx, GRID_Y))
        for i, (col, label) in enumerate(legend):
            ly = GRID_Y + 22 + i * 22
            pygame.draw.rect(screen, col, (lx, ly, 14, 14), border_radius=3)
            draw_text(screen, label, font_label, TEXT_PRIMARY, (lx + 20, ly))

        # Algorithm label
        algo = "A*" if use_astar else "Dijkstra"
        draw_text(screen, f"Algorithm: {algo}", font_label, colour, (lx, GRID_Y + 160))

        for btn in (run_btn, reset_btn, toggle_btn, clear_btn):
            btn.check_hover(mouse)
            btn.draw(screen)

        draw_status(screen, message)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

            # Wall drawing — hold mouse button
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                gc = (mx - GRID_X) // CELL_SIZE
                gr = (my - GRID_Y) // CELL_SIZE
                if 0 <= gr < GRID_ROWS and 0 <= gc < GRID_COLS:
                    cell = (gr, gc)
                    if placing == "start":
                        start = cell
                        placing = "end"
                        message = "Click to place END."
                    elif placing == "end":
                        if cell != start:
                            end = cell
                            placing = "walls"
                            message = "Click/drag to draw walls. Press Run when ready."
                    elif placing == "walls" and gen is None:
                        if cell != start and cell != end:
                            grid[gr][gc] = 1
                            drawing_wall = True

            if event.type == pygame.MOUSEBUTTONUP:
                drawing_wall = False

            if event.type == pygame.MOUSEMOTION and drawing_wall and gen is None:
                mx, my = event.pos
                gc = (mx - GRID_X) // CELL_SIZE
                gr = (my - GRID_Y) // CELL_SIZE
                if 0 <= gr < GRID_ROWS and 0 <= gc < GRID_COLS:
                    cell = (gr, gc)
                    if cell != start and cell != end:
                        grid[gr][gc] = 1

            if run_btn.is_clicked(event):
                if start and end and gen is None:
                    fn = astar_steps if use_astar else dijkstra_steps
                    gen = fn(grid, start, end)
                    message = f"Running {'A*' if use_astar else 'Dijkstra'}..."
                elif not start or not end:
                    message = "Place START and END first."

            if reset_btn.is_clicked(event):
                grid = make_grid()
                start = end = None
                visited = set()
                frontier = set()
                path = []
                gen = None
                done = False
                placing = "start"
                message = "Click to place START, then END, then draw walls."

            if toggle_btn.is_clicked(event):
                use_astar = not use_astar
                toggle_btn.label = "A*" if use_astar else "Dijkstra"
                if gen is None:
                    message = f"Algorithm set to {'A*' if use_astar else 'Dijkstra'}."

            if clear_btn.is_clicked(event):
                grid = make_grid()
                visited = set()
                frontier = set()
                path = []
                gen = None
                done = False
                message = "Walls cleared. Press Run to search again."

        clock.tick(FPS)


# PUZZLE 2 — EVENT QUEUE SIMULATOR


class PriorityEvent:
    """Wraps an event name and priority for use in MaxHeap."""

    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

    def __repr__(self):
        return f"{self.name}(p={self.priority})"


def Int_EventQueue():
    colour = MODULE_COLOURS["Event Queue"]

    # Use MaxHeap from heap_module — key is the event priority
    heap = MaxHeap(key=lambda e: e.priority)
    log = []  # processed events log
    message = "Add events with a name and priority. Extract processes highest priority."

    name_box = InputBox(40, HEIGHT - 100, 200, 36, "Event name:")
    pri_box = InputBox(260, HEIGHT - 100, 100, 36, "Priority (int):")

    add_btn = Button("Add", (380, HEIGHT - 105, 100, 40), colour)
    extract_btn = Button("Extract", (495, HEIGHT - 105, 110, 40), DANGER)
    reset_btn = Button("Reset", (620, HEIGHT - 105, 100, 40), WARNING)

    # Preset events to help the user get started
    presets = [
        ("Server crash", 10),
        ("Low disk space", 5),
        ("User login", 2),
        ("Backup complete", 1),
        ("High CPU", 8),
    ]

    while True:
        mouse = pygame.mouse.get_pos()
        draw_background(screen)
        draw_banner(screen, "Event Queue Simulator", colour)

        # Draw heap array as event cards
        items = heap.items()
        card_w, card_h = 200, 48
        cols = 4
        start_x, start_y = 40, 90

        if not items:
            msg = font_subtitle.render(
                "(heap empty — add events above)", True, TEXT_MUTED
            )
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 200))
        else:
            for i, evt in enumerate(items):
                col_i = i % cols
                row_i = i // cols
                x = start_x + col_i * (card_w + 12)
                y = start_y + row_i * (card_h + 8)

                # Colour by priority
                if evt.priority >= 8:
                    card_col = DANGER
                elif evt.priority >= 5:
                    card_col = WARNING
                else:
                    card_col = colour

                pygame.draw.rect(
                    screen, BG_PANEL, (x, y, card_w, card_h), border_radius=8
                )
                pygame.draw.rect(
                    screen, card_col, (x, y, card_w, card_h), 2, border_radius=8
                )

                # Root marker
                if i == 0:
                    root_lbl = font_label.render("MAX", True, card_col)
                    screen.blit(
                        root_lbl, (x + card_w - root_lbl.get_width() - 6, y + 4)
                    )

                name_surf = font_button.render(evt.name[:18], True, TEXT_PRIMARY)
                pri_surf = font_label.render(
                    f"Priority: {evt.priority}", True, card_col
                )
                screen.blit(name_surf, (x + 8, y + 6))
                screen.blit(pri_surf, (x + 8, y + 28))

        # Processed log
        log_x = WIDTH - 260
        draw_text(screen, "Processed:", font_label, TEXT_MUTED, (log_x, 90))
        pygame.draw.line(screen, BORDER, (log_x, 108), (log_x + 220, 108), 1)
        for i, entry in enumerate(log[-10:]):  # show last 10
            lc = DANGER if entry[1] >= 8 else (WARNING if entry[1] >= 5 else SUCCESS)
            draw_text(
                screen,
                f"{entry[0]} (p={entry[1]})",
                font_label,
                lc,
                (log_x, 114 + i * 20),
            )

        # Preset hint
        hint = font_small.render("Tip: try priorities 1-10", True, TEXT_MUTED)
        screen.blit(hint, (40, HEIGHT - 130))

        name_box.draw(screen)
        pri_box.draw(screen)
        for btn in (add_btn, extract_btn, reset_btn):
            btn.check_hover(mouse)
            btn.draw(screen)
        draw_status(screen, message)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

            name_box.handle_event(event)
            pri_entered = pri_box.handle_event(event)

            if add_btn.is_clicked(event) or pri_entered:
                name = name_box.get()
                pri = pri_box.get()
                if name and pri.lstrip("-").isdigit():
                    evt = PriorityEvent(name, int(pri))
                    heap.insert_heap(evt)
                    message = f"Added '{name}' with priority {pri}."
                    name_box.clear()
                    pri_box.clear()
                else:
                    message = "Enter a name and an integer priority."

            if extract_btn.is_clicked(event):
                try:
                    evt = heap.remove_heap()
                    log.append((evt.name, evt.priority))
                    message = f"Processed: '{evt.name}' (priority {evt.priority})."
                except Exception as e:
                    message = str(e)

            if reset_btn.is_clicked(event):
                heap = MaxHeap(key=lambda e: e.priority)
                log = []
                message = "Queue reset."

        clock.tick(FPS)


# PUZZLE 3 — DYNAMIC PROGRAMMING GRID

DP_COLS = 10
DP_ROWS = 8
DP_CELL = 54
DP_X = (WIDTH - DP_COLS * DP_CELL) // 2
DP_Y = 90


def make_dp_grid(obstacle_prob=0.25):
    """Random grid — 0 = open, 1 = obstacle. Start/end always clear."""
    grid = [
        [1 if random.random() < obstacle_prob else 0 for _ in range(DP_COLS)]
        for _ in range(DP_ROWS)
    ]
    grid[0][0] = 0  # start always open
    grid[DP_ROWS - 1][DP_COLS - 1] = 0  # end always open
    return grid


def dp_path_count(grid):
    """
    Count paths from (0,0) to (rows-1, cols-1) moving only right or down.
    Returns dp table and the reconstructed path (greedy — follows max dp values).
    """
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]

    # Base case
    dp[0][0] = 1 if grid[0][0] == 0 else 0

    # Fill first row
    for c in range(1, cols):
        dp[0][c] = dp[0][c - 1] if grid[0][c] == 0 else 0

    # Fill first column
    for r in range(1, rows):
        dp[r][0] = dp[r - 1][0] if grid[r][0] == 0 else 0

    # Fill rest
    for r in range(1, rows):
        for c in range(1, cols):
            if grid[r][c] == 1:
                dp[r][c] = 0
            else:
                dp[r][c] = dp[r - 1][c] + dp[r][c - 1]

    # Reconstruct path (greedy — follow the larger neighbour)
    path = set()
    if dp[rows - 1][cols - 1] > 0:
        r, c = rows - 1, cols - 1
        path.add((r, c))
        while r > 0 or c > 0:
            if r == 0:
                c -= 1
            elif c == 0:
                r -= 1
            elif dp[r - 1][c] >= dp[r][c - 1]:
                r -= 1
            else:
                c -= 1
            path.add((r, c))

    return dp, path


def dp_fill_steps(grid):
    """Generator — yields dp table state after each cell is filled."""
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = 1 if grid[0][0] == 0 else 0
    yield [row[:] for row in dp], (-1, -1)

    for c in range(1, cols):
        dp[0][c] = dp[0][c - 1] if grid[0][c] == 0 else 0
        yield [row[:] for row in dp], (0, c)

    for r in range(1, rows):
        dp[r][0] = dp[r - 1][0] if grid[r][0] == 0 else 0
        yield [row[:] for row in dp], (r, 0)

    for r in range(1, rows):
        for c in range(1, cols):
            if grid[r][c] == 1:
                dp[r][c] = 0
            else:
                dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
            yield [row[:] for row in dp], (r, c)


def draw_dp_grid(surface, grid, dp, current_cell, path):
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        for c in range(cols):
            x = DP_X + c * DP_CELL
            y = DP_Y + r * DP_CELL
            cell = (r, c)

            if grid[r][c] == 1:
                col = CELL_WALL
            elif cell == (0, 0):
                col = CELL_START
            elif cell == (rows - 1, cols - 1):
                col = CELL_END
            elif cell in path:
                col = CELL_PATH
            elif cell == current_cell:
                col = CELL_FRONTIER
            else:
                col = CELL_EMPTY

            pygame.draw.rect(
                surface, col, (x + 1, y + 1, DP_CELL - 2, DP_CELL - 2), border_radius=4
            )

            # Draw dp value
            val = dp[r][c]
            if val > 0 and grid[r][c] == 0:
                v_surf = font_label.render(str(val), True, TEXT_PRIMARY)
                surface.blit(
                    v_surf,
                    (
                        x + DP_CELL // 2 - v_surf.get_width() // 2,
                        y + DP_CELL // 2 - v_surf.get_height() // 2,
                    ),
                )

    pygame.draw.rect(surface, BORDER, (DP_X, DP_Y, cols * DP_CELL, rows * DP_CELL), 1)


def Int_DPGrid():
    colour = MODULE_COLOURS["DP Grid"]
    grid = make_dp_grid()
    dp = [[0] * DP_COLS for _ in range(DP_ROWS)]
    path = set()
    gen = None
    done = False
    cur_cell = (-1, -1)
    message = "Press Run to fill the DP table. Press New Grid for a new puzzle."
    last_step = 0
    STEP_MS = 80

    btn_y = HEIGHT - 52
    run_btn = Button("Run", (40, btn_y, 100, 38), colour)
    new_btn = Button("New Grid", (155, btn_y, 130, 38), ACCENT)
    reset_btn = Button("Reset", (300, btn_y, 100, 38), WARNING)

    while True:
        now = pygame.time.get_ticks()
        mouse = pygame.mouse.get_pos()

        # Advance DP one step
        if gen is not None and not done and now - last_step >= STEP_MS:
            try:
                dp, cur_cell = next(gen)
                last_step = now
            except StopIteration:
                done = True
                _, path = dp_path_count(grid)
                total = dp[DP_ROWS - 1][DP_COLS - 1]
                message = (
                    f"Done! {total} path(s) from start to end."
                    if total > 0
                    else "No path exists!"
                )

        draw_background(screen)
        draw_banner(screen, "DP Grid Path Counter", colour)
        draw_dp_grid(screen, grid, dp, cur_cell, path)

        # Info panel
        ix = DP_X + DP_COLS * DP_CELL + 16
        draw_text(screen, "How it works:", font_label, colour, (ix, DP_Y))
        draw_text(screen, "Each cell =", font_small, TEXT_MUTED, (ix, DP_Y + 22))
        draw_text(screen, "paths from", font_small, TEXT_MUTED, (ix, DP_Y + 36))
        draw_text(screen, "above + left", font_small, TEXT_MUTED, (ix, DP_Y + 50))
        draw_text(screen, "Move: right", font_small, TEXT_MUTED, (ix, DP_Y + 74))
        draw_text(screen, "or down only", font_small, TEXT_MUTED, (ix, DP_Y + 88))

        # Legend
        draw_text(screen, "Legend:", font_label, TEXT_MUTED, (ix, DP_Y + 120))
        for i, (col, lbl) in enumerate(
            [
                (CELL_START, "Start"),
                (CELL_END, "End"),
                (CELL_WALL, "Obstacle"),
                (CELL_PATH, "Best path"),
                (CELL_FRONTIER, "Current"),
            ]
        ):
            ly = DP_Y + 142 + i * 22
            pygame.draw.rect(screen, col, (ix, ly, 14, 14), border_radius=3)
            draw_text(screen, lbl, font_label, TEXT_PRIMARY, (ix + 20, ly))

        for btn in (run_btn, new_btn, reset_btn):
            btn.check_hover(mouse)
            btn.draw(screen)
        draw_status(screen, message)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

            if run_btn.is_clicked(event):
                if gen is None and not done:
                    gen = dp_fill_steps(grid)
                    message = "Filling DP table..."
                elif done:
                    message = "Press New Grid or Reset to run again."

            if new_btn.is_clicked(event):
                grid = make_dp_grid()
                dp = [[0] * DP_COLS for _ in range(DP_ROWS)]
                path = set()
                gen = None
                done = False
                cur_cell = (-1, -1)
                message = "New grid generated. Press Run."

            if reset_btn.is_clicked(event):
                dp = [[0] * DP_COLS for _ in range(DP_ROWS)]
                path = set()
                gen = None
                done = False
                cur_cell = (-1, -1)
                message = "Reset. Press Run to fill again."

        clock.tick(FPS)


# SUB-MENU


def build_menu_buttons():
    labels = list(MODULE_COLOURS.keys())
    buttons = []
    btn_w, btn_h = 360, 58
    start_x = WIDTH // 2 - btn_w // 2
    start_y = 220
    gap = 72
    for i, label in enumerate(labels):
        rect = (start_x, start_y + i * gap, btn_w, btn_h)
        buttons.append(Button(label, rect, MODULE_COLOURS[label]))
    return buttons


DISPATCH = {
    "Pathfinding": Int_Pathfinding,
    "Event Queue": Int_EventQueue,
    "DP Grid": Int_DPGrid,
}


def draw_submenu(surface, buttons, mouse_pos):
    draw_background(surface)

    title_surf = font_title.render("Puzzle Challenges", True, ACCENT)
    surface.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 60))

    sub_surf = font_subtitle.render("Choose a puzzle to solve", True, TEXT_MUTED)
    surface.blit(sub_surf, (WIDTH // 2 - sub_surf.get_width() // 2, 118))

    pygame.draw.line(
        surface, BORDER, (WIDTH // 2 - 180, 155), (WIDTH // 2 + 180, 155), 1
    )

    for btn in buttons:
        btn.check_hover(mouse_pos)
        btn.draw(surface)

    footer = font_small.render("ESC — return to main menu", True, TEXT_MUTED)
    surface.blit(footer, (WIDTH // 2 - footer.get_width() // 2, HEIGHT - 30))


# Entry point
def run(ext_screen, ext_clock):
    """Called by main_menu.py when the Puzzles button is clicked."""
    global screen, clock
    screen = ext_screen
    clock = ext_clock

    buttons = build_menu_buttons()

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

            for btn in buttons:
                if btn.is_clicked(event):
                    DISPATCH[btn.label]()

        draw_submenu(screen, buttons, mouse_pos)
        pygame.display.flip()
        clock.tick(FPS)
