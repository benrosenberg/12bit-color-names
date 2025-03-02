import pygame
import sys

import shelve

shelf = shelve.open("colornames")
names = shelf["names"]  # { rgb color : name }
namecolors = shelf["name colors"]  # { name : real name color }
shelf.close()


def getHex(x):
    c = hex(x)[2:]
    return ("0" * (2 - len(c))) + c


def toHexCode(r, g, b):
    return "#{}{}{}".format(getHex(r), getHex(g), getHex(b))


# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
CELL_SIZE = WIDTH // 16
FONT = pygame.font.SysFont("Consolas", 20)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RGB Slice Visualizer")

# Sample dictionaries (replace with your actual mappings)
# rgb_to_name = {(0, 0, 0): "Black", (255, 255, 255): "White"}  # Example
rgb_to_name = names
# name_to_rgb = {"Black": (0, 0, 0), "White": (255, 255, 255)}  # Example
name_to_rgb = namecolors

# State
axis = 0  # 0 = R excluded, 1 = G excluded, 2 = B excluded
slice_val = 0  # 0-15 for the value of the excluded axis


# Draw the current slice
def draw_slice():
    screen.fill((0, 0, 0))
    for i in range(16):
        for j in range(16):
            if axis == 0:  # R excluded
                color = (slice_val * 17, i * 17, j * 17)
            elif axis == 1:  # G excluded
                color = (i * 17, slice_val * 17, j * 17)
            else:  # B excluded
                color = (i * 17, j * 17, slice_val * 17)

            # Find closest named color
            # closest_name = min(
            #     rgb_to_name.keys(),
            #     key=lambda k: sum((a - b) ** 2 for a, b in zip(k, color)),
            # )
            # mapped_color = name_to_rgb[rgb_to_name[closest_name]]
            mapped_color = name_to_rgb[rgb_to_name[color]]

            pygame.draw.rect(
                screen,
                mapped_color,
                (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )

    # pygame.display.flip()


# Main loop
running = True
hovered_color_name = ""
color = (0, 0, 0)
while running:
    draw_slice()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                axis = (axis - 1) % 3
            elif event.key == pygame.K_RIGHT:
                axis = (axis + 1) % 3
            elif event.key == pygame.K_UP:
                slice_val = min(slice_val + 1, 15)
            elif event.key == pygame.K_DOWN:
                slice_val = max(slice_val - 1, 0)
        if event.type == pygame.MOUSEMOTION or (
            event.type == pygame.KEYDOWN
            and event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        ):
            x, y = pygame.mouse.get_pos()
            i, j = x // CELL_SIZE, y // CELL_SIZE
            if 0 <= i < 16 and 0 <= j < 16:
                if axis == 0:
                    color = (slice_val * 17, i * 17, j * 17)
                elif axis == 1:
                    color = (i * 17, slice_val * 17, j * 17)
                else:
                    color = (i * 17, j * 17, slice_val * 17)
                # closest_name = min(
                #     rgb_to_name.keys(),
                #     key=lambda k: sum((a - b) ** 2 for a, b in zip(k, color)),
                # )
                # hovered_color_name = rgb_to_name[closest_name]
                hovered_color_name = rgb_to_name[color]

    # Display hovered color name
    info = "Color: {}\nRGB: {}\nHex: {}\nAxes: {}".format(
        hovered_color_name,
        color,
        toHexCode(*color).upper(),
        "RGB"[:axis] + "RGB"[axis + 1 :],
    )
    for i, text in enumerate(info.splitlines()):
        text_surface = FONT.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10 + (30 * i)))
    pygame.display.flip()

pygame.quit()
