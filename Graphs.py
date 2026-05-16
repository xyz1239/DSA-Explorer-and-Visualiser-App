"""
graphs_module.py — BFS / DFS Graph Traversal Visualiser
"""

import pygame
import sys
import math
import time

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
)

# globals
screen    = None
clock     = None
font_node = None

MODULE_COLOURS = {
    "BFS": (80, 180, 255),
    "DFS": (180, 80, 255),
}

# Node colours
NODE_DEFAULT = (45,  45,  75)
NODE_BORDER  = (100, 100, 160)
NODE_START   = (255, 200,  50)
NODE_CURRENT = ( 80, 200, 255)
NODE_QUEUED  = (200, 100, 255)
NODE_VISITED = ( 50, 220, 130)

NODE_R   = 28
BANNER_H = 70
PANEL_W  = 220
GRAPH_W  = WIDTH - PANEL_W


# Graph class
class Graph:
    def __init__(self, directed=False, weighted=False):
        self.graph    = {}
        self.weights  = {}
        self.directed = directed
        self.weighted = weighted

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, vertex1, vertex2, weight=0):
        if vertex1 in self.graph and vertex2 in self.graph:
            self.graph[vertex1].append(vertex2)
            if self.weighted:
                self.weights[(vertex1, vertex2)] = weight
            if not self.directed:
                self.graph[vertex2].append(vertex1)
                if self.weighted:
                    self.weights[(vertex2, vertex1)] = weight
        else:
            print("One or both vertices not found in graph.")


# Graph
def build_demo_graph():
    g = Graph(directed=True, weighted=False)
    for v in ['A', 'B', 'C', 'D']:
        g.add_vertex(v)
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    g.add_edge('C', 'A')
    g.add_edge('C', 'D')
    return g


def compute_positions():
    cx = GRAPH_W // 2
    cy = BANNER_H + (HEIGHT - BANNER_H) // 2
    r  = 180
    return {
        'D': (cx,       cy - r),
        'C': (cx - r,   cy),
        'A': (cx + r,   cy),
        'B': (cx,       cy + r),
    }


# BFS steps
def bfs_steps(graph, start_vertex):
    visited = {start_vertex}
    queue   = [start_vertex]
    while queue:
        vertex = queue.pop(0)
        yield (vertex, list(queue), set(visited))
        for neighbor in graph.graph[vertex]:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                yield (vertex, list(queue), set(visited))
        yield (vertex, list(queue), set(visited))


# DFS steps
def dfs_steps(graph, start_vertex):
    visited = set()
    stack   = [start_vertex]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            yield (vertex, list(stack), set(visited))
            for neighbor in graph.graph[vertex]:
                if neighbor not in visited:
                    stack.append(neighbor)
                    yield (vertex, list(stack), set(visited))
        yield (vertex, list(stack), set(visited))


# Arrow function
def draw_arrow(surf, colour, start, end, node_r, width=2):
    dx   = end[0] - start[0]
    dy   = end[1] - start[1]
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    ux, uy = dx / dist, dy / dist
    s = (int(start[0] + ux * node_r), int(start[1] + uy * node_r))
    e = (int(end[0]   - ux * node_r), int(end[1]   - uy * node_r))
    pygame.draw.line(surf, colour, s, e, width)
    arrow_len = 14
    perp_x, perp_y = -uy, ux
    tip   = e
    base1 = (int(e[0] - ux * arrow_len + perp_x * 5),
             int(e[1] - uy * arrow_len + perp_y * 5))
    base2 = (int(e[0] - ux * arrow_len - perp_x * 5),
             int(e[1] - uy * arrow_len - perp_y * 5))
    pygame.draw.polygon(surf, colour, [tip, base1, base2])


# Panel button
class _PanelButton:
    def __init__(self, label, rect, colour):
        self.label  = label
        self.rect   = pygame.Rect(rect)
        self.colour = colour

    def draw(self, surf, mouse):
        hover = self.rect.collidepoint(mouse)
        col   = tuple(min(255, c + 35) for c in self.colour) if hover else self.colour
        pygame.draw.rect(surf, BG_PANEL, self.rect, border_radius=8)
        pygame.draw.rect(surf, col, self.rect, width=2, border_radius=8)
        lbl = font_button.render(self.label, True, TEXT_PRIMARY if not hover else col)
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))


