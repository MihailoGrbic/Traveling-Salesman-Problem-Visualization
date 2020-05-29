import numpy as np
import pygame

from common import window, colors, Slider
from simulation_box import SimulationBox, NODE_RADIUS

ANT_RADIUS = int(NODE_RADIUS / 3)
ANT_OPT_CONSTANT = 100


class AntOptSim(SimulationBox):
    def __init__(self, center=[460, 550], size=[800, 800]):
        super(AntOptSim, self).__init__(center, size)
        self.pher_matrix = np.ones((self.cities.shape[0], self.cities.shape[0])) * 0.3
        self.current_city = 0
        self.target_city = 0
        self.ant_position = self.cities[0]
        self.path = [0]
        self.moving = False
        self.moving_angle = np.array([1, 0])

        self.beta_obj = [0]
        self.alpha_obj = [0]

        self.buttons.update({"BetaSlider": Slider(self.beta_obj, (0, 1), (1500, 550), "Beta", float),
                             "AlphaSlider": Slider(self.alpha_obj, (0, 1), (1500, 700), "Alfa", float)})

    def softReset(self):
        self.current_city = 0
        self.path = [0]
        self.ant_position = self.cities[0]
        self.moving = False

    def resetSimulation(self):
        self.softReset()
        self.pher_matrix = np.ones((self.cities.shape[0], self.cities.shape[0])) * 0.3

    def performSimulationStep(self):
        if len(self.path) == self.cities.shape[0] + 1:
            self.globalUpdate()
            self.softReset()

        for i in range(self.pher_matrix.shape[0]):
            for j in range(i):
                line_color = (255,
                              max(int(255 * (1 - self.pher_matrix[i][j])), 0),
                              0)
                line_width = min(int(self.pher_matrix[i][j] * 25), 25)
                pygame.draw.line(window, line_color, self.cities[i] + self.center,
                                 self.cities[j] + self.center, line_width)

        # Redraw cities because it looks better
        for city in self.cities:
            pygame.draw.circle(window, colors['Black'], city + self.center, NODE_RADIUS)

        if not self.moving:
            self.decideCity()
        else:
            if np.linalg.norm(self.ant_position - self.cities[self.target_city]) < 5:
                self.moving = False
                self.current_city = self.target_city
                self.path.append(self.target_city)
            pygame.draw.circle(window, colors['Green'], (self.ant_position + self.center).astype(int), ANT_RADIUS)
            self.ant_position = self.ant_position + self.moving_angle * self.simulation_speed_obj[0]

    def decideCity(self):
        probability = np.zeros(self.cities.shape[0])

        # If all cities are visited, go back to the starting city
        if len(self.path) == self.cities.shape[0]:
            probability[0] = 1

        for i in range(self.cities.shape[0]):
            if i not in self.path:
                probability[i] = (self.pher_matrix[self.current_city][i]) ** (1 - self.beta_obj[0]) * \
                    (1 / np.linalg.norm(self.cities[self.current_city] - self.cities[i])) ** (self.beta_obj[0])

        rand_roll = np.random.rand(1) * np.sum(probability) * 0.99
        for i in range(probability.shape[0]):
            if rand_roll < probability[i]:
                self.target_city = i
                self.moving_angle = self.cities[i] - self.ant_position
                self.moving_angle = self.moving_angle / np.linalg.norm(self.moving_angle)
                break
            else:
                rand_roll -= probability[i]
        self.moving = True

    def globalUpdate(self):
        for i in range(self.pher_matrix.shape[0]):
            for j in range(self.pher_matrix.shape[1]):
                self.pher_matrix[i][j] *= (1 - self.alpha_obj[0])
                self.pher_matrix[i][j] = max(self.pher_matrix[i][j], 0.05)

        path_length = 0
        for i in range(1, len(self.path)):
            path_length += np.linalg.norm(self.cities[self.path[i]] - self.cities[self.path[i - 1]])

        for i in range(1, len(self.path)):
            self.pher_matrix[self.path[i]][self.path[i - 1]] += ANT_OPT_CONSTANT * len(self.cities) / path_length
            self.pher_matrix[self.path[i - 1]][self.path[i]] += ANT_OPT_CONSTANT * len(self.cities) / path_length
