# Phase 2 - Sorting module

import pygame
import sys
import random
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

# Module-level globals (set by run())
screen = None
clock = None

MODULE_COLOURS = {
    "Bubble Sort": (100, 200, 255),
    "Selection Sort": (255, 160, 80),
    "Merge Sort": (160, 220, 100),
}

ARRAY_SIZE = 20
ARRAY_MIN = 5
ARRAY_MAX = 100
STEP_DELAY = 60  # ms between animation steps (lower = faster)


# Sort logic
def bubble_sort(arr: list) -> list:
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(arr: list) -> list:
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def mergesort(array: list, l: int, r: int) -> None:
    if l < r:
        m = l + (r - l) // 2
        mergesort(array, l, m)
        mergesort(array, m + 1, r)
        merge(array, l, m, r)


def merge(array: list, l: int, m: int, r: int) -> None:
    n1 = m - l + 1
    n2 = r - m
    L = [0] * n1
    R = [0] * n2
    for i in range(n1):
        L[i] = array[l + i]
    for j in range(n2):
        R[j] = array[m + 1 + j]
    i = j = 0
    k = l
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            array[k] = L[i]
            i += 1
        else:
            array[k] = R[j]
            j += 1
        k += 1
    while i < n1:
        array[k] = L[i]
        i += 1
        k += 1
    while j < n2:
        array[k] = R[j]
        j += 1
        k += 1


