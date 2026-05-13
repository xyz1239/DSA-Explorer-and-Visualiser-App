# Phase 1 - Stack, Queue, Linked List, BST Implementation

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

# font_node is unique to this module — node value labels in DS visualisers
font_node = None

MODULE_COLOURS = {
    "Stack": (100, 160, 255),
    "Queue": (255, 160, 80),
    "Linked List": (160, 220, 100),
    "BST": (220, 100, 200),
}


# DATA STRUCTURE CLASSES
# Stack logic
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, val):
        self.stack.append(val)

    def pop(self):
        if len(self.stack) == 0:
            return None
        return self.stack.pop()

    def peek(self):
        if len(self.stack) == 0:
            return None
        return self.stack[-1]

    def is_empty(self):
        return len(self.stack) == 0

    MAX_CAPACITY = 9

    def is_full(self):
        return len(self.stack) >= self.MAX_CAPACITY


# Queue logic
class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, val):
        self.queue.append(val)

    def dequeue(self):
        if len(self.queue) == 0:
            return None
        return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0

    MAX_CAPACITY = 9

    def is_full(self):
        return len(self.queue) >= self.MAX_CAPACITY


# Linked List logic
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, val):
        n = Node(val)
        if not self.head:
            self.head = n
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = n

    def delete(self, val):
        if not self.head:
            return
        if self.head.val == val:
            self.head = self.head.next
            return
        current = self.head
        while current.next:
            if current.next.val == val:
                current.next = current.next.next
                return
            current = current.next

    def reverse(self):
        previous, current = None, self.head
        while current:
            nxt = current.next
            current.next = previous
            previous = current
            current = nxt
        self.head = previous

    def to_list(self):
        out, current = [], self.head
        while current:
            out.append(current.val)
            current = current.next
        return out


# Binary Search Tree logic
class BSTNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, val):
        def _ins(node, v):
            if not node:
                return BSTNode(v)
            if v < node.val:
                node.left = _ins(node.left, v)
            elif v > node.val:
                node.right = _ins(node.right, v)
            return node

        self.root = _ins(self.root, val)

    def inorder(self):
        out = []

        def _in(n):
            if n:
                _in(n.left)
                out.append(n.val)
                _in(n.right)

        _in(self.root)
        return out

    def preorder(self):
        out = []

        def _pre(n):
            if n:
                out.append(n.val)
                _pre(n.left)
                _pre(n.right)

        _pre(self.root)
        return out

    def postorder(self):
        out = []

        def _post(n):
            if n:
                _post(n.left)
                _post(n.right)
                out.append(n.val)

        _post(self.root)
        return out


