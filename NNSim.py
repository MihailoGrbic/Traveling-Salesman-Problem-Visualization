import numpy as np
import pygame

from common import window, colors
from simulation_box import SimulationBox, NODE_RADIUS


class NNSim(SimulationBox):
    def __init__(self, center=[460, 550], size=[800, 800]):
        super(NNSim, self).__init__(center, size)
        self.current_city = 0
        self.path = [0]
        self.search_radius = NODE_RADIUS

    def resetSimulation(self):
        self.current_city = 0
        self.path = [0]
        self.search_radius = NODE_RADIUS

    def performSimulationStep(self):
        if len(self.path) == self.cities.shape[0]:
            self.path.append(0)
            self.toggleSimulation(False, True)

        for i in range(len(self.path)):
            pygame.draw.circle(window, colors['Red'], self.cities[self.path[i]] + self.center, NODE_RADIUS)
            if i > 0:
                pygame.draw.line(window, colors['Red'], self.cities[self.path[i]] + self.center,
                                 self.cities[self.path[i - 1]] + self.center, 8)

        pygame.draw.circle(window, colors['Red'], self.cities[self.path[i]] + self.center, self.search_radius, 2)
        self.search_radius += self.simulation_speed_obj[0]

        for i in range(self.cities.shape[0]):
            if i not in self.path and np.linalg.norm(
                    self.cities[i] - self.cities[self.current_city]) < self.search_radius:
                self.path.append(i)
                self.current_city = i
                self.search_radius = NODE_RADIUS
