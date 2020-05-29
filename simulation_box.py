from abc import ABC, abstractmethod

import numpy as np
import pygame

from common import window, colors, Object, Text, Button, ToggleButton, Slider

NODE_RADIUS = 27
BOX_BORDER = 70


class SimulationBox(Object):
    def __init__(self, center=[460, 550], size=[800, 800]):
        self.center = np.array(center)
        self.size = np.array(size)
        self.cities = np.array([[-180, -200],
                                [200, 50],
                                [-200, 50],
                                [0, 300],
                                [150, -150]])
        self.clicked_city = -1
        self.screen_update = False
        self.simulate = False
        self.simulation_speed_obj = [1]
        self.buttons = {
            "AddCity": Button(self.center + self.size / 2 * [-1, 1] + [100, 50],
                              size=(200, 100), color=colors['Blue'], clicked_color=colors['DarkBlue'],
                              text="Dodaj grad", action=self.addCity),
            "RemoveCity": Button(self.center + self.size / 2 * [-1, 1] + [300, 50],
                                 size=(200, 100), color=colors['Purple'], clicked_color=colors['DarkPurple'],
                                 text="Skloni grad", action=self.removeCity),
            "StartSimulation": ToggleButton(self.center + self.size / 2 + [-150, 50],
                                            size=(300, 100), color=colors['Green'], clicked_color=colors['DarkRed'],
                                            text="Simuliraj", action=self.toggleSimulation, action_arg=True,
                                            alt_text="Zaustavi Simulaciju", alt_action=self.toggleSimulation, alt_action_arg=False),
            "SimSpeedSlider": Slider(self.simulation_speed_obj, (1, 10), (1500, 400), "Brzina simulacije")
        }

    def draw(self, force=False):
        for button in self.buttons.values():
            button.draw(force)

        if self.simulate or self.screen_update or force:
            cities = self.cities
            center = self.center
            size = self.size
            update_rect = pygame.draw.rect(window, colors['Gray' if self.simulate else 'LightGray'],
                                           (center - size / 2, size))

            for i in range(len(cities)):
                for j in range(i + 1, len(cities)):
                    pygame.draw.line(window, colors['DarkGray'],
                                     cities[i] + center, cities[j] + center, 5)
            for i in range(len(cities)):
                pygame.draw.circle(window, colors['Black'], cities[i] + center, NODE_RADIUS)
                text_object = Text(chr(ord('A') + i), cities[i] + center +
                                   (cities[i] / (np.linalg.norm(cities[i]) + 1) * 40), 35)
                text_object.draw(force=True, update=False)
                del text_object

            if self.simulate:
                self.performSimulationStep()

            pygame.display.update(update_rect)
            self.screen_update = False

    def handleMouseDown(self, click_pos):
        for button in self.buttons.values():
            button.handleMouseDown(click_pos)

        if self.simulate:
            return

        if self.clicked_city == -1:
            if all(abs(click_pos - self.center) < self.size / 2):
                for i in range(len(self.cities)):
                    if np.linalg.norm(click_pos - self.cities[i] - self.center) < NODE_RADIUS:
                        self.clicked_city = i
                        break
        else:
            self.screen_update = True
            self.cities[self.clicked_city] = np.clip(
                click_pos - self.center, -self.size / 2 + BOX_BORDER, self.size / 2 - BOX_BORDER)

    def handleMouseUp(self, click_pos):
        for button in self.buttons.values():
            button.handleMouseUp(click_pos)

        if self.simulate:
            return

        self.clicked_city = -1

    def addCity(self):
        if not self.simulate:
            self.screen_update = True
            new_city = np.random.randint(-400 + BOX_BORDER, 401 - BOX_BORDER, size=2)
            self.cities = np.vstack((self.cities, new_city))

    def removeCity(self):
        if not self.simulate:
            self.screen_update = True
            self.cities = self.cities[:-1, :]

    def toggleSimulation(self, state, toggle_button=False):
        if state:
            self.resetSimulation()

        self.simulate = state
        if toggle_button:
            self.buttons["StartSimulation"].toggle_state = state

    @abstractmethod
    def resetSimulation(self):
        pass

    @abstractmethod
    def performSimulationStep(self):
        pass
