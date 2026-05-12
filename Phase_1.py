# Phase 1 - Stack, Queue, Linked List, BST Implementation

import pygame
import sys


WIDTH, HEIGHT = 900, 650
FPS = 30

# Colour Palette 
BG_DARK       = (15, 20, 40)
BG_PANEL      = (25, 32, 60)
ACCENT        = (80, 180, 255)
TEXT_PRIMARY  = (230, 235, 255)
TEXT_MUTED    = (120, 135, 170)
BORDER        = (50, 70, 120)
SUCCESS       = (80, 220, 160)
WARNING       = (255, 200, 80)
DANGER        = (255, 80, 80)

MODULE_COLOURS = {
    "Stack":        (100, 160, 255),
    "Queue":        (255, 160, 80),
    "Linked List":  (160, 220, 100),
    "BST":          (220, 100, 200),
}


#Helpers

def draw_text_centred(surface, text, font, colour, rect):
    rendered = font.render(text, True, colour)
    x = rect.centerx - rendered.get_width() // 2
    y = rect.centery - rendered.get_height() // 2
    surface.blit(rendered, (x, y))


def draw_text(surface, text, font, colour, pos):
    rendered = font.render(text, True, colour)
    surface.blit(rendered, pos)

def draw_background(surface):
    surface.fill(BG_DARK)
    for x in range(0, WIDTH, 30):
        for y in range(0, HEIGHT, 30):
            pygame.draw.circle(surface, BORDER, (x, y), 1)
    pygame.draw.line(surface, ACCENT, (0, 0), (WIDTH, 0), 3)

def draw_status(surface, message, colour=WARNING):
    msg = font_label.render(message, True, colour)
    surface.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 36))

#  BUTTON CLASS

class Button:
    def __init__(self, label, rect, colour):
        self.label  = label
        self.rect   = pygame.Rect(rect)
        self.colour = colour
        self.hovered = False

    def draw(self, surface):
        if self.hovered:
            glow = pygame.Surface((self.rect.width + 8, self.rect.height + 8), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*self.colour, 60), glow.get_rect(), border_radius=14)
            surface.blit(glow, (self.rect.x - 4, self.rect.y - 4))
        body_colour = self.colour if not self.hovered else tuple(min(c + 30, 255) for c in self.colour)
        pygame.draw.rect(surface, BG_PANEL, self.rect, border_radius=10)
        pygame.draw.rect(surface, body_colour, self.rect, width=2, border_radius=10)
        bar = pygame.Rect(self.rect.x + 2, self.rect.y + 10, 4, self.rect.height - 20)
        pygame.draw.rect(surface, body_colour, bar, border_radius=2)
        label_colour = TEXT_PRIMARY if not self.hovered else body_colour
        draw_text_centred(surface, self.label, font_button, label_colour, self.rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))


def draw_banner(surface, title, colour):
    banner = pygame.Rect(0, 0, WIDTH, 70)
    pygame.draw.rect(surface, BG_PANEL, banner)
    pygame.draw.line(surface, colour, (0, 70), (WIDTH, 70), 2)
    title_surf = font_title.render(title, True, colour)
    surface.blit(title_surf, (40, 18))
    hint = font_small.render("ESC — back to menu", True, TEXT_MUTED)
    surface.blit(hint, (WIDTH - hint.get_width() - 20, 28))


#  INPUT BOX


