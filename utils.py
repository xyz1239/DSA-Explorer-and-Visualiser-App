"""
utils.py — Shared UI utilities for DSA Explorer & Visualiser
Imported by all modules to avoid code duplication.
"""

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

# Shared colours not in main_menu
WARNING = (255, 200, 80)
DANGER = (255, 80, 80)

# Shared dimensions
WIDTH, HEIGHT = 900, 650
FPS = 60


# Drawing helpers
def draw_text(surface, text, font, colour, pos):
    """Blit text at a given (x, y) position."""
    rendered = font.render(text, True, colour)
    surface.blit(rendered, pos)


def draw_text_centred(surface, text, font, colour, rect):
    """Blit text centred inside a pygame.Rect."""
    rendered = font.render(text, True, colour)
    x = rect.centerx - rendered.get_width() // 2
    y = rect.centery - rendered.get_height() // 2
    surface.blit(rendered, (x, y))


def draw_background(surface):
    """Fill the screen with the dark dot-grid background."""
    surface.fill(BG_DARK)
    for x in range(0, WIDTH, 30):
        for y in range(0, HEIGHT, 30):
            pygame.draw.circle(surface, BORDER, (x, y), 1)
    pygame.draw.line(surface, ACCENT, (0, 0), (WIDTH, 0), 3)


def draw_banner(surface, title, colour):
    """Draw the top banner bar with a module title and ESC hint."""
    banner = pygame.Rect(0, 0, WIDTH, 70)
    pygame.draw.rect(surface, BG_PANEL, banner)
    pygame.draw.line(surface, colour, (0, 70), (WIDTH, 70), 2)
    title_surf = font_title.render(title, True, colour)
    surface.blit(title_surf, (40, 18))
    hint = font_small.render("ESC — back to menu", True, TEXT_MUTED)
    surface.blit(hint, (WIDTH - hint.get_width() - 20, 28))


def draw_status(surface, message, colour=None):
    """Draw a status message centred at the bottom of the screen."""
    if colour is None:
        colour = WARNING
    msg = font_label.render(message, True, colour)
    surface.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT - 36))


# Button
class Button:
    """Styled button with hover glow and accent bar."""

    def __init__(self, label, rect, colour):
        self.label = label
        self.rect = pygame.Rect(rect)
        self.colour = colour
        self.hovered = False

    def draw(self, surface):
        if self.hovered:
            glow = pygame.Surface(
                (self.rect.width + 8, self.rect.height + 8), pygame.SRCALPHA
            )
            pygame.draw.rect(
                glow, (*self.colour, 60), glow.get_rect(), border_radius=14
            )
            surface.blit(glow, (self.rect.x - 4, self.rect.y - 4))

        body_colour = (
            self.colour
            if not self.hovered
            else tuple(min(c + 30, 255) for c in self.colour)
        )
        pygame.draw.rect(surface, BG_PANEL, self.rect, border_radius=10)
        pygame.draw.rect(surface, body_colour, self.rect, width=2, border_radius=10)

        bar = pygame.Rect(self.rect.x + 2, self.rect.y + 10, 4, self.rect.height - 20)
        pygame.draw.rect(surface, body_colour, bar, border_radius=2)

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


# InputBox
class InputBox:
    """Text input field with label, cursor, and enter-to-submit."""

    def __init__(self, x, y, w, h, label=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.text = ""
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif (
                event.key not in (pygame.K_RETURN, pygame.K_TAB) and len(self.text) < 8
            ):
                self.text += event.unicode
        return (
            self.active
            and event.type == pygame.KEYDOWN
            and event.key == pygame.K_RETURN
        )

    def draw(self, surface):
        colour = ACCENT if self.active else BORDER
        lbl = font_label.render(self.label, True, TEXT_MUTED)
        surface.blit(lbl, (self.rect.x, self.rect.y - 18))
        pygame.draw.rect(surface, BG_PANEL, self.rect, border_radius=8)
        pygame.draw.rect(surface, colour, self.rect, 2, border_radius=8)
        t = font_button.render(
            self.text + ("|" if self.active else ""), True, TEXT_PRIMARY
        )
        surface.blit(t, (self.rect.x + 8, self.rect.centery - t.get_height() // 2))

    def get(self):
        return self.text.strip()

    def clear(self):
        self.text = ""