# STACK DISPLAY
def Int_Stack():
    colour = MODULE_COLOURS["Stack"]
    stack = Stack()
    message = "Push values onto the stack."
    input = InputBox(40, 560, 160, 36, "Value:")

    push_btn = Button("Push", (220, 555, 120, 40), colour)
    pop_btn = Button("Pop", (360, 555, 120, 40), DANGER)

    while True:
        mouse = pygame.mouse.get_pos()
        draw_background(screen)
        draw_banner(screen, "Stack Visualiser", colour)

        # Draw stack boxes bottom-up
        box_w, box_h = 180, 46
        base_x = WIDTH // 2 - box_w // 2
        base_y = 500
        for i, val in enumerate(stack.stack):
            y = base_y - i * (box_h + 4)
            col = (
                SUCCESS
                if i == len(stack.stack) - 1
                else (WARNING if i == 0 else BG_PANEL)
            )
            pygame.draw.rect(screen, col, (base_x, y, box_w, box_h), border_radius=8)
            pygame.draw.rect(
                screen, colour, (base_x, y, box_w, box_h), 2, border_radius=8
            )
            lbl = font_node.render(str(val), True, TEXT_PRIMARY)
            screen.blit(
                lbl,
                (
                    base_x + box_w // 2 - lbl.get_width() // 2,
                    y + box_h // 2 - lbl.get_height() // 2,
                ),
            )

        if stack.stack:
            top_y = base_y - (len(stack.stack) - 1) * (box_h + 4)
            draw_text(
                screen,
                "TOP",
                font_label,
                SUCCESS,
                (base_x + box_w + 10, top_y + box_h // 2 - 7),
            )
            if len(stack.stack) > 1:
                draw_text(
                    screen,
                    "BOTTOM",
                    font_label,
                    WARNING,
                    (base_x + box_w + 10, base_y + box_h // 2 - 7),
                )
        else:
            draw_text(
                screen,
                "(empty)",
                font_subtitle,
                TEXT_MUTED,
                (WIDTH // 2 - 40, base_y + 5),
            )

        input.draw(screen)
        push_btn.check_hover(mouse)
        push_btn.draw(screen)
        pop_btn.check_hover(mouse)
        pop_btn.draw(screen)
        draw_status(screen, message)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            entered = input.handle_event(event)
            if push_btn.is_clicked(event) or entered:
                val = input.get()
                if val:
                    if stack.is_full():
                        message = "Stack is full! Pop an item first."
                    else:
                        stack.push(val)
                        message = f"Pushed '{val}' onto stack."
                        input.clear()
                else:
                    message = "Enter a value first."
            if pop_btn.is_clicked(event):
                v = stack.pop()
                message = (
                    f"Popped '{v}' from stack." if v is not None else "Stack is empty!"
                )
        clock.tick(FPS)


# QUEUE DISPLAY
def Int_Queue():
    colour = MODULE_COLOURS["Queue"]
    queue = Queue()
    message = "Enqueue values into the queue."
    input = InputBox(40, 560, 160, 36, "Value:")

    enq_btn = Button("Enqueue", (220, 555, 140, 40), colour)
    deq_btn = Button("Dequeue", (380, 555, 140, 40), DANGER)

    while True:
        mouse = pygame.mouse.get_pos()
        draw_background(screen)
        draw_banner(screen, "Queue Visualiser", colour)

        # Draw queue boxes left to right
        box_w, box_h = 80, 50
        start_x, start_y = 60, 280
        for i, val in enumerate(queue.queue):
            x = start_x + i * (box_w + 8)
            col = (
                SUCCESS
                if i == 0
                else (WARNING if i == len(queue.queue) - 1 else BG_PANEL)
            )
            pygame.draw.rect(screen, col, (x, start_y, box_w, box_h), border_radius=8)
            pygame.draw.rect(
                screen, colour, (x, start_y, box_w, box_h), 2, border_radius=8
            )
            lbl = font_node.render(str(val), True, TEXT_PRIMARY)
            screen.blit(
                lbl,
                (
                    x + box_w // 2 - lbl.get_width() // 2,
                    start_y + box_h // 2 - lbl.get_height() // 2,
                ),
            )
            # Arrow
            if i < len(queue.queue) - 1:
                ax = x + box_w + 1
                ay = start_y + box_h // 2
                pygame.draw.line(screen, colour, (ax, ay), (ax + 6, ay), 2)
                pygame.draw.polygon(
                    screen, colour, [(ax + 6, ay - 4), (ax + 6, ay + 4), (ax + 12, ay)]
                )

        if queue.queue:
            draw_text(
                screen, "FRONT", font_label, SUCCESS, (start_x, start_y + box_h + 8)
            )
            if len(queue.queue) > 1:
                rx = start_x + (len(queue.queue) - 1) * (box_w + 8)
                draw_text(
                    screen, "REAR", font_label, WARNING, (rx, start_y + box_h + 8)
                )
        else:
            draw_text(
                screen,
                "(empty)",
                font_subtitle,
                TEXT_MUTED,
                (WIDTH // 2 - 40, start_y + 10),
            )

        input.draw(screen)
        enq_btn.check_hover(mouse)
        enq_btn.draw(screen)
        deq_btn.check_hover(mouse)
        deq_btn.draw(screen)
        draw_status(screen, message)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            entered = input.handle_event(event)
            if enq_btn.is_clicked(event) or entered:
                val = input.get()
                if val:
                    if queue.is_full():
                        message = "Queue is full! Dequeue an item first."
                    else:
                        queue.enqueue(val)
                        message = f"Enqueued '{val}'."
                        input.clear()
                else:
                    message = "Enter a value first."
            if deq_btn.is_clicked(event):
                v = queue.dequeue()
                message = f"Dequeued '{v}'." if v is not None else "Queue is empty!"
        clock.tick(FPS)


# LinkedListDisplay
def Int_LinkedLists():
    colour = MODULE_COLOURS["Linked List"]
    ll = LinkedList()
    message = "Insert nodes into the linked list."
    input = InputBox(40, 560, 160, 36, "Value:")

    ins_btn = Button("Insert", (220, 555, 120, 40), colour)
    del_btn = Button("Delete", (360, 555, 120, 40), DANGER)
    rev_btn = Button("Reverse", (500, 555, 120, 40), ACCENT)

    while True:
        mouse = pygame.mouse.get_pos()
        draw_background(screen)
        draw_banner(screen, "Linked List Visualiser", colour)

        nodes = ll.to_list()
        node_w, node_h = 72, 42
        start_x, start_y = 50, 270
        if not nodes:
            draw_text(
                screen,
                "(empty list)",
                font_subtitle,
                TEXT_MUTED,
                (WIDTH // 2 - 60, 280),
            )
        else:
            for i, val in enumerate(nodes):
                x = start_x + i * (node_w + 44)
                pygame.draw.rect(
                    screen, BG_PANEL, (x, start_y, node_w, node_h), border_radius=8
                )
                pygame.draw.rect(
                    screen, colour, (x, start_y, node_w, node_h), 2, border_radius=8
                )
                lbl = font_node.render(str(val), True, TEXT_PRIMARY)
                screen.blit(
                    lbl,
                    (
                        x + node_w // 2 - lbl.get_width() // 2,
                        start_y + node_h // 2 - lbl.get_height() // 2,
                    ),
                )
                # Arrow pointer
                if i < len(nodes) - 1:
                    ax = x + node_w + 2
                    ay = start_y + node_h // 2
                    pygame.draw.line(screen, colour, (ax, ay), (ax + 40, ay), 2)
                    pygame.draw.polygon(
                        screen,
                        colour,
                        [(ax + 40, ay - 5), (ax + 40, ay + 5), (ax + 48, ay)],
                    )

        input.draw(screen)
        ins_btn.check_hover(mouse)
        ins_btn.draw(screen)
        del_btn.check_hover(mouse)
        del_btn.draw(screen)
        rev_btn.check_hover(mouse)
        rev_btn.draw(screen)
        draw_status(screen, message)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            entered = input.handle_event(event)
            if ins_btn.is_clicked(event) or entered:
                val = input.get()
                if val:
                    ll.insert(val)
                    message = f"Inserted '{val}'."
                    input.clear()
                else:
                    message = "Enter a value first."
            if del_btn.is_clicked(event):
                val = input.get()
                if val:
                    ll.delete(val)
                    message = f"Deleted '{val}'."
                    input.clear()
                else:
                    message = "Enter a value to delete."
            if rev_btn.is_clicked(event):
                ll.reverse()
                message = "List reversed!"
        clock.tick(FPS)


# BST DISPLAY
def draw_node(surface, node, x, y, gap, colour):
    if not node:
        return
    r = 24
    pygame.draw.circle(surface, BG_PANEL, (x, y), r)
    pygame.draw.circle(surface, colour, (x, y), r, 2)
    lbl = font_node.render(str(node.val), True, TEXT_PRIMARY)
    surface.blit(lbl, (x - lbl.get_width() // 2, y - lbl.get_height() // 2))
    next_y = y + 72
    if node.left:
        lx = x - gap
        pygame.draw.line(surface, colour, (x - r, y), (lx + r, next_y), 2)
        draw_node(surface, node.left, lx, next_y, max(gap // 2, 22), colour)
    if node.right:
        rx = x + gap
        pygame.draw.line(surface, colour, (x + r, y), (rx - r, next_y), 2)
        draw_node(surface, node.right, rx, next_y, max(gap // 2, 22), colour)


def Int_BST():
    colour = MODULE_COLOURS["BST"]
    bst = BST()
    message = "Insert integer values to build the BST."
    traversal = ""
    input = InputBox(40, 560, 160, 36, "Integer value:")

    ins_btn = Button("Insert", (220, 555, 110, 40), colour)
    in_btn = Button("Inorder", (345, 555, 110, 40), ACCENT)
    pre_btn = Button("Preorder", (470, 555, 110, 40), ACCENT)
    post_btn = Button("Postorder", (595, 555, 120, 40), ACCENT)

    while True:
        mouse = pygame.mouse.get_pos()
        draw_background(screen)
        draw_banner(screen, "BST Visualiser", colour)

        draw_node(screen, bst.root, WIDTH // 2, 130, 160, colour)

        if traversal:
            t = font_label.render(traversal, True, SUCCESS)
            screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 430))

        input.draw(screen)
        for btn in (ins_btn, in_btn, pre_btn, post_btn):
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
            entered = input.handle_event(event)
            if ins_btn.is_clicked(event) or entered:
                val = input.get()
                if val.lstrip("-").isdigit():
                    bst.insert(int(val))
                    message = f"Inserted {val}."
                    input.clear()
                    traversal = ""
                else:
                    message = "Please enter an integer."
            if in_btn.is_clicked(event):
                traversal = "Inorder:   " + str(bst.inorder())
            if pre_btn.is_clicked(event):
                traversal = "Preorder:  " + str(bst.preorder())
            if post_btn.is_clicked(event):
                traversal = "Postorder: " + str(bst.postorder())
        clock.tick(FPS)


#  SUB-Menu
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
    "Stack": Int_Stack,
    "Queue": Int_Queue,
    "Linked List": Int_LinkedLists,
    "BST": Int_BST,
}


# ── Sub-menu screen ───────────────────────────────────────────────────────────
def draw_submenu(surface, buttons, mouse_pos):
    """Draws the Data Structures sub-menu."""
    draw_background(surface)

    title_surf = font_title.render("Data Structures", True, ACCENT)
    surface.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 60))

    sub_surf = font_subtitle.render(
        "Choose a data structure to explore", True, TEXT_MUTED
    )
    surface.blit(sub_surf, (WIDTH // 2 - sub_surf.get_width() // 2, 118))

    pygame.draw.line(
        surface, BORDER, (WIDTH // 2 - 180, 155), (WIDTH // 2 + 180, 155), 1
    )

    for btn in buttons:
        btn.check_hover(mouse_pos)
        btn.draw(surface)

    footer = font_small.render("ESC — return to main menu", True, TEXT_MUTED)
    surface.blit(footer, (WIDTH // 2 - footer.get_width() // 2, HEIGHT - 30))


# ── Entry point called by main_menu.py ───────────────────────────────────────
def run(ext_screen, ext_clock):
    """
    Called by main_menu.py when the Data Structures button is clicked.
    Receives the shared screen and clock so the whole app uses one window.
    """
    global screen, clock
    global font_title, font_subtitle, font_button, font_label, font_small, font_node

    screen = ext_screen
    clock = ext_clock

    # font_node is the only font unique to this module
    font_node = pygame.font.SysFont("Consolas", 20, bold=True)

    buttons = build_menu_buttons()

    # Sub-menu loop
    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # back to main menu

            for btn in buttons:
                if btn.is_clicked(event):
                    DISPATCH[btn.label]()  # launch the chosen visualiser

        draw_submenu(screen, buttons, mouse_pos)
        pygame.display.flip()
        clock.tick(FPS)
