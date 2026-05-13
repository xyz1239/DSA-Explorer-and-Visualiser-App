# Phase 2 - Heap Implementation

import pygame
import sys
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

# Module-level globals (set by run())
screen = None
clock = None

# font_node unique to this module
font_node = None

MODULE_COLOUR = (220, 100, 200)

identity = lambda x: x


# Heap Logic
class MaxHeap(object):
    def __init__(self, key=identity) -> None:
        self._arr = [None]
        self._nItems = 0
        self._key = key

    def isEmpty(self):
        return self._nItems == 0

    def isFull(self):
        return self._nItems == len(self._arr)

    def __len__(self):
        return self._nItems

    def _swap(self, i, j):
        self._arr[i], self._arr[j] = self._arr[j], self._arr[i]

    def parent(self, i):
        return (i - 1) // 2

    def leftchild(self, i):
        return i * 2 + 1

    def rightchild(self, i):
        return i * 2 + 2

    def insert_heap(self, item) -> None:
        if self.isFull():
            self._growHeap()
        self._arr[self._nItems] = item
        self._nItems += 1
        self._siftUp_rec(self._nItems - 1)

    def _growHeap(self):
        current = self._arr
        self._arr = [None] * max(1, 2 * len(self._arr))
        for i in range(self._nItems):
            self._arr[i] = current[i]

    def _siftUp_rec(self, i):
        if i <= 0:
            return
        parent = self.parent(i)
        if self._key(self._arr[parent]) < self._key(self._arr[i]):
            self._swap(parent, i)
            self._siftUp_rec(parent)

    def remove_heap(self):
        if self.isEmpty():
            raise Exception("Heap underflow")
        root = self._arr[0]
        self._nItems -= 1
        self._arr[0] = self._arr[self._nItems]
        self._arr[self._nItems] = None
        self._siftDown_rec(0)
        return root

    def _siftDown_rec(self, i):
        left, right = self.leftchild(i), self.rightchild(i)
        if left < len(self):
            if right < len(self):
                maxi = (
                    right
                    if self._key(self._arr[left]) < self._key(self._arr[right])
                    else left
                )
            else:
                maxi = left
            if self._key(self._arr[i]) < self._key(self._arr[maxi]):
                self._swap(i, maxi)
                self._siftDown_rec(maxi)

    def items(self):
        """Return the active portion of the heap array."""
        return self._arr[: self._nItems]


# Visualisation
def draw_heap_tree(surface, heap, highlighted=None):
    """
    Draw the heap as a binary tree.
    highlighted: set of indices to colour differently (e.g. nodes being swapped).
    """
    if highlighted is None:
        highlighted = set()

    all_items = heap.items()
    if not all_items:
        msg = font_subtitle.render("(empty heap)", True, TEXT_MUTED)
        surface.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 280))
        return

    # Cap display to keep tree readable on screen (max 4 levels = 15 nodes)
    MAX_DISPLAY = 15
    items = all_items[:MAX_DISPLAY]
    n = len(items)

    # Show a warning if the heap is larger than what's displayed
    if len(all_items) > MAX_DISPLAY:
        warn = font_label.render(
            f"Showing first {MAX_DISPLAY} of {len(all_items)} nodes", True, WARNING
        )
        surface.blit(warn, (WIDTH // 2 - warn.get_width() // 2, 75))

    # Precompute (x, y) for every node so edges can reference parent positions
    padding = 70  # min distance from screen edge
    start_y = 100  # y of root node
    level_h = 90  # vertical gap between levels
    r = 26  # node radius

    positions = {}
    for i in range(n):
        level = max(0, i.bit_length() - 1)
        pos_in_level = i - (2**level - 1)
        nodes_in_level = 2**level
        usable_width = WIDTH - 2 * padding
        segment = usable_width // (nodes_in_level + 1)
        x = padding + segment * (pos_in_level + 1)
        y = start_y + level * level_h
        positions[i] = (x, y)

    # Draw edges first so nodes render on top
    for i in range(1, n):
        pi = heap.parent(i)
        if pi in positions:
            pygame.draw.line(surface, BORDER, positions[pi], positions[i], 2)

    # Draw nodes
    for i in range(n):
        x, y = positions[i]
        colour = WARNING if i in highlighted else MODULE_COLOUR
        pygame.draw.circle(surface, BG_PANEL, (x, y), r)
        pygame.draw.circle(surface, colour, (x, y), r, 2)
        lbl = font_node.render(str(items[i]), True, TEXT_PRIMARY)
        surface.blit(lbl, (x - lbl.get_width() // 2, y - lbl.get_height() // 2))

    # Raw array display at the bottom
    array_str = "Array: " + str(all_items)
    arr_surf = font_label.render(array_str, True, TEXT_MUTED)
    surface.blit(arr_surf, (WIDTH // 2 - arr_surf.get_width() // 2, HEIGHT - 60))


# Interactive visualiser
def Int_Heap():
    colour = MODULE_COLOUR
    heap = MaxHeap()
    message = "Insert integer values to build the heap."

    input_box = InputBox(40, 560, 160, 36, "Integer value:")
    ins_btn = Button("Insert", (220, 555, 120, 40), colour)
    ext_btn = Button("Extract", (360, 555, 120, 40), DANGER)
    reset_btn = Button("Reset", (500, 555, 100, 40), WARNING)

    while True:
        mouse = pygame.mouse.get_pos()
        draw_background(screen)
        draw_banner(screen, "Heap Visualiser", colour)
        draw_heap_tree(screen, heap)

        input_box.draw(screen)
        for btn in (ins_btn, ext_btn, reset_btn):
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

            entered = input_box.handle_event(event)

            if ins_btn.is_clicked(event) or entered:
                val = input_box.get()
                if val.lstrip("-").isdigit():
                    heap.insert_heap(int(val))
                    message = f"Inserted {val} into heap."
                    input_box.clear()
                else:
                    message = "Please enter an integer."

            if ext_btn.is_clicked(event):
                try:
                    val = heap.remove_heap()
                    message = f"Extracted max value: {val}."
                except Exception as e:
                    message = str(e)

            if reset_btn.is_clicked(event):
                heap = MaxHeap()
                message = "Heap reset."

        clock.tick(FPS)


# Entry point
def run(ext_screen, ext_clock):
    """Called by main_menu.py when the Heap button is clicked."""
    global screen, clock, font_node

    screen = ext_screen
    clock = ext_clock
    font_node = pygame.font.SysFont("Consolas", 18, bold=True)

    Int_Heap()
