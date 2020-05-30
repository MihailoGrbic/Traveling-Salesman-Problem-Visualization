import numpy as np
import pygame

from common import window, colors, Slider
from simulation_box import SimulationBox, NODE_RADIUS
from AntOptSim import AntOptSim

ANT_RADIUS = int(NODE_RADIUS / 3)
ANT_OPT_CONSTANT = 100
INITIAL_ANTS = 5
INITAL_PHER_VALUE = 0.3


class AntColOptSim(SimulationBox):
    def __init__(self, center=[460, 550], size=[800, 800]):
        super(AntColOptSim, self).__init__(center, size)

        self.ant_count_obj = [INITIAL_ANTS]
        self.beta_obj = [0]
        self.alpha_obj = [0]
        self.exp_obj = [0]
        self.r_obj = [0]
        self.resetSimulation()

        self.buttons["SimSpeedSlider"].moveCenter([1500, 300])
        self.buttons.update({
            "AntCountSlider": Slider(self.ant_count_obj, (INITIAL_ANTS, 20), (1500, 400), "Broj mrava", int),
            "BetaSlider": Slider(self.beta_obj, (0, 1), (1500, 500), "Beta", float),
            "AlphaSlider": Slider(self.alpha_obj, (0, 1), (1500, 600), "Alfa", float),
            "ExploreSlider": Slider(self.exp_obj, (0, 100), (1500, 700), "Istraži%", int),
            "RSlider": Slider(self.r_obj, (0, 1), (1500, 800), "R", float)
        })

    def toggleSimulation(self, state, toggle_button=False):
        super().toggleSimulation(state, toggle_button)
        self.buttons["AntCountSlider"].disable(state)

    def softReset(self):
        self.paths = [[] for _ in range(self.ant_count_obj[0])]
        for i in range(self.ant_count_obj[0]):
            self.paths[i].append(self.current_cities[i])

        self.moving = np.zeros(self.ant_count_obj[0], dtype=bool)
        self.finished = np.zeros(self.ant_count_obj[0], dtype=bool)

    def resetSimulation(self):
        self.pher_matrix = np.ones((self.cities.shape[0], self.cities.shape[0])) * INITAL_PHER_VALUE
        self.current_cities = np.zeros(self.ant_count_obj[0], dtype=int)
        self.target_cities = np.zeros(self.ant_count_obj[0], dtype=int)
        self.ant_positions = np.zeros((self.ant_count_obj[0], 2))

        for i in range(self.ant_count_obj[0]):
            self.ant_positions[i] = self.cities[self.current_cities[i]]

        self.moving_angles = np.zeros((self.ant_count_obj[0], 2))
        self.softReset()

    def performSimulationStep(self):
        # Drawing
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

        # Draw the ants
        for i in range(self.ant_count_obj[0]):
            pygame.draw.circle(window, colors['Green'],
                               (self.ant_positions[i] + self.center).astype(int), ANT_RADIUS)

        # Check if all ants are finished
        for i in range(self.ant_count_obj[0]):
            if len(self.paths[i]) == self.cities.shape[0] + 1:
                self.finished[i] = True

        if np.min(self.finished) == 1:
            self.globalUpdate()
            self.softReset()

        # Move the ants
        for i in range(self.ant_count_obj[0]):
            if self.finished[i]:
                continue

            if not self.moving[i]:
                self.decideCity(i)
            else:
                if np.linalg.norm(self.ant_positions[i] - self.cities[self.target_cities[i]]) < 5:
                    self.localUpdate(i)
                    self.moving[i] = False
                    self.current_cities[i] = self.target_cities[i]
                    self.paths[i].append(self.target_cities[i])
                else:
                    self.ant_positions[i] = self.ant_positions[i] + self.moving_angles[i] * self.simulation_speed_obj[0]

    def decideCity(self, ant_index):

        # If all cities are visited, go back to the starting city
        if len(self.paths[ant_index]) == self.cities.shape[0]:
            target_city_index = self.paths[ant_index][0]
        else:
            probability = np.zeros(self.cities.shape[0])

            for i in range(self.cities.shape[0]):
                if i not in self.paths[ant_index]:
                    probability[i] = (self.pher_matrix[self.current_cities[ant_index]][i]) ** (1 - self.beta_obj[0]) * \
                        (1 /
                         np.linalg.norm(self.cities[self.current_cities[ant_index]] -
                                        self.cities[i])) ** (self.beta_obj[0])

            exploit_roll = np.random.randint(0, 101)
            if exploit_roll > self.exp_obj[0]:
                target_city_index = np.argmax(probability)
            else:
                rand_roll = np.random.rand(1) * np.sum(probability) * 0.99
                for i in range(probability.shape[0]):
                    if rand_roll < probability[i]:
                        target_city_index = i
                        break
                    else:
                        rand_roll -= probability[i]

        self.target_cities[ant_index] = target_city_index
        self.moving_angles[ant_index] = self.cities[target_city_index] - self.ant_positions[ant_index]
        self.moving_angles[ant_index] = self.moving_angles[ant_index] / np.linalg.norm(self.moving_angles)
        self.moving[ant_index] = True

    def localUpdate(self, ant_index):
        self.pher_matrix[self.current_cities[ant_index]
                         ][self.target_cities[ant_index]] += self.alpha_obj[0] * self.r_obj[0]

    def globalUpdate(self):
        # Pheromone Decay
        for i in range(self.pher_matrix.shape[0]):
            for j in range(self.pher_matrix.shape[1]):
                self.pher_matrix[i][j] *= (1 - self.alpha_obj[0])
                self.pher_matrix[i][j] = max(self.pher_matrix[i][j], 0.05)

        # Find the shortest path
        sp_index = 0
        sp_len = -1
        for i in range(self.ant_count_obj[0]):
            path_len = 0
            path = self.paths[i]
            for j in range(1, len(path)):
                path_len += np.linalg.norm(self.cities[path[j]] - self.cities[path[j - 1]])
            if sp_len < 0 or path_len < sp_len:
                sp_len = path_len
                sp_index = i
        shortest_path = self.paths[sp_index]

        # Increase pheromone on the shortest path
        for i in range(1, len(shortest_path)):
            self.pher_matrix[shortest_path[i]][shortest_path[i - 1]] += ANT_OPT_CONSTANT * len(self.cities) / sp_len
            self.pher_matrix[shortest_path[i - 1]][shortest_path[i]] += ANT_OPT_CONSTANT * len(self.cities) / sp_len
