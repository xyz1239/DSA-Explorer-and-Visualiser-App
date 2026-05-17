"""
DSA Explorer and Visualiser
Main Menu Skeleton
"""

import pygame
import sys

# INITIALISATION
pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DSA Explorer & Visualiser")
clock = pygame.time.Clock()
FPS = 60


# COLOUR PALETTE
BG_DARK = (15, 20, 40)
BG_PANEL = (25, 32, 60)
ACCENT = (80, 180, 255)
ACCENT_HOVER = (120, 210, 255)
TEXT_PRIMARY = (230, 235, 255)
TEXT_MUTED = (120, 135, 170)
BORDER = (50, 70, 120)
SUCCESS = (80, 220, 160)

MODULE_COLOURS = {
    "Data Structures": (100, 160, 255),
    "Sorting": (255, 160, 80),
    "Graphs": (160, 220, 100),
    "Heap": (220, 100, 200),
    "Puzzles": (255, 200, 60),
}


# FONTS
font_title = pygame.font.SysFont("Consolas", 48, bold=True)
font_subtitle = pygame.font.SysFont("Consolas", 18)
font_button = pygame.font.SysFont("Consolas", 22, bold=True)
font_label = pygame.font.SysFont("Consolas", 14)
font_small = pygame.font.SysFont("Consolas", 13)


# HELPER: draw text centred on a rect
def draw_text_centred(surface, text, font, colour, rect):
    rendered = font.render(text, True, colour)
    x = rect.centerx - rendered.get_width() // 2
    y = rect.centery - rendered.get_height() // 2
    surface.blit(rendered, (x, y))


def draw_text(surface, text, font, colour, pos):
    rendered = font.render(text, True, colour)
    surface.blit(rendered, pos)


class Button:
    def __init__(self, label, rect, colour):
        self.label = label
        self.rect = pygame.Rect(rect)
        self.colour = colour
        self.hovered = False

    def draw(self, surface):
        # Glow effect when hovered
        if self.hovered:
            glow = pygame.Surface(
                (self.rect.width + 8, self.rect.height + 8), pygame.SRCALPHA
            )
            pygame.draw.rect(
                glow, (*self.colour, 60), glow.get_rect(), border_radius=14
            )
            surface.blit(glow, (self.rect.x - 4, self.rect.y - 4))

        # Button body
        body_colour = (
            self.colour
            if not self.hovered
            else tuple(min(c + 30, 255) for c in self.colour)
        )
        pygame.draw.rect(surface, BG_PANEL, self.rect, border_radius=10)
        pygame.draw.rect(surface, body_colour, self.rect, width=2, border_radius=10)

        # Left accent bar
        bar = pygame.Rect(self.rect.x + 2, self.rect.y + 10, 4, self.rect.height - 20)
        pygame.draw.rect(surface, body_colour, bar, border_radius=2)

        # Label
        label_colour = TEXT_PRIMARY if not self.hovered else body_colour
        draw_text_centred(surface, self.label, font_button, label_colour, self.rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


def draw_background(surface):
    surface.fill(BG_DARK)
    # Subtle dot grid
    for x in range(0, WIDTH, 30):
        for y in range(0, HEIGHT, 30):
            pygame.draw.circle(surface, BORDER, (x, y), 1)
    # Top accent line
    pygame.draw.line(surface, ACCENT, (0, 0), (WIDTH, 0), 3)


# MAIN MENU SCREEN
def build_menu_buttons():
    labels = list(MODULE_COLOURS.keys())
    buttons = []
    btn_w, btn_h = 360, 58
    start_x = WIDTH // 2 - btn_w // 2
    start_y = 240
    gap = 72
    for i, label in enumerate(labels):
        rect = (start_x, start_y + i * gap, btn_w, btn_h)
        buttons.append(Button(label, rect, MODULE_COLOURS[label]))
    return buttons


def draw_main_menu(surface, buttons, mouse_pos):
    draw_background(surface)

    # Title block
    title_surf = font_title.render("DSA Explorer", True, ACCENT)
    surface.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 60))

    sub = "& Visualiser"
    sub_surf = font_subtitle.render(sub, True, TEXT_MUTED)
    surface.blit(sub_surf, (WIDTH // 2 - sub_surf.get_width() // 2, 118))

    # Divider
    pygame.draw.line(
        surface, BORDER, (WIDTH // 2 - 180, 155), (WIDTH // 2 + 180, 155), 1
    )

    prompt = font_label.render("Select a module to begin", True, TEXT_MUTED)
    surface.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 168))

    # Buttons
    for btn in buttons:
        btn.check_hover(mouse_pos)
        btn.draw(surface)

    # Footer
    footer = font_small.render(
        "ST2 Group Project  |  Press ESC at any time to return here", True, TEXT_MUTED
    )
    surface.blit(footer, (WIDTH // 2 - footer.get_width() // 2, HEIGHT - 30))


#  MODULE ENTRY POINTS
#  Import and call your real modules here
def run_data_structures():
    """Phase 1 — Stack, Queue, Linked List, BST."""
    from Data_Structures_module import run

    run(screen, clock)


def run_sorting():
    """Phase 2 — Bubble, Selection, Merge sort."""
    from sorting_module import run

    run(screen, clock)


def run_graphs():
    """Phase 2 — BFS / DFS graph traversal."""
    from Graphs import run

    run(screen, clock)


def run_heap():
    """Phase 2 — Heap insertion / extraction."""
    from heap_module import run

    run(screen, clock)


def run_puzzles():
    """Phase 3 — Pathfinding, Event Simulator, DP puzzle."""
    from puzzles_module import run

    run(screen, clock)


# DISPATCH TABLE  (maps button label → function)

MODULE_DISPATCH = {
    "Data Structures": run_data_structures,
    "Sorting": run_sorting,
    "Graphs": run_graphs,
    "Heap": run_heap,
    "Puzzles": run_puzzles,
}


# MAIN LOOP
def main():
    buttons = build_menu_buttons()

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # ESC on main menu = quit
                pygame.quit()
                sys.exit()

            for btn in buttons:
                if btn.is_clicked(event):
                    MODULE_DISPATCH[btn.label]()  # launch module
                    # When the module returns, we fall back to the menu loop

        draw_main_menu(screen, buttons, mouse_pos)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