# Step generators
def bubble_sort_steps(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            yield (j, j + 1, "compare")
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                yield (j, j + 1, "swap")
        if not swapped:
            break


def selection_sort_steps(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield (min_idx, j, "compare")
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            yield (i, min_idx, "swap")


def merge_sort_steps(arr):
    n = len(arr)
    width = 1
    while width < n:
        for l in range(0, n, 2 * width):
            m = min(l + width - 1, n - 1)
            r = min(l + 2 * width - 1, n - 1)
            if m < r:
                left = arr[l : m + 1]
                right = arr[m + 1 : r + 1]
                i = j = 0
                k = l
                while i < len(left) and j < len(right):
                    yield (l + i, m + 1 + j, "compare")
                    if left[i] <= right[j]:
                        arr[k] = left[i]
                        i += 1
                    else:
                        arr[k] = right[j]
                        j += 1
                    yield (k, k, "swap")
                    k += 1
                while i < len(left):
                    arr[k] = left[i]
                    yield (k, k, "swap")
                    i += 1
                    k += 1
                while j < len(right):
                    arr[k] = right[j]
                    yield (k, k, "swap")
                    j += 1
                    k += 1
        width *= 2


# Array drawing
def draw_array(
    surface, arr, idx1=-1, idx2=-1, action="", colour=ACCENT, sorted_idx=None
):
    """
    Draw the array as vertical bars.
    idx1, idx2  — indices currently highlighted
    action      — 'compare' or 'swap' determines highlight colour
    sorted_idx  — all indices >= this are considered sorted (drawn in SUCCESS)
    """
    if sorted_idx is None:
        sorted_idx = len(arr)

    n = len(arr)
    max_val = max(arr) if arr else 1
    bar_area_x = 60
    bar_area_y = 90
    bar_area_w = WIDTH - 120
    bar_area_h = HEIGHT - 200
    bar_w = bar_area_w // n
    gap = 2

    if action == "compare":
        hi_colour = WARNING
    elif action == "swap":
        hi_colour = DANGER
    else:
        hi_colour = ACCENT

    for i, val in enumerate(arr):
        bar_h = int((val / max_val) * bar_area_h)
        x = bar_area_x + i * bar_w
        y = bar_area_y + bar_area_h - bar_h

        if i == idx1 or i == idx2:
            col = hi_colour
        elif i >= sorted_idx:
            col = SUCCESS
        else:
            col = colour

        pygame.draw.rect(
            surface, col, (x + gap, y, bar_w - gap * 2, bar_h), border_radius=3
        )

        # Value label — only draw if bars are wide enough
        if bar_w >= 22:
            lbl = font_label.render(str(val), True, TEXT_MUTED)
            surface.blit(
                lbl,
                (x + bar_w // 2 - lbl.get_width() // 2, bar_area_y + bar_area_h + 4),
            )


# Generic sort visualiser
def run_sort_visualiser(title, colour, generator_fn):
    """
    Shared visualiser loop used by all three sort screens.
    generator_fn: one of bubble_sort_steps, selection_sort_steps, merge_sort_steps
    """
    arr = random.sample(range(ARRAY_MIN, ARRAY_MAX), ARRAY_SIZE)
    gen = None
    idx1 = -1
    idx2 = -1
    action = ""
    message = "Press Start to begin sorting."
    done = False
    last_step = 0  # timestamp of last generator advance

    start_btn = Button("Start", (40, HEIGHT - 80, 110, 40), colour)
    reset_btn = Button("Reset", (170, HEIGHT - 80, 110, 40), WARNING)
    fast_btn = Button("Fast", (300, HEIGHT - 80, 110, 40), ACCENT)

    global STEP_DELAY
    step_delay = STEP_DELAY

    while True:
        now = pygame.time.get_ticks()
        mouse = pygame.mouse.get_pos()

        # Advance one generator step after delay
        if gen is not None and not done and now - last_step >= step_delay:
            try:
                idx1, idx2, action = next(gen)
                last_step = now
            except StopIteration:
                idx1 = idx2 = -1
                action = ""
                done = True
                message = "Sorted!"

        # Draw
        draw_background(screen)
        draw_banner(screen, title, colour)
        draw_array(screen, arr, idx1, idx2, action, colour)

        # Legend
        draw_text(screen, "■ Compare", font_label, WARNING, (WIDTH - 200, HEIGHT - 120))
        draw_text(screen, "■ Swap", font_label, DANGER, (WIDTH - 200, HEIGHT - 100))
        draw_text(screen, "■ Sorted", font_label, SUCCESS, (WIDTH - 200, HEIGHT - 80))

        for btn in (start_btn, reset_btn, fast_btn):
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

            if start_btn.is_clicked(event):
                if gen is None and not done:
                    gen = generator_fn(arr[:])  # copy so original preserved
                    # reassign arr to the same list the generator mutates
                    arr = arr[:]
                    gen = generator_fn(arr)
                    message = "Sorting..."
                elif done:
                    message = "Press Reset to sort a new array."

            if reset_btn.is_clicked(event):
                arr = random.sample(range(ARRAY_MIN, ARRAY_MAX), ARRAY_SIZE)
                gen = None
                idx1 = idx2 = -1
                action = ""
                done = False
                step_delay = STEP_DELAY
                message = "Press Start to begin sorting."

            if fast_btn.is_clicked(event):
                step_delay = max(5, step_delay - 15)
                message = f"Speed up! Delay: {step_delay}ms"

        clock.tick(FPS)


# Individual visualiser entry points
def Int_BubbleSort():
    run_sort_visualiser("Bubble Sort", MODULE_COLOURS["Bubble Sort"], bubble_sort_steps)


def Int_SelectionSort():
    run_sort_visualiser(
        "Selection Sort", MODULE_COLOURS["Selection Sort"], selection_sort_steps
    )


def Int_MergeSort():
    run_sort_visualiser("Merge Sort", MODULE_COLOURS["Merge Sort"], merge_sort_steps)


# Sub-menu
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
    "Bubble Sort": Int_BubbleSort,
    "Selection Sort": Int_SelectionSort,
    "Merge Sort": Int_MergeSort,
}


def draw_submenu(surface, buttons, mouse_pos):
    draw_background(surface)

    title_surf = font_title.render("Sorting Algorithms", True, ACCENT)
    surface.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 60))

    sub_surf = font_subtitle.render(
        "Choose a sorting algorithm to visualise", True, TEXT_MUTED
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


# Entry point
def run(ext_screen, ext_clock):
    """Called by main_menu.py when the Sorting button is clicked."""
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