class InputBox:
    def __init__(self, x, y, w, h, label=""):
        self.rect   = pygame.Rect(x, y, w, h)
        self.label  = label
        self.text   = ""
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key not in (pygame.K_RETURN, pygame.K_TAB) and len(self.text) < 8:
                self.text += event.unicode
        return self.active and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN

    def draw(self, surface):
        colour = ACCENT if self.active else BORDER
        lbl = font_label.render(self.label, True, TEXT_MUTED)
        surface.blit(lbl, (self.rect.x, self.rect.y - 18))
        pygame.draw.rect(surface, BG_PANEL, self.rect, border_radius=8)
        pygame.draw.rect(surface, colour, self.rect, 2, border_radius=8)
        t = font_button.render(self.text + ("|" if self.active else ""), True, TEXT_PRIMARY)
        surface.blit(t, (self.rect.x + 8, self.rect.centery - t.get_height() // 2))

    def get(self):
        return self.text.strip()

    def clear(self):
        self.text = ""

#  DATA STRUCTURE CLASSES 

# Stack - Same Logic Used In Assignment 1
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


# Queue  - Again the same
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
    
    "Only signifcant change added from assingment 1 to ensure queue doesnt go offscreen"
    
    MAX_CAPACITY = 9

    def is_full(self):
        return len(self.queue) >= self.MAX_CAPACITY

# Linked List Logic
"Based on assignment 1"
class Node:
    def __init__(self, val):
        self.val  = val
        self.next = None
        self.previous = None

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


# BST LOGIC
"Based on assignment 1"
class BSTNode:
    def __init__(self, val):
        self.val   = val
        self.left  = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, val):
        def _ins(node, v):
            if not node:return BSTNode(v)
            if v < node.val:node.left  = _ins(node.left,  v)
            elif v > node.val:node.right = _ins(node.right, v)
            return node
        self.root = _ins(self.root, val)

    def inorder(self):
        out = []
        def _in(n):
            if n: _in(n.left); out.append(n.val); _in(n.right)
        _in(self.root); return out

    def preorder(self):
        out = []
        def _pre(n):
            if n: out.append(n.val); _pre(n.left); _pre(n.right)
        _pre(self.root); return out

    def postorder(self):
        out = []
        def _post(n):
            if n: _post(n.left); _post(n.right); out.append(n.val)
        _post(self.root); return out



#STACK DISPLAY


def Int_Stack():
    colour  = MODULE_COLOURS["Stack"]
    stack   = Stack()
    message = "Push values onto the stack."
    input     = InputBox(40, 560, 160, 36, "Value:")

    push_btn = Button("Push", (220, 555, 120, 40), colour)
    pop_btn  = Button("Pop",  (360, 555, 120, 40), DANGER)

    while True:
        mouse = pygame.mouse.get_pos()
        draw_background(screen)
        draw_banner(screen, "Stack Visualiser", colour)

        # Draw stack boxes bottom-up
        box_w, box_h = 180, 46
        base_x = WIDTH // 2 - box_w // 2
        base_y = 500
        for i, val in enumerate(stack.stack):
            y   = base_y - i * (box_h + 4)
            col = SUCCESS if i == len(stack.stack) - 1 else (WARNING if i == 0 else BG_PANEL)
            pygame.draw.rect(screen, col, (base_x, y, box_w, box_h), border_radius=8)
            pygame.draw.rect(screen, colour, (base_x, y, box_w, box_h), 2, border_radius=8)
            lbl = font_node.render(str(val), True, TEXT_PRIMARY)
            screen.blit(lbl, (base_x + box_w // 2 - lbl.get_width() // 2, y + box_h // 2 - lbl.get_height() // 2))

        if stack.stack:
            top_y = base_y - (len(stack.stack) - 1) * (box_h + 4)
            draw_text(screen, "TOP",    font_label, SUCCESS, (base_x + box_w + 10, top_y + box_h // 2 - 7))
            if len(stack.stack) > 1:
                draw_text(screen, "BOTTOM", font_label, WARNING, (base_x + box_w + 10, base_y + box_h // 2 - 7))
        else:
            draw_text(screen, "(empty)", font_subtitle, TEXT_MUTED, (WIDTH // 2 - 40, base_y + 5))

        input.draw(screen)
        push_btn.check_hover(mouse); push_btn.draw(screen)
        pop_btn.check_hover(mouse);  pop_btn.draw(screen)
        draw_status(screen, message)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return
            entered = input.handle_event(event)
            if push_btn.is_clicked(event) or entered:
                val = input.get()
                if val:
                    if stack.is_full():
                        message = "Stack is full! Pop an item first."
                    else:
                        stack.push(val); message = f"Pushed '{val}' onto stack."; input.clear()
                else:
                    message = "Enter a value first."
            if pop_btn.is_clicked(event):
                v = stack.pop()
                message = f"Popped '{v}' from stack." if v is not None else "Stack is empty!"
        clock.tick(FPS)


#QUEUE DISPLAY
def Int_Queue():
    colour  = MODULE_COLOURS["Queue"]
    queue   = Queue()
    message = "Enqueue values into the queue."
    input     = InputBox(40, 560, 160, 36, "Value:")

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
            x   = start_x + i * (box_w + 8)
            col = SUCCESS if i == 0 else (WARNING if i == len(queue.queue) - 1 else BG_PANEL)
            pygame.draw.rect(screen, col, (x, start_y, box_w, box_h), border_radius=8)
            pygame.draw.rect(screen, colour, (x, start_y, box_w, box_h), 2, border_radius=8)
            lbl = font_node.render(str(val), True, TEXT_PRIMARY)
            screen.blit(lbl, (x + box_w // 2 - lbl.get_width() // 2, start_y + box_h // 2 - lbl.get_height() // 2))
            # Arrow
            if i < len(queue.queue) - 1:
                ax = x + box_w + 1
                ay = start_y + box_h // 2
                pygame.draw.line(screen, colour, (ax, ay), (ax + 6, ay), 2)
                pygame.draw.polygon(screen, colour, [(ax+6,ay-4),(ax+6,ay+4),(ax+12,ay)])

        if queue.queue:
            draw_text(screen, "FRONT", font_label, SUCCESS, (start_x, start_y + box_h + 8))
            if len(queue.queue) > 1:
                rx = start_x + (len(queue.queue) - 1) * (box_w + 8)
                draw_text(screen, "REAR",  font_label, WARNING, (rx,      start_y + box_h + 8))
        else:
            draw_text(screen, "(empty)", font_subtitle, TEXT_MUTED, (WIDTH // 2 - 40, start_y + 10))

        input.draw(screen)
        enq_btn.check_hover(mouse); enq_btn.draw(screen)
        deq_btn.check_hover(mouse); deq_btn.draw(screen)
        draw_status(screen, message)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return
            entered = input.handle_event(event)
            if enq_btn.is_clicked(event) or entered:
                val = input.get()
                if val:
                    if queue.is_full():
                        message = "Queue is full! Dequeue an item first."
                    else:
                        queue.enqueue(val); message = f"Enqueued '{val}'."; input.clear()
                else:
                    message = "Enter a value first."
            if deq_btn.is_clicked(event):
                v = queue.dequeue()
                message = f"Dequeued '{v}'." if v is not None else "Queue is empty!"
        clock.tick(FPS)
        


#LinkedListDisplay
def Int_LinkedLists():
    colour = MODULE_COLOURS["Linked List"]
    ll = LinkedList()
    message = "Insert nodes into the linked list."
    input = InputBox(40, 560, 160, 36, "Value:")

    ins_btn = Button("Insert",  (220, 555, 120, 40), colour)
    del_btn = Button("Delete",  (360, 555, 120, 40), DANGER)
    rev_btn = Button("Reverse", (500, 555, 120, 40), ACCENT)

    while True:
        mouse = pygame.mouse.get_pos()
        draw_background(screen)
        draw_banner(screen, "Linked List Visualiser", colour)

        nodes = ll.to_list()
        node_w, node_h = 72, 42
        start_x, start_y = 50, 270
        for i, val in enumerate(nodes):
            x = start_x + i * (node_w + 44)
            pygame.draw.rect(screen, BG_PANEL, (x, start_y, node_w, node_h), border_radius=8)
            pygame.draw.rect(screen, colour,   (x, start_y, node_w, node_h), 2, border_radius=8)
            lbl = font_node.render(str(val), True, TEXT_PRIMARY)
            screen.blit(lbl, (x + node_w // 2 - lbl.get_width() // 2, start_y + node_h // 2 - lbl.get_height() // 2))
            # Arrow pointer
            if i < len(nodes) - 1:
                ax = x + node_w + 2
                ay = start_y + node_h // 2
                pygame.draw.line(screen, colour, (ax, ay), (ax + 40, ay), 2)
                pygame.draw.polygon(screen, colour, [(ax+40,ay-5),(ax+40,ay+5),(ax+48,ay)])
        else:
            draw_text(screen, "(empty list)", font_subtitle, TEXT_MUTED, (WIDTH // 2 - 60, 280))

        input.draw(screen)
        ins_btn.check_hover(mouse); ins_btn.draw(screen)
        del_btn.check_hover(mouse); del_btn.draw(screen)
        rev_btn.check_hover(mouse); rev_btn.draw(screen)
        draw_status(screen, message)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return
            entered = input.handle_event(event)
            if ins_btn.is_clicked(event) or entered:
                val = input.get()
                if val:
                    ll.insert(val); message = f"Inserted '{val}'."; input.clear()
                else:
                    message = "Enter a value first."
            if del_btn.is_clicked(event):
                val = input.get()
                if val:
                    ll.delete(val); message = f"Deleted '{val}'."; input.clear()
                else:
                    message = "Enter a value to delete."
            if rev_btn.is_clicked(event):
                ll.reverse(); message = "List reversed!"
        clock.tick(FPS)



# BST DISPLAY
def draw_node(surface, node, x, y, gap, colour):
    if not node: return
    r = 24
    pygame.draw.circle(surface, BG_PANEL, (x, y), r)
    pygame.draw.circle(surface, colour,   (x, y), r, 2)
    lbl = font_node.render(str(node.val), True, TEXT_PRIMARY)
    surface.blit(lbl, (x - lbl.get_width() // 2, y - lbl.get_height() // 2))
    next_y = y + 72
    if node.left:
        lx = x - gap
        pygame.draw.line(surface, colour, (x - r, y), (lx + r, next_y), 2)
        draw_node(surface, node.left,  lx, next_y, max(gap // 2, 22), colour)
    if node.right:
        rx = x + gap
        pygame.draw.line(surface, colour, (x + r, y), (rx - r, next_y), 2)
        draw_node(surface, node.right, rx, next_y, max(gap // 2, 22), colour)


def Int_BST():
    colour    = MODULE_COLOURS["BST"]
    bst       = BST()
    message   = "Insert integer values to build the BST."
    traversal = ""
    input = InputBox(40, 560, 160, 36, "Integer value:")

    ins_btn  = Button("Insert",    (220, 555, 110, 40), colour)
    in_btn   = Button("Inorder",   (345, 555, 110, 40), ACCENT)
    pre_btn  = Button("Preorder",  (470, 555, 110, 40), ACCENT)
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
            btn.check_hover(mouse); btn.draw(screen)
        draw_status(screen, message)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return
            entered = input.handle_event(event)
            if ins_btn.is_clicked(event) or entered:
                val = input.get()
                if val.lstrip("-").isdigit():
                    bst.insert(int(val)); message = f"Inserted {val}."; input.clear(); traversal = ""
                else:
                    message = "Please enter an integer."
            if in_btn.is_clicked(event):
                traversal = "Inorder:   " + str(bst.inorder())
            if pre_btn.is_clicked(event):
                traversal = "Preorder:  " + str(bst.preorder())
            if post_btn.is_clicked(event):
                traversal = "Postorder: " + str(bst.postorder())
        clock.tick(FPS)

#  SUB-MENu
def build_menu_buttons():
    labels  = list(MODULE_COLOURS.keys())
    buttons = []
    btn_w, btn_h = 360, 58
    start_x = WIDTH // 2 - btn_w // 2
    start_y = 220
    gap     = 72
    for i, label in enumerate(labels):
        rect = (start_x, start_y + i * gap, btn_w, btn_h)
        buttons.append(Button(label, rect, MODULE_COLOURS[label]))
    return buttons


def data_structures_module(screen_ref=None):
    global font_title, font_subtitle, font_button, font_label, font_small, font_node, screen, clock
    screen = screen_ref 
    clock  = pygame.time.Clock()
    font_title    = pygame.font.SysFont("Consolas", 36, bold=True)
    font_subtitle = pygame.font.SysFont("Consolas", 18)
    font_button   = pygame.font.SysFont("Consolas", 20, bold=True)
    font_label    = pygame.font.SysFont("Consolas", 14)
    font_small    = pygame.font.SysFont("Consolas", 13)
    font_node     = pygame.font.SysFont("Consolas", 16, bold=True)
    buttons = build_menu_buttons()
    DISPATCH = {
        "Stack":       Int_Stack,
        "Queue":       Int_Queue,
        "Linked List": Int_LinkedLists,
        "BST":         Int_BST,
    }

    while True:
        mouse = pygame.mouse.get_pos()
        draw_background(screen)

        # Title
        t = font_title.render("Data Structures", True, ACCENT)
        screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 80))
        s = font_subtitle.render("Choose a data structure to explore", True, TEXT_MUTED)
        screen.blit(s, (WIDTH // 2 - s.get_width() // 2, 138))
        pygame.draw.line(screen, BORDER, (WIDTH // 2 - 180, 170), (WIDTH // 2 + 180, 170), 1)

        for btn in buttons:
            btn.check_hover(mouse); btn.draw(screen)

        hint = font_small.render("ESC — return to main menu", True, TEXT_MUTED)
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return
            for btn in buttons:
                if btn.is_clicked(event):
                    DISPATCH[btn.label]()
        clock.tick(FPS)

#Cant get main to intiliase fonts without this part spent an hour and half. Font where up the top but error kept coming up so moved them directly into the function being called in main to initliase instantly it did not work lol

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DSA Explorer — Data Structures")
    data_structures_module(screen)
    pygame.quit()