# run - Standard entry point
def run(ext_screen, ext_clock):
    global screen, clock
    global font_title, font_subtitle, font_button, font_label, font_small, font_node

    screen    = ext_screen
    clock     = ext_clock
    font_node = pygame.font.SysFont("Consolas", 16, bold=True)

    graph     = build_demo_graph()
    positions = compute_positions()

    s = {
        "start":    None,
        "mode":     None,
        "gen":      None,
        "current":  None,
        "frontier": [],
        "visited":  set(),
        "done":     set(),
        "playing":  False,
        "speed":    0.06,
        "last_t":   0.0,
        "finished": False,
    }

    def reset():
        s["gen"]      = None
        s["current"]  = None
        s["frontier"] = []
        s["visited"]  = set()
        s["done"]     = set()
        s["playing"]  = False
        s["finished"] = False

    def start_traversal(mode):
        if s["start"] is None:
            return
        reset()
        s["mode"]    = mode
        s["gen"]     = (bfs_steps if mode == "BFS" else dfs_steps)(graph, s["start"])
        s["playing"] = True

    def advance():
        if s["gen"] is None or s["finished"]:
            return
        try:
            current, frontier, visited = next(s["gen"])
            if s["current"] and s["current"] != current:
                s["done"].add(s["current"])
            s["current"]  = current
            s["frontier"] = frontier
            s["visited"]  = visited
        except StopIteration:
            if s["current"]:
                s["done"].add(s["current"])
            s["current"]  = None
            s["playing"]  = False
            s["finished"] = True

    px = GRAPH_W + 14
    bw = PANEL_W - 28
    hw = (bw - 6) // 2

    btn_bfs   = _PanelButton("Run BFS", (px,      100, bw, 38), MODULE_COLOURS["BFS"])
    btn_dfs   = _PanelButton("Run DFS", (px,      148, bw, 38), MODULE_COLOURS["DFS"])
    btn_pause = _PanelButton("Pause",   (px,      196, bw, 38), (60, 120, 60))
    btn_reset = _PanelButton("Reset",   (px,      244, bw, 38), (120, 60, 60))
    btn_fast  = _PanelButton("Fast",    (px,      300, hw, 34), (60, 140, 80))
    btn_slow  = _PanelButton("Slow",    (px+hw+6, 300, hw, 34), (140, 100, 40))

    running = True
    while running:
        clock.tick(FPS)
        mouse = pygame.mouse.get_pos()
        now   = time.time()

        if s["playing"] and not s["finished"]:
            if now - s["last_t"] >= s["speed"]:
                s["last_t"] = now
                advance()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if mx < GRAPH_W and my > BANNER_H:
                    for v, (nx, ny) in positions.items():
                        if (mx - nx) ** 2 + (my - ny) ** 2 <= NODE_R ** 2:
                            s["start"] = v
                            reset()
                            break

            if btn_bfs.clicked(event):   start_traversal("BFS")
            if btn_dfs.clicked(event):   start_traversal("DFS")
            if btn_pause.clicked(event):
                s["playing"] = not s["playing"]
                s["last_t"]  = now
            if btn_reset.clicked(event):
                s["start"] = None
                s["mode"]  = None
                reset()
            if btn_fast.clicked(event):
                s["speed"] = 0.06
            if btn_slow.clicked(event):
                s["speed"] = 0.30

        # Drawing
        draw_background(screen)
        draw_banner(screen, "Graph Traversal", MODULE_COLOURS["BFS"])

        pygame.draw.rect(screen, (18, 18, 30),
                         (0, BANNER_H, GRAPH_W, HEIGHT - BANNER_H))

        # Edges 
        for v in graph.graph:
            for nb in graph.graph[v]:
                draw_arrow(screen, NODE_BORDER,
                           positions[v], positions[nb], NODE_R, width=2)

        # Nodes — drawn after edges to hide arrow tails
        for v, (nx, ny) in positions.items():
            if v == s["current"]:
                col = NODE_CURRENT
            elif v in s["done"]:
                col = NODE_VISITED
            elif v in s["frontier"]:
                col = NODE_QUEUED
            elif v == s["start"]:
                col = NODE_START
            else:
                col = NODE_DEFAULT

            pygame.draw.circle(screen, col,         (nx, ny), NODE_R)
            pygame.draw.circle(screen, NODE_BORDER, (nx, ny), NODE_R, 2)
            lbl = font_node.render(v, True, (255, 255, 255))
            screen.blit(lbl, lbl.get_rect(center=(nx, ny)))

        # Side panel
        pygame.draw.rect(screen, BG_PANEL, (GRAPH_W, 0, PANEL_W, HEIGHT))
        pygame.draw.line(screen, BORDER, (GRAPH_W, 0), (GRAPH_W, HEIGHT), 2)

        if s["mode"]:
            mc = MODULE_COLOURS[s["mode"]]
            mt = font_button.render(s["mode"], True, mc)
            screen.blit(mt, mt.get_rect(centerx=GRAPH_W + PANEL_W // 2, y=72))
        else:
            nt = font_small.render("select a mode", True, TEXT_MUTED)
            screen.blit(nt, nt.get_rect(centerx=GRAPH_W + PANEL_W // 2, y=76))

        btn_bfs.draw(screen, mouse)
        btn_dfs.draw(screen, mouse)
        btn_pause.label = "Pause" if s["playing"] else "Resume"
        btn_pause.draw(screen, mouse)
        btn_reset.draw(screen, mouse)

        draw_text(screen, "Speed", font_small, TEXT_MUTED, (px, 284))
        btn_fast.draw(screen, mouse)
        btn_slow.draw(screen, mouse)
        spd     = "60ms" if s["speed"] == 0.06 else "300ms"
        spd_col = SUCCESS if s["speed"] == 0.06 else WARNING
        spd_lbl = font_small.render(spd, True, spd_col)
        screen.blit(spd_lbl, spd_lbl.get_rect(centerx=GRAPH_W + PANEL_W // 2, y=340))

        ly = 360
        draw_text(screen, "Legend", font_small, TEXT_MUTED, (px, ly)); ly += 18
        for col, lbl in [
            (NODE_DEFAULT, "Unvisited"),
            (NODE_START,   "Start"),
            (NODE_CURRENT, "Current"),
            (NODE_QUEUED,  "Queue/Stack"),
            (NODE_VISITED, "Visited"),
        ]:
            pygame.draw.circle(screen, col, (px + 8, ly + 7), 7)
            draw_text(screen, lbl, font_small, TEXT_MUTED, (px + 22, ly))
            ly += 18

        if s["finished"]:
            msg = font_label.render(f"{s['mode']} complete!", True, SUCCESS)
            screen.blit(msg, (GRAPH_W // 2 - msg.get_width() // 2, HEIGHT - 36))
        elif s["playing"]:
            msg = font_label.render(f"Running {s['mode']}...", True, ACCENT)
            screen.blit(msg, (GRAPH_W // 2 - msg.get_width() // 2, HEIGHT - 36))
        else:
            msg = font_label.render("ESC — back to menu", True, TEXT_MUTED)
            screen.blit(msg, (GRAPH_W // 2 - msg.get_width() // 2, HEIGHT - 36))

        pygame.display.flip()