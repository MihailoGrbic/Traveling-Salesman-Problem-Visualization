import numpy as np
import pygame

from common import window, colors, Object, Button, Text, quitProgram
from screens import screens, updateScreen, changeState, state_object, quitProgram

if __name__ == "__main__":
    pygame.display.set_caption(
        "Introduction to the Traveling Salesman Problem and it's most popular solutions")

    updateScreen(state_object[0])
    pos = [0, 0]
    mouse_down = False
    tab_out = False
    window_dim = np.array(window.get_size())
    while True:
        state = state_object[0]
        events = pygame.event.get()

        # Drawing
        for obj in list(screens[state]['ObjectDict'].values()):
            obj.draw()

        if tab_out:
            changeState(state_object[0])
            tab_out = False

        # Event handling
        for event in events:
            if event.type == pygame.QUIT:
                quitProgram()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB or event.key == pygame.K_LALT:
                    tab_out = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
                mouse_pos = np.array(pygame.mouse.get_pos())
                for obj in screens[state]['ObjectDict'].values():
                    obj.handleMouseDown(mouse_pos)

            if event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    mouse_pos = np.array(pygame.mouse.get_pos())
                    for obj in screens[state]['ObjectDict'].values():
                        obj.handleMouseDown(mouse_pos)

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                mouse_pos = np.array(pygame.mouse.get_pos())
                for obj in screens[state]['ObjectDict'].values():
                    obj.handleMouseUp(mouse_pos)

        # pos[0] += 1
        # pos[1] += 1
        # circle_rect = pygame.draw.circle(window, colors['Red'], pos, 10)
        # pygame.display.update(circle_rect)
